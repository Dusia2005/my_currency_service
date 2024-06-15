from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CurrencyRate(Base):
    __tablename__ = 'currency_rates'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    currency_code = Column(String, index=True)
    rate = Column(Float)
