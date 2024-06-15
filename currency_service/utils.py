import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import CurrencyRate


def fetch_currency_rates(date: str):
    url = f'https://www.nbrb.by/api/exrates/rates?ondate={date}&periodicity=0'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def fetch_currency_rate_by_code(date: str, code: str):
    url = f'https://www.nbrb.by/api/exrates/rates/{code}?ondate={date}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def save_currency_rates(db: Session, rates: list, date: str):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    # Удаляем старые данные за указанную дату
    db.query(CurrencyRate).filter(CurrencyRate.date == date_obj).delete()

    for rate in rates:
        currency_rate = CurrencyRate(
            date=date_obj,
            currency_code=rate['Cur_Abbreviation'],
            rate=rate['Cur_OfficialRate']
        )
        db.add(currency_rate)
    db.commit()


def get_previous_working_day(date: datetime):
    prev_day = date - timedelta(days=1)
    while prev_day.weekday() >= 5:  # 5 и 6 соответствуют субботе и воскресенью
        prev_day -= timedelta(days=1)
    return prev_day


def get_currency_rate(db: Session, date: str, code: str):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    return db.query(CurrencyRate).filter(
        CurrencyRate.date == date_obj,
        CurrencyRate.currency_code == code
    ).first()


def get_previous_day_rate(db: Session, date: str, code: str):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    prev_day = get_previous_working_day(date_obj)
    return db.query(CurrencyRate).filter(
        CurrencyRate.date == prev_day,
        CurrencyRate.currency_code == code
    ).first()
