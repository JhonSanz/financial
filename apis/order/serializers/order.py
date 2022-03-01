from rest_framework import serializers
from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    type_str = serializers.CharField(source='get_type_display')

    class Meta:
        model = Order
        fields = [
            "id", "owner", "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "comission_convertion", "comission_purchase_binance",
            "type", "type_str"
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "comission_convertion", "comission_purchase_binance",
            "type", "amount_currency"
        ]

    def create(self, validated_data):
        owner = self.context['request'].user
        return super().create({**validated_data, 'owner': owner})
