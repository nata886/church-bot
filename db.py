from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean

from config import DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    full_name = Column(String)


class CleaningDate(Base):
    __tablename__ = "cleaning_dates"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    date = Column(Date)
    confirmed = Column(Boolean, default=False)


class MonthStatus(Base):
    __tablename__ = "months"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    month = Column(String)
    closed = Column(Boolean, default=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)