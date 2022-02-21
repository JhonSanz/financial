import pandas as pd
import numpy as np
from rest_framework.serializers import ValidationError


class FileReader:
    FILE_COLUMNS_NAMES_BUY = [
        'Fecha', 'purchase_price', 'invested_amount_usd',
        'comission_binance', 'amount'
    ]
    FILE_COLUMNS_NAMES_SALE = [
        'fecha', 'sale_price', 'earned_amount_usd',
        'amount_usd', 'amount_currency_sold'
    ]

    def __init__(self, file):
        self.file = file
        self.df = self.convert(file)
        self.columns = []

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
        self.df.set_index(['position', 'index'], inplace=True)
        # Remove sub tables titles
        self.df = self.df[self.df[self.df.columns[0]] != self.columns[0]]
        self.df.columns = self.columns
        self.df = self.df[
            ~self.df[self.FILE_COLUMNS_NAMES_BUY[0]].isin(['', np.nan])
            &
            ~self.df[self.FILE_COLUMNS_NAMES_SALE[0]].isin(['', np.nan])
        ]

    def validate_file(self):
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

    def return_as_dict(self):
        self.df.dropna(how='all', inplace=True)
        self.df.dropna(axis=1, how='all', inplace=True)
        self.columns = self.df.iloc[0].tolist()
        # self.validate_file()
        self.clean_file()
        print(self.df)
        return {}
