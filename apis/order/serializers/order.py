
from rest_framework import serializers
from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    type_str = serializers.CharField(source='get_type_display')

    class Meta:
        model = Order
        fields = [
            "pk", "owner", "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "comission_convertion", "comission_purchase_binance",
            "type", "type_str"
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "owner", "order_date", "currency", "purchase_price",
            "invested_amount_usd", "invested_amount_cop",
            "comission_convertion", "comission_purchase_binance",
            "type",
        ]
