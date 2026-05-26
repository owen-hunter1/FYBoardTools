from cash_equiv import CashEquiv
from glob import glob
from pathlib import Path

def main():
    ce = load_cash_equiv()


def load_cash_equiv():
    print("Loading stored values...")
    ce = CashEquiv()
    return ce