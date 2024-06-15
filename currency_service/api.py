from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .utils import fetch_currency_rates, save_currency_rates, get_currency_rate, get_previous_day_rate
from .database import SessionLocal

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
        return {"message": "Данные успешно загружены", "data": rates}
    raise HTTPException(status_code=404, detail="Данные не найдены")

@router.get("/currency_rate")
def currency_rate(date: str, code: str, db: Session = Depends(get_db)):
    rate = get_currency_rate(db, date, code)
    if rate:
        prev_rate = get_previous_day_rate(db, date, code)
        if prev_rate:
            change = rate.rate - prev_rate.rate
            change_status = "вырос" if change > 0 else "уменьшился" if change < 0 else "не изменился"
            return {
                "date": rate.date,
                "currency_code": rate.currency_code,
                "rate": rate.rate,
                "previous_rate": prev_rate.rate,
                "change": change,
                "change_status": change_status
            }
        return {
            "date": rate.date,
            "currency_code": rate.currency_code,
            "rate": rate.rate,
            "previous_rate": None,
            "change": None,
            "change_status": "нет данных за предыдущий рабочий день"
        }
    raise HTTPException(status_code=404, detail="Данные не найдены")
