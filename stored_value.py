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

    # loads stored value details from CSVs
    def load_from_csv(self, path):
        df = pd.read_csv(path) # load whole report
        self.data_df = self.parse_data_from_csv(df)
        self.output_df = self.to_fyboard_df(self.data_df)

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

        return df
    
    # translate data to fyboard format
    def to_fyboard_df(self, df:pd.DataFrame):
        print(df)
        df["FYBoard Account"] = df.iloc[:,2].replace(ACCOUNT_MAP)
        df["FYBoard Location"] = df.iloc[:,0].replace(LOCATION_MAP)
        
        # todo: create pivot table 
        
        return df
    
    def print(self):
        print("Stored Value")
        print("Data")
        print(self.data_df)
        print("Output")
        print(self.output_df)
        print(f"Total Count: {self.total_count}")
        print(f"Total Amount: {self.total_amount}")