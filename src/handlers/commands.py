from typing import Dict, List, Optional, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from loguru import logger

from src.database.db import Database
from src.utils.news_api import NewsAPIClient, Article


# Доступные категории новостей
CATEGORIES = {
    "business": "Бизнес",
    "entertainment": "Развлечения",
    "health": "Здоровье",
    "science": "Наука",
    "sports": "Спорт",
    "technology": "Технологии"
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}) запустил бота")
    
    # Сохраняем пользователя в базу данных
    db = Database()
    await db.add_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        last_name=user.last_name or ""
    )
    
    # Создаем клавиатуру с категориями новостей
    keyboard = [
        [
            InlineKeyboardButton("Последние новости", callback_data="news_latest"),
            InlineKeyboardButton("Выбрать категорию", callback_data="select_category")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я NewsPulseBot — ваш персональный помощник для получения последних новостей.\n\n"
        "Доступные команды:\n"
        "/start — начать работу с ботом\n"
        "/news — получить последние новости\n"
        "/latest [категория] — получить новости по категории\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /news."""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запросил последние новости")
    
    # Сохраняем последнюю команду
    db = Database()
    await db.update_user_preference(user_id=user.id, last_command="/news")
    
    # Получаем предпочитаемую категорию пользователя
    user_prefs = await db.get_user_preferences(user.id)
    favorite_category = user_prefs.get("favorite_category") if user_prefs else None
    
    await update.message.reply_text("🔍 Ищу последние новости...")
    
    news_api = NewsAPIClient()
    try:
        if favorite_category:
            articles = await news_api.get_top_headlines(category=favorite_category)
            category_name = CATEGORIES.get(favorite_category, favorite_category)
            intro_text = f"📰 Последние новости из категории '{category_name}':\n\n"
        else:
            articles = await news_api.get_top_headlines()
            intro_text = "📰 Последние главные новости:\n\n"
        
        await send_articles(update, articles, intro_text)
    except Exception as e:
        logger.error(f"Ошибка при получении новостей: {str(e)}")
        await update.message.reply_text(
            "😔 Произошла ошибка при получении новостей. Пожалуйста, попробуйте позже."
        )


async def latest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /latest [категория]."""
    user = update.effective_user
    
    # Получаем категорию из аргументов команды
    args = context.args
    category = args[0].lower() if args else None
    
    # Проверяем, что категория допустима
    if category and category not in CATEGORIES:
        categories_text = ", ".join([f"{k} ({v})" for k, v in CATEGORIES.items()])
        await update.message.reply_text(
            f"❌ Указана неверная категория.\n\n"
            f"Доступные категории: {categories_text}\n\n"
            f"Пример: /latest technology"
        )
        return
    
    logger.info(f"Пользователь {user.id} запросил новости по категории: {category}")
    
    # Сохраняем последнюю команду и категорию
    db = Database()
    await db.update_user_preference(
        user_id=user.id, 
        last_command=f"/latest {category}" if category else "/latest",
        favorite_category=category
    )
    
    await update.message.reply_text(f"🔍 Ищу последние новости{f' по категории {CATEGORIES.get(category, category)}' if category else ''}...")
    
    news_api = NewsAPIClient()
    try:
        articles = await news_api.get_top_headlines(category=category)
        
        if category:
            category_name = CATEGORIES.get(category, category)
            intro_text = f"📰 Последние новости из категории '{category_name}':\n\n"
        else:
            intro_text = "📰 Последние главные новости:\n\n"
        
        await send_articles(update, articles, intro_text)
    except Exception as e:
        logger.error(f"Ошибка при получении новостей: {str(e)}")
        await update.message.reply_text(
            "😔 Произошла ошибка при получении новостей. Пожалуйста, попробуйте позже."
        )


async def send_articles(update: Update, articles: List[Article], intro_text: str) -> None:
    """Отправка списка статей пользователю.
    
    Args:
        update: Объект обновления Telegram
        articles: Список статей для отправки
        intro_text: Вводный текст перед списком статей
    """
    if not articles:
        await update.message.reply_text("😔 Новости не найдены.")
        return
    
    message_text = intro_text
    
    for i, article in enumerate(articles, 1):
        message_text += (
            f"{i}. [{article.title}]({article.url})\n"
            f"   🗞️ {article.source}\n"
            f"   📝 {article.description[:100] + '...' if article.description and len(article.description) > 100 else article.description or 'Описание отсутствует'}\n\n"
        )
    
    # Добавляем кнопки для действий
    keyboard = [
        [
            InlineKeyboardButton("Обновить", callback_data="refresh_news"),
            InlineKeyboardButton("Выбрать категорию", callback_data="select_category")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик callback запросов от инлайн-кнопок."""
    query = update.callback_query
    user = query.from_user
    
    await query.answer()
    
    if query.data == "news_latest":
        # Эмулируем команду /news
        context.args = []
        await news_command(update, context)
    
    elif query.data == "select_category":
        # Отображаем меню выбора категории
        keyboard = []
        row = []
        
        for i, (category_key, category_name) in enumerate(CATEGORIES.items(), 1):
            row.append(InlineKeyboardButton(
                category_name, callback_data=f"category_{category_key}"
            ))
            
            # По 2 кнопки в ряд
            if i % 2 == 0 or i == len(CATEGORIES):
                keyboard.append(row)
                row = []
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="Выберите категорию новостей:",
            reply_markup=reply_markup
        )
    
    elif query.data.startswith("category_"):
        category = query.data.split("_")[1]
        
        # Сохраняем выбранную категорию
        db = Database()
        await db.update_user_preference(
            user_id=user.id,
            favorite_category=category
        )
        
        # Эмулируем команду /latest с выбранной категорией
        context.args = [category]
        await latest_command(update, context)
    
    elif query.data == "refresh_news":
        # Получаем последнюю выполненную команду
        db = Database()
        user_prefs = await db.get_user_preferences(user.id)
        last_command = user_prefs.get("last_command") if user_prefs else "/news"
        
        # Выполняем соответствующую команду
        if last_command.startswith("/latest "):
            category = last_command.split(" ")[1]
            context.args = [category]
            await latest_command(update, context)
        else:
            context.args = []
            await news_command(update, context) 