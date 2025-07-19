import pandas as pd
from typing import List

def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(file_path)


def load_excel(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    """Load an Excel file into a DataFrame."""
    return pd.read_excel(file_path, sheet_name=sheet_name) 