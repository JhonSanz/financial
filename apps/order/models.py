
from django.db import models
from django.db.models import Case, F, When
from apps.utils.base_table import CommonData
from apps.user.models import User


class NegativeColumnsManager(models.QuerySet):
    def negative_values(self):
        return self.annotate(
            negative_amount=Case(
                When(type=0, then=F('amount_currency') * -1),
                default=F('amount_currency')
            ),
            negative_invested_amount_usd=Case(
                When(type=0, then=F('invested_amount_usd') * -1),
                default=F('invested_amount_usd')
            )
        )


class Order(CommonData):
    SELL = 0
    BUY = 1
    ORDER_TYPE = [
        (SELL, 'Sell'),
        (BUY, 'Buy'),
    ]

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    order_date = models.DateField()
    currency = models.CharField(max_length=250)
    purchase_price = models.FloatField()
    amount_currency = models.FloatField()
    invested_amount_usd = models.FloatField()
    amount_usd = models.FloatField()
    invested_amount_cop = models.FloatField()
    commission_conversion = models.FloatField()
    commission_purchase_binance = models.FloatField()
    type = models.PositiveSmallIntegerField(choices=ORDER_TYPE)
    position = models.ForeignKey(
        'self', null=True, on_delete=models.PROTECT)
    objects = models.Manager()
    negative_columns = NegativeColumnsManager.as_manager()

    def __str__(self):
        return f'{self.currency}: {self.invested_amount_usd} USD'
