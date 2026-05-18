import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "sample" / "top_100_risky_accounts_explained.csv"


def load_risk_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Risk veri dosyası bulunamadı: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    return df


def make_json_safe(df):
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")


def get_top_risky_accounts(limit: int = 20):
    df = load_risk_data()

    if "risk_score" in df.columns:
        df = df.sort_values("risk_score", ascending=False)

    df = df.head(limit)

    return make_json_safe(df)


def get_account_risk(account_number: str):
    df = load_risk_data()

    account_rows = df[df["account_number"].astype(str) == str(account_number)]

    if account_rows.empty:
        return None

    return make_json_safe(account_rows.head(1))[0]