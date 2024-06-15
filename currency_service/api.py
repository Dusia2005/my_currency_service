from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from currency_service.utils import fetch_currency_rates, fetch_currency_rate_by_code, save_currency_rates, get_currency_rate
from currency_service.database import init_db, SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/currency_rates")
def currency_rates(date: str, db: Session = Depends(get_db)):
    rates = fetch_currency_rates(date)
    if rates:
        save_currency_rates(db, rates, date)
        return {"message": "Data loaded successfully"}
    raise HTTPException(status_code=404, detail="Data not found")


@router.get("/currency_rate")
def currency_rate(date: str, code: str, db: Session = Depends(get_db)):
    rate = get_currency_rate(db, date, code)
    if rate:
        return {
            "date": rate.date,
            "currency_code": rate.currency_code,
            "rate": rate.rate
        }
    raise HTTPException(status_code=404, detail="Data not found")
