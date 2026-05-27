from report_tools.config import *

config = ReportConfig(
    output_rows=SV_OUTPUT_ROWS,
    output_columns=SV_OUTPUT_COLUMNS,
    location_map=SV_LOCATION_MAP,
    account_map=SV_ACCOUNT_MAP,    
)

def config_test():
    print(config)


config_test()