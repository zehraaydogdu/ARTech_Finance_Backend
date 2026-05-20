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
def get_dashboard_stats():
    df = load_risk_data()

    total = len(df)
    high_risk = df[df["risk_level"] == "high"] if "risk_level" in df.columns else pd.DataFrame()
    suspicious = len(high_risk)
    avg_score = round(df["risk_score"].mean(), 1) if "risk_score" in df.columns else 0
    high_risk_accounts = len(df[df["risk_score"] >= 80]) if "risk_score" in df.columns else 0
    total_volume = round(df["total_sent"].sum(), 2) if "total_sent" in df.columns else 0

    return {
        "total_transactions": total,
        "suspicious_transactions": suspicious,
        "average_risk_score": avg_score,
        "high_risk_accounts": high_risk_accounts,
        "total_volume": total_volume,
    }


def get_risk_distribution():
    df = load_risk_data()

    if "risk_level" not in df.columns:
        return []

    total = len(df)
    counts = df["risk_level"].value_counts()

    result = []
    colors = {"low": "#22c55e", "medium": "#f59e0b", "high": "#ef4444"}
    labels = {"low": "Düşük", "medium": "Orta", "high": "Yüksek"}

    for level, count in counts.items():
        result.append({
            "level": labels.get(level, level),
            "count": int(count),
            "percentage": round((count / total) * 100, 1),
            "color": colors.get(level, "#gray"),
        })

    return result


def get_suspicious_trend():
    df = load_risk_data()

    if "risk_level" not in df.columns:
        return []

    suspicious = df[df["risk_level"] == "high"]
    total_count = len(df)
    suspicious_count = len(suspicious)

    from datetime import datetime, timedelta
    today = datetime.today()

    result = []
    for i in range(14):
        date = today - timedelta(days=13 - i)
        result.append({
            "date": date.strftime("%d %b"),
            "count": suspicious_count // 14,
            "total": total_count // 14,
        })

    return result