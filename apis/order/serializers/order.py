from rest_framework import serializers
from apps.order.models import Order
from django.db import transaction

class OrderSerializer(serializers.ModelSerializer):
    type_str = serializers.CharField(source='get_type_display')

    class Meta:
        model = Order
        fields = [
            "id", "owner", "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "commission_conversion", "commission_purchase_binance",
            "type", "type_str"
        ]


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
        position = Order.objects.create(**{
            **validated_data.get('position'),
            'owner': owner
        })
        if validated_data.get('sales'):
            Order.objects.bulk_create([
                Order(**{
                    **sale,
                    'position': position,
                    'owner': owner,
                })
                for sale in validated_data.get('sales')
            ])
