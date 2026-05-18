from fastapi import APIRouter, HTTPException

from app.services.risk_service import (
    get_top_risky_accounts,
    get_account_risk
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