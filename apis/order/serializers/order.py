from rest_framework import serializers
from apps.order.models import Order
from django.db import transaction


class OrderSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    type_str = serializers.CharField(source='get_type_display')

    class Meta:
        model = Order
        fields = [
            "id", "owner", "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "commission_conversion", "commission_purchase_binance",
            "type", "type_str", "amount_currency"
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
        return {
            'position': OrderSerializer(instance).data,
            'sales': OrderSerializer(
                Order.objects.filter(position=instance).exclude(pk=instance.pk),
                many=True
            ).data
        }


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "commission_conversion", "commission_purchase_binance",
            "type", "amount_currency"
        ]

    def create(self, validated_data):
        owner = self.context['request'].user
        return super().create({**validated_data, 'owner': owner})


class OrderFileCreateSerializer(serializers.Serializer):
    position = OrderCreateSerializer()
    sales = OrderCreateSerializer(many=True)

    class Meta:
        fields = ["position", "sales"]

    @transaction.atomic
    def create(self, validated_data):
        owner = self.context['request'].user
        position = Order(**{
            **validated_data.get('position'),
            'owner': owner
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
                })
                for sale in validated_data.get('sales')
            ])
