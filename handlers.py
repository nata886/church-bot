from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy import select
from datetime import datetime

from db import async_session, User, CleaningDate, MonthStatus
from keyboards import main_menu
from config import ADMIN_ID

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar()

        if not user:
            new_user = User(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name
            )
            session.add(new_user)
            await session.commit()

    await message.answer("Меню:", reply_markup=main_menu())


@router.callback_query(F.data == "my_months")
async def my_months(call: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(MonthStatus).where(
                MonthStatus.telegram_id == call.from_user.id
            )
        )
        months = result.scalars().all()

        if not months:
            text = "Нет данных."
        else:
            text = "\n".join(
                f"{m.month} — {'Закрыт' if m.closed else 'Открыт'}"
                for m in months
            )

    await call.message.answer(text)


@router.callback_query(F.data == "my_date")
async def my_date(call: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(CleaningDate).where(
                CleaningDate.telegram_id == call.from_user.id,
                CleaningDate.confirmed == True
            )
        )
        date = result.scalar()

        if date:
            text = f"Ваша дата: {date.date}"
        else:
            text = "Дата не назначена."

    await call.message.answer(text)