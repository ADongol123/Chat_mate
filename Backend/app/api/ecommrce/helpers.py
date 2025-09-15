import pandas as pd


def dataframe_to_text_list(df: pd.DataFrame) -> list:
    # Combine textual columns into single string per row
    text_cols = df.select_dtypes