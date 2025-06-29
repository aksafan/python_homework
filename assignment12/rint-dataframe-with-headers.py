import pandas as pd

class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)

        return cls(df)

    def print_with_headers(self):
        df_len = len(self)
        print(df_len)
        start, end = 0, 10
        while start < df_len:
            print(super().iloc[start:min(end, df_len)])
            start += 10
            end += 10


dfp = DFPlus.from_csv("../csv/products.csv")
dfp.print_with_headers()
