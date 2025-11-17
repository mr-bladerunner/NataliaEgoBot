import asyncio
import os

from typing import Dict, List
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    FSInputFile,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

# --- конфиг ---
from dotenv import load_dotenv
load_dotenv()
print("DEBUG BOT_TOKEN =", os.getenv("BOT_TOKEN"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
TZ = os.getenv("TZ", "Europe/Zurich")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Provide it via environment variable.")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Über mich")],
        [KeyboardButton(text="Dienstleistungen")],
        [KeyboardButton(text="Preisliste Dienstleistungen")],
        [KeyboardButton(text="Kontakt")],
        [KeyboardButton(text="Abonnieren")],
    ],
    resize_keyboard=True,
)


# --- временное хранилище на демо (в проде заменить на Postgres) ---
USERS: Dict[int, Dict] = {}  


# ----------------- Хендлеры -----------------
@dp.message(Command("start"))
async def cmd_start(m: Message):
    USERS[m.chat.id] = {"active": True}
    
    photo_path = "assets/preview.jpg"  # или banner.jpg — как ты хочешь
    
    if os.path.isfile(photo_path):
        photo = FSInputFile(photo_path)
        await m.answer_photo(
            photo=photo,
            caption="Guten Tag, ich bin Ihr virtueller Assistent für Immobilienfragen.",
            reply_markup=kb,
        )
    else:
        # Резерв: если фото нет — просто текст с клавиатурой
        await m.answer(
            "Guten Tag, ich bin Ihr virtueller Assistent für Immobilienfragen.",
            reply_markup=kb,
        )

@dp.message(F.text == "Über mich")
async def about_me(m: Message):
    photo_path = "assets/profile__picture.jpg"
    
    if os.path.isfile(photo_path):
        photo = FSInputFile(photo_path)
        caption = (
            "Guten Tag,\n"
            "ich bin Ihr virtueller Assistent für Immobilienfragen.\n\n"
            "Als Immobilienexperte stehe ich Ihnen gerne mit folgenden Dienstleistungen zur Verfügung:\n\n"
            "• *Immobilienbewertung*\n"
            "• *Immobilienvermarktung*\n"
            "• *Vermietung*\n"
            "• *Verkauf von Liegenschaften*\n\n"
            "Ich freue mich darauf, Sie kompetent und zuverlässig zu unterstützen."
        )
        await m.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="Markdown"  # ← включаем обработку звёздочек
        )
    else:
        await m.answer("Guten Tag! [Profilbild nicht gefunden]")


@dp.message(F.text == "Dienstleistungen")
async def about(m: Message):
    photo_path = "assets/leistungen.jpg"  # ← укажите имя вашего файла
    if os.path.isfile(photo_path):
        photo = FSInputFile(photo_path)
        await m.answer_photo(photo=photo)
    else:
        await m.answer("Dienstleistungen-Bild nicht gefunden.")
    

@dp.message(F.text == "Preisliste Dienstleistungen")
async def price_list(m: Message):
    photo_path = "assets/preisliste.jpg"
    if os.path.isfile(photo_path):
        photo = FSInputFile(photo_path)
        await m.answer_photo(photo=photo)
    else:
        await m.answer("Preisliste-Bild nicht gefunden.")

@dp.message(F.text == "Kontakt")
async def contacts(m: Message):
    text = (
        "📞 *Kontaktdatei:*\n\n"
        "👤 *Name:* Real Estate Egorova Marguglio  \n"
        "📧 *Email:* info@immo17.ch  \n"
        "📱 *Telefon:* +41 76 542 72 88"
    )
    await m.answer(text, parse_mode="Markdown")


@dp.message(F.text == "Abonnieren")
async def subscribe(m: Message):
    USERS[m.chat.id] = {"active": True}
    await m.answer("Sie sind jetzt für Updates angemeldet!")



# ----------------- Точка входа (Webhook-версия) -----------------
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Настройки webhook
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your_strong_secret_here")
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL", "https://your-bot.onrender.com")

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET
    )

def main() -> None:
    # Создаём aiohttp-приложение
    app = web.Application()
    
    # Регистрируем webhook-обработчик
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Подключаем aiogram к aiohttp
    setup_application(app, dp, bot=bot)
    
    # Запуск сервера
    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()