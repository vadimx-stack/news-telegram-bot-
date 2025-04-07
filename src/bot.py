import os
import sys
from dotenv import load_dotenv
from loguru import logger
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from src.handlers.commands import start_command, news_command, latest_command, callback_handler
from src.utils.logger import setup_logger


def main() -> None:
    """Основная функция запуска бота."""
    # Загрузка переменных окружения
    load_dotenv()
    
    # Настройка логгера
    setup_logger()
    
    # Проверка наличия токена
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Не найден токен Telegram бота. Добавьте TELEGRAM_BOT_TOKEN в файл .env")
        sys.exit(1)
    
    # Проверка наличия ключа NewsAPI
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        logger.error("Не найден ключ News API. Добавьте NEWS_API_KEY в файл .env")
        sys.exit(1)
    
    # Создание директорий для логов и базы данных
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Инициализация бота
    logger.info("Инициализация бота NewsPulseBot")
    application = Application.builder().token(token).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("latest", latest_command))
    
    # Регистрация обработчика callback-запросов
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Запуск бота
    logger.info("Запуск бота NewsPulseBot")
    application.run_polling()
    
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {str(e)}")
        sys.exit(1) 