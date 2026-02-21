import asyncio
import logging
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Menga video link tashlang 🎥")


@dp.message()
async def download_video(message: Message):
    url = message.text
    await message.answer("⏳ Yuklanmoqda...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await message.answer_video(types.FSInputFile(file))
                os.remove(file)
                break

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
