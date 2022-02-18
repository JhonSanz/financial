import pandas as pd


class FileReader:
    def __init__(self, file):
        self.file = file
        self.df = self.convert(file)

    @staticmethod
    def convert(file):
        return pd.read_excel(file)

    def clean_file(self):
        self.df = self.df[self.df['EPS'].notna()]

    def validate_file(self):
        print(self.df)
        return {}

    def return_as_dict(self):
        self.clean_file()
        self.validate_file()
        return {}
