SV_OUTPUT_COLUMNS = ["JC STUDENT","MEAL MONEY","JC DEPT CARDS","JC FAC/ STAFF"]
SV_OUTPUT_ROWS = ["CARMICHAEL", "DEWICK/MACP.", "CATERING", "MUGAR CAFÉ", "HILLEL", "COMMONS", "HOTUNG CAFE", "HODGDON ON-THE-RUN", "PAX ET LOX", "TOWER CAFÉ", "KINDLEVAN CAFÉ", "SMFA CAFÉ"]

SV_COLUMNS = ["SV Tran Profit Center Name", "Classification", "SV Account Type Name", "Count of SV Transactions", "Sum of SV Tran Amount"]

SV_ACCOUNT_MAP = {
    "Department Dining Credit SV": "JC DEPT CARDS",
    "JumboCash Faculty/Staff": "JC FAC/ STAFF",
    "JumboCash Student": "JC STUDENT",
    "SMFA Meal Money": "MEAL MONEY",
    "Department Dining Limited": "JC DEPT CARDS",
    "{null}": ""
}

SV_LOCATION_MAP = {
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
