"""
Filename: payment_summary.py
Author: Owen Hunter
Date: 2026-02-11
Version: 1.0
Description: Payment Summary class. Relevent information and helpers for importing payment summary reports
"""

import extract_msg
import pdfplumber
from pathlib import Path
import re
import pandas as pd

# Payment Summary Class
# Stores relevent information about the payment summary reports
# Imports msg, pdf
# Converts to dataframe 
class PaymentSummary:
    def __init__(self):
        self.count = 0
        self.amount = 0

    # Loads payment summary from email
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
        
    # loads payment summary from pdfs
    # store cash and credit counts and amounts
    # todo: used pdf plumber when I should have used camelot. camelot parses pdf tables better. if regex breaks, it may be worth considering a rewrite using camelot
    # todo: handle empty pdfs
    def load_from_pdf(self, path):
        self.count = 0
        self.amount = 0

        # totals regex
        # stores values in: label, amount, and count
        pattern = re.compile(
            r"""
            (?P<label>Student\ Cash|Taxable\ Cash|Discover|Mastercard|Visa)\s+
            \$?(?P<amount>[\d,]+\.\d{2})\s+
            (?P<count>[\d,]+)\s+Transactions
            """,
            re.VERBOSE
        )

        # opens pdf, loops through pages, loops through lines, extracts totals 
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                for line in text.splitlines():
                    match = pattern.search(line)
                    if match:
                        self.amount += float(match["amount"].replace(",", ""))
                        self.count += int(match["count"].replace(",", ""))
    # payment summary to dataframe
    # converts the counts and amounts to a dataframe
    # returns a dataframe
    def to_df(self):
        df = pd.DataFrame({
            "Dining Center": ["Payment Summary by Time"],
            "Total Amount": [self.amount],
            "Total Count": [self.count]
        })

        return df

    # debug string
    def __str__(self):
        return f"Payment Summary:\namount: {self.amount}\ncount: {self.count}"