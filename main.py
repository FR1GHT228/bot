import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from app.database.requests import Database
from app.handlers import router
import portalocker
import sys

load_dotenv()

LOCK_FILE = "E:/PythonProjects/pythonProject4/app/bot.lock"  # Путь к файлу блокировки


async def main():
    token = os.getenv('TOKEN_ID')
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    db = Database()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    await db.create_db()


def acquire_lock():
    lock_file = open(LOCK_FILE, "w")
    try:
        portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    except portalocker.LockException:
        print("Bot is already running.")
        sys.exit(1)
    return lock_file


if __name__ == "__main__":
    lock_file = acquire_lock()

    try:
        # Ваш код бота здесь
        print("Bot is running...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot off')
    finally:
        portalocker.unlock(lock_file)
        lock_file.close()

# if __name__ == '__main__':
#    try:
#        asyncio.run(main())
#    except KeyboardInterrupt:
#        print('Bot off')
