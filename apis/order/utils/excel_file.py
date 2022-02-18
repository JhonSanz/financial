import pandas as pd


class FileReader:
    def __init__(self, file):
        self.file = file
        self.df = self.convert(file)

    @staticmethod
    def convert(file):
        return pd.read_excel(file)

    @staticmethod
    def set_position_index(row):
        i = 0
        if row[1] == 'Fecha':
            i += 1
        return i

    def clean_file(self):
        self.df.dropna(how='all', inplace=True)
        self.df.dropna(axis=1, how='all', inplace=True)
        self.df.reset_index(inplace=True)
        self.df['position'] = 0
        self.df['position'] = self.df[['index', self.df.columns[1]]].apply(
            lambda x: self.set_position_index(x),
            axis=1
        )

    def validate_file(self):
        print(self.df)
        return {}

    def return_as_dict(self):
        self.clean_file()
        self.validate_file()
        return {}
