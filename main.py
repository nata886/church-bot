import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_URL
from db import init_db
from handlers import router
from scheduler import start_scheduler

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def on_startup(app):
    await init_db()
    start_scheduler()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    await bot.delete_webhook()


def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path="/webhook")

    setup_application(app, dp, bot=bot)

    web.run_app(app, port=8000)


if __name__ == "__main__":
    main()