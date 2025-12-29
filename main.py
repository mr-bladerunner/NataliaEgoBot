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

BOT_TOKEN = os.getenv("BOT_TOKEN")
TZ = os.getenv("TZ", "Europe/Zurich")
MODE = os.getenv("MODE", "dev").lower()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Provide it via environment variable.")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Dienstleistungen")],
        [KeyboardButton(text="💼 Preise & Bewertungen")],
        [KeyboardButton(text="🧭 Ablauf des Verkaufs")],
        [KeyboardButton(text="ℹ️ Ueber uns")],
        [KeyboardButton(text="📞 Kontakt")],
    ],
    resize_keyboard=True,
)

# Sub-keyboards for services flow
services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏡 Immobilie verkaufen"), KeyboardButton(text="💰 Immobilie bewerten lassen")],
        [KeyboardButton(text="🏘️ Immobilie vermieten"), KeyboardButton(text="💬 Kostenlose Beratung")],
        [KeyboardButton(text="🔙 Zurueck zum Hauptmenue")],
    ],
    resize_keyboard=True,
)

sell_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Kostenlose Erstberatung")],
        [KeyboardButton(text="🔙 Zurueck zu Dienstleistungen")],
    ],
    resize_keyboard=True,
)

valuation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Wohnung"), KeyboardButton(text="Einfamilienhaus")],
        [KeyboardButton(text="Gewerbeobjekt")],
        [KeyboardButton(text="🔙 Zurueck zu Dienstleistungen")],
    ],
    resize_keyboard=True,
)

rent_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Kontakt fuer Vermietung")],
        [KeyboardButton(text="🔙 Zurueck zu Dienstleistungen")],
    ],
    resize_keyboard=True,
)

# Preise & Bewertungen keyboards
prices_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Immobilienbewertung")],
        [KeyboardButton(text="🏡 Verkauf von Immobilien"), KeyboardButton(text="🏘️ Vermietung")],
        [KeyboardButton(text="📄 Mietvertragserstellung"),],
        [KeyboardButton(text="🔙 Zurueck zum Hauptmenue")],
    ],
    resize_keyboard=True,
)

valuation_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏢 Wohnung / Einfamilienhaus")],
        [KeyboardButton(text="🏬 Renditeobjekt")],
        [KeyboardButton(text="🏗️ Projektentwicklung")],
        [KeyboardButton(text="🏘️ Gemischtes Objekt")],
        [KeyboardButton(text="🔙 Zurueck")],
    ],
    resize_keyboard=True,
)

price_contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Kontakt")],
        [KeyboardButton(text="🔙 Zurueck")],
    ],
    resize_keyboard=True,
)

sale_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Kostenlose Einschaetzung anfordern")],
        [KeyboardButton(text="🔙 Zurueck")],
    ],
    resize_keyboard=True,
)

rent_options_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧾 Mietvertrag erstellen lassen (CHF 80)"), KeyboardButton(text="👥 Mieter finden")],
        [KeyboardButton(text="🔙 Zurueck")],
    ],
    resize_keyboard=True,
)

mietvertrag_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Ja, bitte")],
        [KeyboardButton(text="🔙 Zurueck")],
    ],
    resize_keyboard=True,
)

# Ablauf des Verkaufs (sales process) keyboard
ablauf_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Beratung vereinbaren")],
        [KeyboardButton(text="🔙 Zurueck zum Hauptmenue")],
    ],
    resize_keyboard=True,
)

# About us keyboard
about_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Kontakt")],
        [KeyboardButton(text="🔙 Zurueck zum Hauptmenue")],
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
            caption=(
                "Willkommen!\n"
                "Ich bin Ihr virtueller Assistent fuer Immobilienfragen in der Schweiz.\n"
                "Ob Verkauf, Bewertung oder Vermietung – wir begleiten Sie kompetent und transparent.\n"
                "Bitte waehlen Sie unten:"
            ),
            reply_markup=kb,
        )
    else:
        # Резерв: если фото нет — просто текст с клавиатурой
        await m.answer(
            "Willkommen!\n"
            "Ich bin Ihr virtueller Assistent fuer Immobilienfragen in der Schweiz.\n"
            "Ob Verkauf, Bewertung oder Vermietung – wir begleiten Sie kompetent und transparent.\n"
            "Bitte waehlen Sie unten:",
            reply_markup=kb,
        )

@dp.message(F.text == "ℹ️ Ueber uns")
async def about_me(m: Message):
    photo_path = "assets/profile_picture.jpg"
    
    if os.path.isfile(photo_path):
        photo = FSInputFile(photo_path)
        caption = (
            "Erfahrung, Transparenz, Diskretion.\n"
            "Ihre Immobilie ist in zuverlaessigen Haenden – von der Bewertung bis zur Schluesseluebergabe.\n\n"
            "Moechten Sie direkt Kontakt aufnehmen?"
        )
        await m.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="Markdown",  # ← включаем обработку звёздочек
            reply_markup=about_kb,
        )
    else:
        await m.answer(
            "Erfahrung, Transparenz, Diskretion.\n"
            "Ihre Immobilie ist in zuverlaessigen Haenden – von der Bewertung bis zur Schluesseluebergabe.\n\n"
            "Moechten Sie direkt Kontakt aufnehmen?",
            reply_markup=about_kb,
        )


@dp.message(F.text == "🏠 Dienstleistungen")
async def services_menu(m: Message):
    text = (
        "Unsere Hauptdienstleistungen:\n"
        "- Immobilienbewertung\n"
        "- Verkauf und Vermietung von Liegenschaften\n"
        "- Projektvorschlaege und Nutzungsoptimierung\n"
        "- Unterstuetzung bei Renovationen und Umbauten\n\n"
        "Welche Dienstleistung interessiert Sie?"
    )
    await m.answer(text, reply_markup=services_kb)
    

@dp.message(F.text == "🧭 Ablauf des Verkaufs")
async def sale_process(m: Message):
    text = (
        "So laeuft ein professioneller Immobilienverkauf ab:\n"
        "1) Unverbindliche Erstberatung\n"
        "2) Bewertung und Offerte\n"
        "3) Marketing und Fotos\n"
        "4) Inserate\n"
        "5) Besichtigungen\n"
        "6) Notar\n"
        "7) Uebergabe\n\n"
        "Moechten Sie eine Beratung vereinbaren?"
    )
    await m.answer(text, reply_markup=ablauf_kb)


@dp.message(F.text == "📅 Beratung vereinbaren")
async def schedule_consult(m: Message):
    await m.answer("Danke — wir verbinden Sie mit unseren Kontaktdaten.", reply_markup=kb)
    await contacts(m)
    

@dp.message(F.text == "💼 Preise & Bewertungen")
async def price_list(m: Message):
    # Interactive prices menu
    await m.answer(
        "Bitte waehlen Sie den Bereich, der Sie interessiert:",
        reply_markup=prices_kb,
    )


@dp.message(F.text == "💰 Immobilienbewertung")
async def prices_valuation(m: Message):
    await m.answer("Bitte waehlen Sie den Objekttyp:", reply_markup=valuation_type_kb)


@dp.message(F.text == "🏢 Wohnung / Einfamilienhaus")
async def price_apartment_house(m: Message):
    await m.answer(
        "Preis: ab CHF 390. Inklusive Marktanalyse und Vergleichswerte.",
        reply_markup=price_contact_kb,
    )


@dp.message(F.text == "🏬 Renditeobjekt")
async def price_rendite(m: Message):
    await m.answer(
        "Preis: ab CHF 680. Inklusive Ertragswert.",
        reply_markup=price_contact_kb,
    )


@dp.message(F.text == "🏗️ Projektentwicklung")
async def price_project(m: Message):
    await m.answer(
        "Preis: ab CHF 980.",
        reply_markup=price_contact_kb,
    )


@dp.message(F.text == "🏘️ Gemischtes Objekt")
async def price_mixed(m: Message):
    await m.answer(
        "Preis: ab CHF 870.",
        reply_markup=price_contact_kb,
    )


@dp.message(F.text == "🏡 Verkauf von Immobilien")
async def prices_sale(m: Message):
    await m.answer(
        "Provision 2-3 Prozent, je nach Lage, Objekt und Aufwand. Beratung ist kostenlos.\nMoechten Sie eine unverbindliche Einschaetzung?",
        reply_markup=sale_kb,
    )


@dp.message(F.text == "💬 Kostenlose Einschaetzung anfordern")
async def sale_request(m: Message):
    await m.answer("Vielen Dank — wir werden uns fuer die Einschaetzung melden.", reply_markup=kb)
    await contacts(m)


@dp.message(F.text == "🏘️ Vermietung")
async def prices_rent(m: Message):
    await m.answer(
        "Gebuehr fuer Vermietung: 1 Monatsmiete. Optional: Mietvertragserstellung CHF 80.\nWas moechten Sie tun?",
        reply_markup=rent_options_kb,
    )


@dp.message(F.text == "🧾 Mietvertrag erstellen lassen (CHF 80)")
async def rent_mietvertrag(m: Message):
    await m.answer("Mietvertragserstellung: CHF 80. Moechten Sie starten?", reply_markup=mietvertrag_kb)


@dp.message(F.text == "👥 Mieter finden")
async def rent_find_tenant(m: Message):
    await m.answer("Wir helfen Ihnen beim Finden von Mietern — bitte kontaktieren Sie uns.", reply_markup=kb)
    await contacts(m)


@dp.message(F.text == "📄 Mietvertragserstellung")
async def prices_mietvertrag(m: Message):
    await m.answer("Mietvertragserstellung: CHF 80. Moechten Sie starten?", reply_markup=mietvertrag_kb)


@dp.message(F.text == "✅ Ja, bitte")
async def mietvertrag_confirm(m: Message):
    await m.answer("Vielen Dank — wir werden uns wegen der Mietvertragserstellung bei Ihnen melden.", reply_markup=kb)
    await contacts(m)


@dp.message(F.text == "🔙 Zurueck")
async def prices_back(m: Message):
    await price_list(m)

@dp.message(F.text == "📞 Kontakt")
async def contacts(m: Message):
    text = (
        "📞 *Kontaktdatei:*\n\n"
        "👤 *Name:* Real Estate Egorova Marguglio  \n"
        "📧 *Email:* info@immo17.ch  \n"
        "📱 *Telefon:* +41 76 542 72 88"
    )
    await m.answer(text, parse_mode="Markdown")


@dp.message(F.text == "Kostenlose Erstberatung")
async def free_first_consult(m: Message):
    # Redirect to contact form / contact info
    await m.answer("Moechten Sie eine kostenlose Erstberatung? Hier unsere Kontaktinformationen:", reply_markup=kb)
    await contacts(m)


@dp.message(F.text == "🏡 Immobilie verkaufen")
async def sell_property(m: Message):
    text = (
        "Provision: In der Regel 2-3% des Verkaufspreises.\n"
        "Kostenlose Erstberatung?"
    )
    await m.answer(text, reply_markup=sell_kb)


@dp.message(F.text == "💰 Immobilie bewerten lassen")
async def valuation_start(m: Message):
    await m.answer("Zu welchem Objekttyp möchten Sie eine Bewertung?", reply_markup=valuation_kb)


@dp.message(F.text == "🏘️ Immobilie vermieten")
async def rent_property(m: Message):
    text = (
        "Gebuehr: 1 Monatsmiete. Optional: Mietvertrag CHF 80.\n"
        "Moechten Sie ein Angebot oder eine Kontaktaufnahme?"
    )
    await m.answer(text, reply_markup=rent_kb)


@dp.message(F.text == "💬 Kostenlose Beratung")
async def free_consult(m: Message):
    await m.answer("Sie werden zur Kontaktaufnahme weitergeleitet.", reply_markup=kb)
    await contacts(m)


@dp.message(F.text == "🔙 Zurueck zum Hauptmenue")
async def back_to_main(m: Message):
    await m.answer("Zurueck zum Hauptmenue.", reply_markup=kb)


@dp.message(F.text == "🔙 Zurueck zu Dienstleistungen")
async def back_to_services(m: Message):
    await services_menu(m)


@dp.message(F.text == "Kontakt fuer Vermietung")
async def contact_rent(m: Message):
    await contacts(m)


@dp.message(F.text == "Wohnung")
async def valuation_apartment(m: Message):
    await m.answer("Sie haben 'Wohnung' ausgewaehlt. Bitte kontaktieren Sie uns fuer ein genaues Angebot.", reply_markup=kb)


@dp.message(F.text == "Einfamilienhaus")
async def valuation_house(m: Message):
    await m.answer("Sie haben 'Einfamilienhaus' ausgewaehlt. Bitte kontaktieren Sie uns fuer ein genaues Angebot.", reply_markup=kb)


@dp.message(F.text == "Gewerbeobjekt")
async def valuation_commercial(m: Message):
    await m.answer("Sie haben 'Gewerbeobjekt' ausgewaehlt. Bitte kontaktieren Sie uns fuer ein genaues Angebot.", reply_markup=kb)


from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your_strong_secret_here")
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL", "https://your-bot.onrender.com")

# MODE is defined above near the configuration section

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET
    )

async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()

def run_webhook() -> None:
    app = web.Application()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

async def run_polling():
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if MODE == "prod":
        run_webhook()
    else:
        asyncio.run(run_polling())
