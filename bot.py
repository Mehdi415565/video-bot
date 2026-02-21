import logging
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Menga video link tashlang 🎥")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text
    await message.reply("⏳ Yuklanmoqda...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await message.reply_video(open(file, 'rb'))
                os.remove(file)
                break

    except:
        await message.reply("❌ Xatolik yuz berdi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)