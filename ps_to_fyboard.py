"""
Filename: ps_to_fyboard.py
Author: Owen Hunter
Date: 2026-02-11
Version: 1.0
Description: This loads information relevant to fyboard from payment details and payment summaries from email containing pdf or pdf and exports it to a csv
"""

from report_tools.payment_detail import PaymentDetail
from report_tools.payment_summary import PaymentSummary

import pandas as pd

import glob

def main():
    payment_summary = load_payment_summary()
    payment_details = load_payment_details()

    payments_df = create_df(payment_summary, payment_details)

    export_df_to_csv(payments_df)
    
    
# Load payment summary
# Returns the payment summary from emails 
def load_payment_summary():
    print("loading payment summary...")
    payment_summary = PaymentSummary()
    for file in glob.glob('./emails/*Payment*Summary*.msg'): # glob gets emails matching pattern
        payment_summary.load_from_email(file)
    return payment_summary

# Load payment details
# Returns a list of payment details
def load_payment_details():
    print("loading payment summary...")
    payment_details = []
    for file in glob.glob('./emails/*Payment*Detail*.msg'):
        payment_detail = PaymentDetail()
        payment_detail.load_from_email(file)
        payment_details.append(payment_detail)
    return payment_details

# Create Dataframe
# Takes the payment summary and payment details converts them into a dataframe
# Inserts totals and labels
# Returns a dataframe
def create_df(payment_summary, payment_details):
    print("creating dataframe...")
    dfs = [payment_detail.to_df() for payment_detail in payment_details]
    df = pd.concat(dfs, ignore_index=True)


    totals = df.select_dtypes("number").sum() # sums columns containing numbers to new dataframe
    totals_df = totals.to_frame().T
    totals_df.insert(0, df.columns[0], "{Payment Detail Totals}") # adding labels

    df = pd.concat([df, totals_df], ignore_index=True)
    df = pd.concat([df, payment_summary.to_df()])

    return df

# Export dataframe to csv
# saves dataframe to csv
def export_df_to_csv(df: pd.DataFrame):
    print("exporting to exports/output.csv")
    df = df.round(2)
    try:
        df.to_csv("./exports/output.csv", index=None)
    except:
        print("Export failed. File output.csv is in use. Close the file and try again")
        exit(-1)
    
    print("export successful!")


main()