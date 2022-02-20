import pandas as pd


class FileReader:
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
        self.df.dropna(how='all', inplace=True)
        self.df.dropna(axis=1, how='all', inplace=True)
        self.columns = self.df.iloc[0].tolist()
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
        self.df = self.df[self.df[self.df.columns[0]] != self.columns[0]]
        self.df.columns = self.columns

    def validate_file(self):
        print(self.df)
        return {}

    def return_as_dict(self):
        self.clean_file()
        self.validate_file()
        return {}
