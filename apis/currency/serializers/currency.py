
from rest_framework import serializers
from apps.order.models import Order


class CurrencySerializer(serializers.ModelSerializer):
    currency = serializers.CharField()
    amount = serializers.FloatField()

    class Meta:
        model = Order
        fields = ["currency", "amount"]
