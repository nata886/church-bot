from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy import select
from db import async_session, CleaningDate
from aiogram import Bot
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
scheduler = AsyncIOScheduler()


async def reminder():
    tomorrow = datetime.now().date() + timedelta(days=1)

    async with async_session() as session:
        result = await session.execute(
            select(CleaningDate).where(
                CleaningDate.date == tomorrow,
                CleaningDate.confirmed == True
            )
        )
        dates = result.scalars().all()

        for d in dates:
            await bot.send_message(
                d.telegram_id,
                "Напоминание: завтра ваша уборка."
            )


def start_scheduler():
    scheduler.add_job(reminder, "cron", hour=10)
    scheduler.start()