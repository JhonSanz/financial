
from rest_framework import serializers
from apps.order.models import Order


class CurrencySerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    amount = serializers.FloatField()

    class Meta:
        model = Order
        fields = ["currency", "amount"]

    def get_currency(self, instance):
        data = instance['currency'].split('|')
        return {
            "id": data[0],
            "symbol": data[1],
            "name": data[-1]
        }

class CurrencyAllSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["currency"]

    def get_currency(self, instance):
        data = instance['currency'].split('|')
        return {
            "id": data[0],
            "symbol": data[1],
            "name": data[-1]
        }
