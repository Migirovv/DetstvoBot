import asyncio
import logging

from aiogram import Dispatcher
from app.handlers import router

from app.handlers import bot


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
