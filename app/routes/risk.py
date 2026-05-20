from fastapi import APIRouter, HTTPException

from app.services.risk_service import (
    get_top_risky_accounts,
    get_account_risk,
    get_dashboard_stats,
    get_risk_distribution,
    get_suspicious_trend
)

router = APIRouter()


@router.get("/top")
def top_risky_accounts(limit: int = 20):
    return {
        "limit": limit,
        "accounts": get_top_risky_accounts(limit)
    }


@router.get("/account/{account_number}")
def account_risk_detail(account_number: str):
    account = get_account_risk(account_number)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Bu hesap numarası için risk kaydı bulunamadı."
        )

    return account


@router.get("/dashboard/stats")
def dashboard_stats():
    return get_dashboard_stats()


@router.get("/dashboard/risk-distribution")
def risk_distribution():
    return get_risk_distribution()


@router.get("/dashboard/suspicious-trend")
def suspicious_trend():
    return get_suspicious_trend()