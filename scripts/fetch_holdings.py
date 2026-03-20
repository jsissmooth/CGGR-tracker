import requests
import pandas as pd
import pandas_market_calendars as mcal
import json
import os
import sys
from datetime import date, timedelta
from io import BytesIO

DOWNLOAD_URL = (
    "https://www.capitalgroup.com/api/investments/investment-service/v1/etfs/cggr"
    "/download/daily-holdings?audience=advisor&redirect=true"
)
SHEET_NAME = "Daily Fund Holdings"
HEADER_ROW = 2  # 0-indexed, so row 3 in Excel

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# ── helpers ────────────────────────────────────────────────────────────────────

def download_file() -> bytes:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
        "Referer": "https://www.capitalgroup.com/",
    }
    resp = requests.get(DOWNLOAD_URL, headers=headers, allow_redirects=True, timeout=30)
    resp.raise_for_status()
    return resp.content


def find_column(columns, *keywords):
    """Case-insensitive partial match for a column header."""
    for col in columns:
        col_lower = str(col).lower()
        if any(kw.lower() in col_lower for kw in keywords):
            return col
    return None


def parse_holdings(content: bytes) -> list
