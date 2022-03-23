import pandas as pd
import numpy as np
from rest_framework.serializers import ValidationError
from apps.order.models import Order
from apis.order.serializers.order import (
    OrderCreateSerializer, OrderFileCreateSerializer)


class FileReader:
    FILE_COLUMNS_NAMES_BUY = [
        'date', 'purchase_price', 'invested_amount_usd',
        'commission_binance', 'amount_currency'
    ]
    FILE_COLUMNS_NAMES_SALE = [
        'date_sale', 'sale_price', 'earned_amount_usd',
        'amount_usd', 'amount_currency_sold'
    ]

    def __init__(self, file, request):
        self.file = file
        self.df = self.convert(file)
        self.columns = []
        self.orders = []
        self.request = request

    @staticmethod
    def convert(file):
        return pd.read_excel(file)

    @staticmethod
    def set_position_index(row, ranges):
        if len(ranges) == 1:
            return 1
        i = 0
        for first, second in zip(ranges, ranges[1:]):
            if first <= row[0] < second:
                return i
            i += 1
        return i

    def clean_file(self):
        self.df.reset_index(inplace=True)
        self.df.drop('index', axis=1, inplace=True)
        self.df.reset_index(inplace=True)
        self.df['position'] = 0
        ranges = self.df[
            self.df[self.df.columns[1]] == self.columns[0]
            ]['index'].tolist()
        self.df['position'] = self.df[['index', self.df.columns[1]]].apply(
            lambda x: self.set_position_index(x, ranges),
            axis=1
        )
        # Remove sub tables titles
        self.df.drop('index', axis=1, inplace=True)
        self.df = self.df[self.df[self.df.columns[0]] != self.columns[0]]
        self.df.columns = self.columns + ['position']
        self.df = self.df[
            ~self.df[self.FILE_COLUMNS_NAMES_BUY[0]].isin(['', np.nan])
            &
            ~self.df[self.FILE_COLUMNS_NAMES_SALE[0]].isin(['', np.nan])
        ]
        self.df = self.df \
            .groupby('position', as_index=False) \
            .apply(lambda x: x.reset_index(drop=True)) \
            .reset_index() \
            .drop('level_0', axis=1)\
            .set_index(['position', 'level_1'])
        self.df['date'] = pd.to_datetime(self.df['date']).dt.date
        self.df['date_sale'] = pd.to_datetime(self.df['date_sale']).dt.date

    def validate_file(self):
        # if self.file.name.split('.')[0]

        if self.df.empty:
            raise ValidationError(detail={
                'detail': 'Empty file'
            })

        if set(self.columns) != set(
                self.FILE_COLUMNS_NAMES_BUY + self.FILE_COLUMNS_NAMES_SALE
        ):
            raise ValidationError(detail={
                'detail': 'Invalid columns names'
            })

        validate_columns_df = self.df[
            self.df[self.df.columns[0]] == self.columns[0]
            ].apply(
            lambda x: set(x.tolist()) != set(
                self.FILE_COLUMNS_NAMES_BUY + self.FILE_COLUMNS_NAMES_SALE
            )
        )
        if not validate_columns_df.all():
            raise ValidationError(detail={
                'detail': 'Invalid columns names'
            })

    def add_to_schema(self, data):
        if len(data) > 1:
            self.orders.append(
                {
                    'position': data[0],
                    'sales': [data[-1]]
                }
            )
        else:
            self.orders[-1]['sales'].append(data[0])

    def validate_row(self, row):
        if row.name[-1] != 0:
            aux = [
                {**row[self.FILE_COLUMNS_NAMES_SALE].to_dict(), 'type': Order.SELL}
            ]
        else:
            aux = [
                {**row[self.FILE_COLUMNS_NAMES_BUY].to_dict(), 'type': Order.BUY},
                {**row[self.FILE_COLUMNS_NAMES_SALE].to_dict(), 'type': Order.SELL}
            ]
        data = list(map(lambda value: {
            "order_date": value['date'] if 'date' in value else value['date_sale'],
            "currency": self.file.name.split('.')[0],
            "purchase_price": (
                value['purchase_price'] if 'purchase_price' in value
                else value['sale_price']
            ),
            "invested_amount_usd": (
                value['invested_amount_usd'] if 'invested_amount_usd' in value
                else value['earned_amount_usd']
            ),
            "invested_amount_cop": 0,
            "commission_conversion": 0,
            "commission_purchase_binance": (
                value['commission_binance'] if 'commission_binance' in value
                else 0
            ),
            "type": value['type'],
            "amount_currency": (
                value['amount_currency'] if 'amount_currency' in value
                else value['amount_currency_sold']
            ),
        }, aux))
        serializer = OrderCreateSerializer(data=data, many=True)
        if not serializer.is_valid():
            raise ValidationError(detail={
                'detail': f'Invalid row data',
                'data': serializer.errors
            })
        self.add_to_schema(data)

    def create_records(self):
        self.df.apply(lambda x: self.validate_row(x), axis=1)
        serializer = OrderFileCreateSerializer(
            data=self.orders, many=True,
            context={
                "request": self.request
            }
        )
        if not serializer.is_valid():
            raise ValidationError(detail={
                'detail': f'Invalid row data',
                'data': serializer.errors
            })
        serializer.save()

    def return_as_dict(self):
        self.df.dropna(how='all', inplace=True)
        self.df.dropna(axis=1, how='all', inplace=True)
        self.columns = self.df.iloc[0].tolist()
        self.validate_file()
        self.clean_file()
        self.create_records()
        return {}
