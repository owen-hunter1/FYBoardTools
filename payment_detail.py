"""
Filename: payment_detail.py
Author: Owen Hunter
Date: 2026-02-11
Version: 1.0
Description: Payment Detail class. Relevent information and helpers for importing payment detail reports
"""

import extract_msg
import pdfplumber
from pathlib import Path
import re
import pandas as pd

# Payment Detail Class
# Stores relevent information about the payment detail reports
# Imports msg, pdf
# Converts to dataframe 
class PaymentDetail:
    def __init__(self):
        self.dining_center = ""
        self.credit_count = 0
        self.credit_amount = 0
        self.cash_count = 0
        self.cash_amount = 0

    # Loads payment details from email
    # extracts pdf from email
    # calls load from pdf
    # todo: could be tightened up a little, needs check for filename
    # todo: handle empty emails
    def load_from_email(self, path):
        msg = extract_msg.Message(path)
        for attachment in msg.attachments:
            pdf_path = "./pdfs/" + str(attachment.longFilename)
            if Path(pdf_path).exists():
                break
            attachment.save(customPath="./pdfs/")
        
        self.load_from_pdf(pdf_path)

    # loads payment details from pdfs
    # store cash and credit counts and amounts
    # todo: used pdf plumber when I should have used camelot. camelot parses pdf tables better. if regex breaks, it may be worth considering a rewrite using camelot
    # todo: handle empty pdfs
    def load_from_pdf(self, path):
        self.credit_count = 0
        self.credit_amount = 0
        self.cash_count = 0
        self.cash_amount = 0

        # dining center regex
        # stored name in dining_center
        dining_center_pattern = re.compile(
            r"Payment\s+Detail\s+by\s+Time\s+(?P<dining_center>.+?)\s+Last",
            re.IGNORECASE        
        )

        # totals regex
        # stores values in: label, amount, and count
        totals_pattern = re.compile(
            r"""
            ^\s*
            (?P<label>External\ Totals:|Credit\ Totals:)\s+
            \$(?:[\d,]+\.\d{2})\s+
            \$(?:[\d,]+\.\d{2})\s+
            \$(?:[\d,]+\.\d{2})\s+
            \$(?P<amount>[\d,]+\.\d{2})\s+
            (?:-|(?:[\d,]+\.\d{2}))\s+
            (?:-|\$(?:[\d,]+\.\d{2}))\s+
            (?P<count>[\d,]+)
            \s*$
            """,
            re.VERBOSE
        )

        # find dining center name
        match = dining_center_pattern.search(str(path))
        if match:
            self.dining_center = match["dining_center"]

        # opens pdf, loops through pages, loops through lines, extracts totals 
        with pdfplumber.open(path) as pdf:
            total_flag = False

            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                for line in text.splitlines():
                    line = " ".join(line.split())

                    if "total all registers" in line.lower(): # loop until we find the total all reisters lie
                        total_flag = True
                        continue

                    if not total_flag: # loops to here
                        continue

                    match = totals_pattern.search(line) # search line for regex pattern
                    if match: # sum cash and credit amounts if found
                        if match["label"] in "External Totals:":
                            self.cash_amount += float(match["amount"].replace(",", ""))
                            self.cash_count += int(match["count"].replace(",", ""))
                        elif match["label"] in "Credit Totals:":
                            self.credit_amount += float(match["amount"].replace(",", ""))
                            self.credit_count += int(match["count"].replace(",", ""))
    # payment details to dataframe
    # converts the counts and amounts to a dataframe
    # returns a dataframe
    def to_df(self):
        df = pd.DataFrame({
            "Dining Center": [self.dining_center],
            "Cash Amount": [self.cash_amount],
            "Cash Count": [self.cash_count],
            "Credit Amount": [self.credit_amount],
            "Credit Count": [self.credit_count],
            "Total Amount": [self.credit_amount + self.cash_amount],
            "Total Count": [self.credit_count + self.cash_count]
        })

        return df

    # debug string
    def __str__(self):
        return f"Payment Summary for {self.dining_center}:\ncredit amount: {self.credit_amount} \ncredit count: {self.credit_count} \ncash amount: {self.cash_amount}\ncash count: {self.cash_count}"
        