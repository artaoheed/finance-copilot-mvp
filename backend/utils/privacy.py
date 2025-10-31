# backend/utils/privacy.py
import re
import pandas as pd

def sanitize_text(text: str) -> str:
    """Mask emails, long numbers, and truncate long strings."""
    if not isinstance(text, str):
        return text
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL]", text)
    text = re.sub(r'\d{10,}', "[NUM]", text)
    if len(text) > 60:
        text = text[:57] + "..."
    return text

def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sanitization to description-like columns."""
    df = df.copy()
    for col in df.columns:
        if any(word in col.lower() for word in ["description", "note", "memo", "remarks"]):
            df[col] = df[col].apply(sanitize_text)
    return df
