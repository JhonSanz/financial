
from django.db import models
from apps.utils.base_table import CommonData
from apps.user.models import User


class Order(CommonData):
    SELL = 0
    BUY = 1
    ORDER_TYPE = [
        (SELL, 'Sell'),
        (BUY, 'Buy'),
    ]

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    order_date = models.DateField()
    currency = models.CharField(max_length=10)
    purchase_price = models.FloatField()
    invested_amount_usd = models.FloatField()
    invested_amount_cop = models.FloatField()
    comission_convertion = models.FloatField()
    comission_purchase_binance = models.FloatField()
    type = models.PositiveSmallIntegerField(choices=ORDER_TYPE)

    def __str__(self):
        return f'{self.currency}: {self.amount_usd} USD'
