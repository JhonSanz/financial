from django.db.models import When, Case, Sum, F
from rest_framework import serializers
from apps.order.models import Order
from rest_framework.serializers import ValidationError
from django.db import transaction
from apis.utils.currency_name_from_object import convert_object_to_name
from apis.utils.currency_list import get_currencies


class OrderSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    type_str = serializers.CharField(source='get_type_display')

    class Meta:
        model = Order
        fields = [
            "id", "owner", "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "commission_conversion", "commission_purchase_binance",
            "type", "type_str", "amount_currency", "amount_usd"
        ]

    def get_currency(self, instance):
        data = instance.currency.split('|')
        return {
            "id": data[0],
            "symbol": data[1],
            "name": data[-1]
        }


class OrderPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order

    def to_representation(self, instance):
        sales = Order.negative_columns.filter(position=instance).exclude(pk=instance.pk)
        totals = sales.negative_values([
            'amount_currency', 'amount_usd'
        ]).aggregate(
            currency_total=Sum('negative_amount_currency'),
            usd_total=Sum('negative_amount_usd'),
        )
        currency_total = totals.get("currency_total")
        usd_total = totals.get("usd_total")
        print('test', usd_total)
        return {
            'position': OrderSerializer(instance).data,
            'sales': OrderSerializer(sales, many=True).data,
            'totals': {
                "currency_total": (
                    (currency_total if currency_total is not None else 0)
                    + instance.amount_currency
                ),
                "usd_total": (
                    (usd_total if usd_total is not None else 0)
                    + instance.invested_amount_usd
                ),
            }
        }


class OrderCreateSerializer(serializers.ModelSerializer):
    currency = serializers.JSONField()

    class Meta:
        model = Order
        fields = [
            "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "commission_conversion", "commission_purchase_binance",
            "type", "amount_currency", "amount_usd"
        ]

    def validate_currency(self, value):
        aux = value.copy()
        if aux.keys() != {'id', 'symbol', 'name', 'label'}:
            raise ValidationError(detail={
                'detail': 'Invalid form data'
            })
        aux.pop('label')
        if not filter(lambda x: x == aux, get_currencies()):
            raise ValidationError(detail={
                'detail': 'Currency not found'
            })
        return value

    def create(self, validated_data):
        owner = self.context['request'].user
        currency = convert_object_to_name(validated_data.pop('currency'))
        return super().create({
            **validated_data, 'owner': owner, 'currency': currency
        })


class OrderFileCreateSerializer(serializers.Serializer):
    position = OrderCreateSerializer()
    sales = OrderCreateSerializer(many=True)

    class Meta:
        fields = ["position", "sales"]

    @transaction.atomic
    def create(self, validated_data):
        owner = self.context['request'].user
        currency = convert_object_to_name(
            validated_data['position'].pop('currency'))
        position = Order(**{
            **validated_data.get('position'),
            'owner': owner,
            'currency': currency
        })
        position.save()
        position.position = position
        position.save()
        if validated_data.get('sales'):
            Order.objects.bulk_create([
                Order(**{
                    **sale,
                    'position': position,
                    'owner': owner,
                    'currency': currency
                })
                for sale in validated_data.get('sales')
            ])
