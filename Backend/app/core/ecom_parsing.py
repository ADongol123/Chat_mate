from fastapi import FastAPI, UploadFile, File,  HTTPException
import tempfile
import pandas as pd
import os
from io import BytesIO
import fitz 
from typing import List
import io

import swifter

def detect_file_type(file: UploadFile) -> str:
    if file.filename.endswith(".csv"):
        return "csv"
    elif file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
        return "excel"
    else:
        raise ValueError("Unsupported file type")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(how='all')  # Remove completely empty rows
    df = df.dropna(axis=1, thresh=len(df) * 0.5)  # Drop sparse columns
    df.fillna("", inplace=True)
    return df


def select_text_columns(df: pd.DataFrame) -> List[str]:
    object_cols = df.select_dtypes(include=['object', 'string']).columns
    return [col for col in object_cols if df[col].str.len().mean() > 3]


def dataframe_to_text_list(df: pd.DataFrame) -> List[str]:
    text_cols = select_text_columns(df)
    return df[text_cols].apply(lambda row: " | ".join(row.astype(str)), axis=1).tolist()



def read_file(file: UploadFile, file_type: str) -> pd.DataFrame:
    contents = file.file.read()
    if file_type == "csv":
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    else:
        df = pd.read_excel(io.BytesIO(contents))
    return clean_dataframe(df)




def pdf_to_dataframe(content: bytes) -> pd.DataFrame:
    text_data = []
    doc = fitz.open(stream=content, filetype="pdf")
    for page in doc:
        text_data.append(page.get_text())

    full_text = "\n".join(text_data)
    return pd.DataFrame({"text": [full_text]})

def infer_text_from_row(row: pd.Series) -> str:
    row = row.dropna()
    text_parts = []
    for col, val in row.items():
        val_str = str(val).strip()
        if val_str:
            text_parts.append(f"{col.capitalize()}: {val_str}")
    return " | ".join(text_parts)

import swifter

def dataframe_to_text_list(df: pd.DataFrame) -> List[str]:
    def row_to_text(row):
        return " | ".join([
            f"{col.capitalize()}: {str(val).strip()}"
            for col, val in row.items() if pd.notna(val) and str(val).strip()
        ])
    return df.swifter.apply(row_to_text, axis=1).tolist()




