from stored_value import StoredValue
from glob import glob
from pathlib import Path

def main():
    sv = load_stored_values()
    print(sv)

def load_stored_values():
    print("Loading stored values...")
    
    sv = StoredValue()
    files = glob("./csvs/Tufts_Dining_Weekly_Summary_Stored_Value*.csv")
    if len(files) == 0:
        print("Stored value file not found")
        print("Failed to load Stored Value")
        return sv
    
    if len(files) > 1:
        print("More than one stored value file found")
        print("Failed to load Stored Value")
        return sv

    for file in files:
        sv.load_from_csv(file)
        print("Successfully loaded Stored Value")
    return sv


main()