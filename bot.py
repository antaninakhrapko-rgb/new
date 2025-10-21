import feedparser
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token="8210782460:AAHK6dInuvZduJ_vtfYZT01qgNkN6CrPNEE",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# 🔗 Город → ключевые слова
city_keywords = {
    "минск": ["минск", "минская"],
    "могилёв": ["могилёв", "могилевская", "бобруйск"],
    "витебск": ["витебск", "витебская", "полоцк", "новополоцк"],
    "гомель": ["гомель", "гомельская", "жлобин"],
    "брест": ["брест", "брестская", "пинск", "барановичи"],
    "гродно": ["гродно", "гродненская", "лида"]
}

# 📡 RSS-ленты
rss_feeds = [
    "https://mlyn.by/feed/",
    "https://minsknews.by/feed/",
    "https://mogilevnews.by/feed/",
    "https://vitvesti.by/feed/",
    "https://www.belta.by/rss/all"
]

# 🧠 Классификация по типу
def classify(entry):
    title = entry.title.lower()
    if any(word in title for word in ["эконом", "бизнес", "рынок"]):
        return "экономика"
    elif any(word in title for word in ["пожар", "взрыв", "спасател", "чрезвычайн"]):
        return "чрезвычайные"
    elif any(word in title for word in ["дтп", "авария", "столкнов"]):
        return "дтп"
    else:
        return "другое"

# 📰 Получение и фильтрация новостей
def get_news_by_city(city):
    city = city.lower()
    keywords = city_keywords.get(city, [city])
    blocks = {"экономика": [], "чрезвычайные": [], "дтп": [], "другое": []}

    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.lower()
            if any(key in title for key in keywords):
                category = classify(entry)
                blocks[category].append(f"🗞 <b>{entry.title}</b>\n{entry.link}")
            if sum(len(v) for v in blocks.values()) >= 5:
                break

    result = []
    for key in ["экономика", "чрезвычайные", "дтп", "другое"]:
        if blocks[key]:
            result.append(f"📌 <b>{key.capitalize()}</b>\n" + "\n\n".join(blocks[key][:2]))
    return "\n\n".join(result) if result else "📰 Нет свежих новостей по вашему региону."

# 👋 Приветствие
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("👋 Привет! Я покажу свежие новости по Беларуси, связанные с вашим городом.\n\n📍 Напиши название города (например, Минск, Бобруйск, Витебск).")

# 🏙 Обработка города
@dp.message(F.text)
async def handle_city_text(message: Message):
    city = message.text.strip()
    news = get_news_by_city(city)
    await message.answer(f"📍 Город: <b>{city}</b>\n\n{news}")

# 🚀 Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())







