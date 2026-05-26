import pandas as pd

OUTPUT_COLUMNS = ["JC STUDENT","MEAL MONEY","JC DEPT CARDS","JC FAC/ STAFF"]
OUTPUT_ROWS = ["CARMICHAEL", "DEWICK/MACP.", "CATERING", "MUGAR CAFÉ", "HILLEL", "COMMONS", "HOTUNG CAFE", "HODGDON ON-THE-RUN", "PAX ET LOX", "TOWER CAFÉ", "KINDLEVAN CAFÉ", "SMFA CAFÉ"]

ACCOUNT_MAP = {
    "Department Dining Credit SV": "JC DEPT CARDS",
    "JumboCash Faculty/Staff": "JC FAC/ STAFF",
    "JumboCash Student": "JC STUDENT",
    "SMFA Meal Money": "MEAL MONEY",
    "Department Dining Limited": "JC DEPT CARDS",
    "{null}": ""
}

LOCATION_MAP = {
    "Carmichael": "CARMICHAEL",
    "Dewick-MacPhie": "DEWICK/MACP.",
    "Catering": "CATERING",
    "Mugar Cafe": "MUGAR CAFÉ",
    "Hillel": "HILLEL",
    "Commons Marketplace": "COMMONS",
    "Hotung Cafe": "HOTUNG CAFE",
    "Hodgdon": "HODGDON ON-THE-RUN",
    "Pax et Lox": "PAX ET LOX",
    "Tower Cafe": "TOWER CAFÉ",
    "Kindlevan Cafe": "KINDLEVAN CAFÉ",
    "SMFA Cafe": "SMFA CAFÉ",
    "{null}": "Totals"
}

class StoredValue:
    def __init__(self):
        self.data_df = pd.DataFrame()
        self.counts_df = pd.DataFrame()
        self.dollars_df = pd.DataFrame()
        self.output_df = pd.DataFrame(data=0,  index=OUTPUT_ROWS, columns=OUTPUT_COLUMNS)
        self.total_count = 0
        self.total_amount = 0

        # silence fill error, should be explored why this is happening
        pd.set_option('future.no_silent_downcasting', True)

    # loads stored value details from CSVs
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
    
    # translate data to counts with pivot table
    def get_counts_df(self, df:pd.DataFrame):
        df = df.copy()
        df["FYBoard Account"] = df.iloc[:,2].replace(ACCOUNT_MAP)
        df["FYBoard Location"] = df.iloc[:,0].replace(LOCATION_MAP)

        df = pd.pivot_table(
            df,
            values=df.columns.to_list()[3],
            index=df.columns.to_list()[6],
            columns=df.columns.to_list()[5],
            aggfunc="sum",
            fill_value=0
        )

        df = self.clean_pivot(df)

        return df

    # translate data to dollars with pivot table
    def get_dollars_df(self, df:pd.DataFrame):
        df = df.copy()
        df["FYBoard Account"] = df.iloc[:,2].replace(ACCOUNT_MAP)
        df["FYBoard Location"] = df.iloc[:,0].replace(LOCATION_MAP)
        
        df = pd.pivot_table(
            df,
            values=df.columns.to_list()[4],
            index=df.columns.to_list()[6],
            columns=df.columns.to_list()[5],
            aggfunc="sum",
            fill_value=0
        )

        df = self.clean_pivot(df)

        return df

    # clean the df after pivot
    def clean_pivot(self, df):
        df = df.copy()
        
        # remove index name
        df.index.name = None

        # add missing rows and columns
        df = df.reindex(index=OUTPUT_ROWS, columns=OUTPUT_COLUMNS, fill_value=0.0)
        
        # add totals
        df["Location Total"] = df.sum(axis=1)
        df.loc["Total"] = df.sum(axis=0)

        return df


    # string definition
    def __str__(self):
        return (
            "Stored Value\n"
            "Data:\n"
            f"{self.data_df}\n"
            "Counts:\n"
            f"{self.counts_df}\n"
            "Dollars:\n"
            f"{self.dollars_df}\n"
            "Output:\n"
            f"{self.output_df}\n"
            f"Total Count: {self.total_count}\n"
            f"Total Amount: {self.total_amount}\n"
        )
    
