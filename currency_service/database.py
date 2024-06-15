from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    currency_code = Column(String, index=True)
    rate = Column(Float)


DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)



