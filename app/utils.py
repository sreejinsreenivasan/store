import pandas as pd


def read_excel(file):
    df = pd.read_excel(file, engine="openpyxl")
    df = df.dropna(how="all")
    return df


def find_enabled(value):
    bool = value.lower()
    is_enabled = True if bool == "yes" or bool == "y" else False
    return is_enabled
