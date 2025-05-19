from fastapi import FastAPI, UploadFile, File,  HTTPException
import tempfile
import pandas as pd
import os
from io import BytesIO
import fitz 
from typing import List

def detect_file_type(file: UploadFile) -> str:
    ext = file.filename.split('.')[-1].lower()
    return ext

def read_file(file: UploadFile, file_type: str) -> pd.DataFrame:
    contents = file.file.read()
    print(file_type,"file_type")
    if file_type == 'csv':
        return pd.read_csv(BytesIO(contents))
    elif file_type in ['xlsx', 'xls']:
        return pd.read_excel(BytesIO(contents))
    elif file_type == 'pdf':
        return pdf_to_dataframe(contents)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

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

def dataframe_to_text_list(df: pd.DataFrame) -> List[str]:
    return [infer_text_from_row(row) for _, row in df.iterrows()]
    
    
def save_temp_file(file: UploadFile) -> str:
    """Save uploaded file to a temporary path and return the path."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.file.read())
        return tmp.name

def load_and_clean_csv(path: str) -> pd.DataFrame:
    """Load and clean the CSV data."""
    df = pd.read_csv(path)
    os.remove(path)  

    df.columns = df.columns.str.strip().str.lower()

    df.fillna({
        'title': 'No title',
        'stars': 0.0,
        'reviews': 0,
        'price': '0',
        'listprice': '0',
        'category_id': 'unknown',
        'isbestseller': False,
        'boughtinlastmonth': 0
    }, inplace=True)

    df['title'] = df['title'].astype(str).str.strip()
    df['stars'] = pd.to_numeric(df['stars'], errors='coerce').fillna(0.0)
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce').fillna(0).astype(int)
    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['listprice'] = df['listprice'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['boughtinlastmonth'] = pd.to_numeric(df['boughtinlastmonth'], errors='coerce').fillna(0).astype(int)
    df['isbestseller'] = df['isbestseller'].astype(str).str.lower().isin(['true', '1', 'yes'])

    return df


def parse_product_text(row) -> str:
    """Build a descriptive text string for each product row."""
    text = f"Product: {row['title']} | Category: {row['category_id']} | "
    text += f"Price: ${row['price']:.2f} | Stars: {row['stars']} from {row['reviews']} reviews | "
    if row['isbestseller']:
        text += "🔥 Best Seller! | "
    if row['boughtinlastmonth'] > 0:
        text += f"Bought {row['boughtinlastmonth']} times last month |"
    return text.strip()




