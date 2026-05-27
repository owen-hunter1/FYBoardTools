import pandas as pd
import report_tools.config as config

class Report:
    def __init__(self):
        self.data_df = pd.DataFrame()
        self.counts_df = pd.DataFrame()
        self.dollars_df = pd.DataFrame()
        self.total_count = 0
        self.total_amount = 0

    # loads report details from CSV
    def load_from_csv(self, path):
        df = pd.read_csv(path) # load whole report
        self.data_df = self.parse_data_from_csv(df)
        self.counts_df = self.get_counts_df(self.data_df)
        self.dollars_df = self.get_dollars_df(self.data_df)

    # parse subdata and extract totals
    def parse_data_from_csv(self, df:pd.DataFrame):
        # get last row of data for totals and extracing subframe
        mask = (
            (df.iloc[:,0:3] == "{null}").all(axis=1) & # 3 {nulls}
            (df.iloc[:,3] != "{null}") # followed by the total value (not {null})
        )

        mask = (
            df[config.SV_COLUMNS[:]]
        )

        last_row = mask.idxmax() + 1
        # extract totals
        self.total_count = df[mask].iloc[:,3].iloc[0] 
        self.total_amount = df[mask].iloc[:,4].iloc[0] 

        df = df.iloc[:last_row,:] # extract relevant data

        # remove totals and subtotals
        mask = (df.iloc[:,0:3] != "{null}").all(axis=1) # flag any {nulls}

        df = df[mask]
        
        # clean data
        df.iloc[:,3] = pd.to_numeric(df.iloc[:,3], errors="coerce")
        df.iloc[:,4] = pd.to_numeric(df.iloc[:,4], errors="coerce")

        return df
