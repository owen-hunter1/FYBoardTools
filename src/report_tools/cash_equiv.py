import pandas as pd

class CashEquiv:
    def __init__(self):
        self.data_df = pd.DataFrame()
        self.counts_df = pd.DataFrame()
        self.dollars_df = pd.DataFrame()
        self.total_count = 0
        self.total_amount = 0

        # silence fill error, should be explored why this is happening
        pd.set_option('future.no_silent_downcasting', True)

    def load_from_csv(self, path):
        df = pd.read_csv(path)