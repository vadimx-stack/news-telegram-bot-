# 📰 NewsPulseBot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-v6.7%2B-blue)
![NewsAPI](https://img.shields.io/badge/NewsAPI-Integrated-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

<div align="center">
  <a href="#overview">English</a> |
  <a href="#обзор">Русский</a>
</div>

---

## Overview

NewsPulseBot is a professional Telegram bot that provides users with up-to-date news from various categories using NewsAPI. The bot is developed using modern Python development approaches, including asynchronous programming, modular architecture, and user preferences storage.

![NewsPulseBot Demo](https://via.placeholder.com/800x450.png?text=NewsPulseBot+Demo)

## ✨ Key Features

- 🔄 **Real-time News Updates** - get the latest news from your selected category
- 🔍 **Category Support** - news sorted by categories (business, technology, sports, etc.)
- 💾 **Preferences Storage** - remembers preferred categories for each user
- 🛠 **Modular Architecture** - easily maintainable and extensible code
- 📊 **Comprehensive Logging** - detailed tracking of bot operations
- 🔐 **Secure Key Storage** - using environment variables for confidential data

## 🚀 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Begin working with the bot and receive a welcome message |
| `/news` | Get the latest news (considering user's preferred category) |
| `/latest [category]` | Get the latest news in the specified category |

## 🏗️ Project Architecture

```
NewsPulseBot/
│
├── src/                     # Source code
│   ├── handlers/            # Command and message handlers
│   │   ├── __init__.py
│   │   └── commands.py      # Bot command handlers
│   │
│   ├── utils/               # Utility modules
│   │   ├── __init__.py
│   │   ├── logger.py        # Logging configuration
│   │   └── news_api.py      # News API interaction
│   │
│   ├── database/            # Database operations
│   │   ├── __init__.py
│   │   └── db.py            # SQLite handler class
│   │
│   ├── __init__.py
│   └── bot.py               # Main bot module
│
├── data/                    # Data storage directory
│   └── newspulsebot.db      # SQLite database (created automatically)
│
├── logs/                    # Logs storage directory
│
├── .env.example             # Example environment variables file
├── .env                     # Environment variables file (not stored in repository)
├── requirements.txt         # Project dependencies
├── main.py                  # Entry point
└── README.md                # Project documentation
```

## 🛠️ Technology Stack

- **Python 3.9+**: Main programming language
- **python-telegram-bot 20.0+**: Library for Telegram Bot API
- **aiohttp**: Asynchronous HTTP client for API requests
- **SQLite**: Lightweight database for user data storage
- **NewsAPI**: API for news retrieval
- **python-dotenv**: Environment variables loader
- **loguru**: Advanced logging
- **pydantic**: Data validation

## 💻 Installation and Launch

1. **Clone the repository:**

```bash
git clone https://github.com/username/NewsPulseBot.git
cd NewsPulseBot
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Create and configure .env file:**

```bash
cp .env.example .env
# Edit .env file, adding your Telegram Bot token and NewsAPI key
```

4. **Run the bot:**

```bash
python main.py
```

## 📝 Environment Variables Configuration

Create a `.env` file in the project root with the following variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NEWS_API_KEY=your_news_api_key
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🧩 Usage Examples

### Getting Latest News

```
/news
```

Result:
```
📰 Latest headlines:

1. [News Headline 1](https://link-to-news1.com)
   🗞️ News Source
   📝 Brief news description...

2. [News Headline 2](https://link-to-news2.com)
   🗞️ News Source
   📝 Brief news description...
```

### Getting News by Category

```
/latest technology
```

Result:
```
📰 Latest news in 'Technology' category:

1. [Technology News Headline 1](https://link-to-tech-news1.com)
   🗞️ News Source
   📝 Brief technology news description...

2. [Technology News Headline 2](https://link-to-tech-news2.com)
   🗞️ News Source
   📝 Brief technology news description...
```

## 🔄 Future Development Prospects

- **Multilingual Support**: Add ability to receive news in different languages
- **Personalized Feed**: Algorithm for news selection based on user interests
- **Advanced Search**: Search for news by keywords and phrases
- **Notification Scheduler**: Setup for regular notifications about important news
- **Integration with Other Services**: Connect additional news sources
- **Usage Statistics**: Analytics for tracking popular categories and queries

## 📜 License

This project is distributed under the MIT license. Detailed information can be found in the LICENSE file.

## 📞 Contacts

- **Developer**: [Your Name](https://github.com/username)
- **Email**: your.email@example.com
- **Telegram**: [@your_telegram_username](https://t.me/your_telegram_username)

---

<div align="center">
  <sub>Created with ❤️ to showcase programming skills</sub>
</div>

---

## 📋 Обзор

NewsPulseBot - это профессиональный Telegram бот, который предоставляет пользователям актуальные новости из разных категорий с использованием NewsAPI. Бот разработан с применением современных подходов к разработке на Python, включая асинхронное программирование, модульную архитектуру и хранение пользовательских настроек.

![NewsPulseBot Demo](https://via.placeholder.com/800x450.png?text=NewsPulseBot+Demo)

## ✨ Ключевые особенности

- 🔄 **Актуальные новости в реальном времени** - получение последних новостей из выбранной категории
- 🔍 **Поддержка категорий** - новости разделены по категориям (бизнес, технологии, спорт и др.)
- 💾 **Сохранение предпочтений** - запоминание предпочитаемых категорий для каждого пользователя
- 🛠 **Модульная архитектура** - легко поддерживаемый и расширяемый код
- 📊 **Логирование всех действий** - детальное отслеживание работы бота
- 🔐 **Безопасное хранение ключей** - использование переменных окружения для конфиденциальных данных

## 🚀 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Начало работы с ботом и приветственное сообщение |
| `/news` | Получение последних новостей (с учетом предпочитаемой категории пользователя) |
| `/latest [категория]` | Получение последних новостей по указанной категории |

## 🏗️ Архитектура проекта

```
NewsPulseBot/
│
├── src/                     # Исходный код
│   ├── handlers/            # Обработчики команд и сообщений
│   │   ├── __init__.py
│   │   └── commands.py      # Обработчики команд бота
│   │
│   ├── utils/               # Вспомогательные модули
│   │   ├── __init__.py
│   │   ├── logger.py        # Настройка логирования
│   │   └── news_api.py      # Взаимодействие с News API
│   │
│   ├── database/            # Работа с базой данных
│   │   ├── __init__.py
│   │   └── db.py            # Класс для работы с SQLite
│   │
│   ├── __init__.py
│   └── bot.py               # Основной модуль бота
│
├── data/                    # Директория для хранения данных
│   └── newspulsebot.db      # База данных SQLite (создается автоматически)
│
├── logs/                    # Директория для хранения логов
│
├── .env.example             # Пример файла с переменными окружения
├── .env                     # Файл с переменными окружения (не хранится в репозитории)
├── requirements.txt         # Зависимости проекта
├── main.py                  # Точка входа
└── README.md                # Документация проекта
```

## 🛠️ Технологический стек

- **Python 3.9+**: Основной язык программирования
- **python-telegram-bot 20.0+**: Библиотека для работы с Telegram Bot API
- **aiohttp**: Асинхронный HTTP-клиент для запросов к API
- **SQLite**: Легковесная БД для хранения данных пользователей
- **NewsAPI**: API для получения новостей
- **python-dotenv**: Загрузка переменных окружения
- **loguru**: Продвинутое логирование
- **pydantic**: Валидация данных

## 💻 Установка и запуск

1. **Клонировать репозиторий:**

```bash
git clone https://github.com/username/NewsPulseBot.git
cd NewsPulseBot
```

2. **Установить зависимости:**

```bash
pip install -r requirements.txt
```

3. **Создать и настроить файл .env:**

```bash
cp .env.example .env
# Отредактируйте файл .env, добавив ваш Telegram Bot токен и ключ NewsAPI
```

4. **Запустить бота:**

```bash
python main.py
```

## 📝 Настройка переменных окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NEWS_API_KEY=your_news_api_key
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🧩 Примеры использования

### Получение последних новостей

```
/news
```

Результат:
```
📰 Последние главные новости:

1. [Заголовок новости 1](https://link-to-news1.com)
   🗞️ Источник новости
   📝 Краткое описание новости...

2. [Заголовок новости 2](https://link-to-news2.com)
   🗞️ Источник новости
   📝 Краткое описание новости...
```

### Получение новостей по категории

```
/latest technology
```

Результат:
```
📰 Последние новости из категории 'Технологии':

1. [Заголовок новости о технологиях 1](https://link-to-tech-news1.com)
   🗞️ Источник новости
   📝 Краткое описание новости о технологиях...

2. [Заголовок новости о технологиях 2](https://link-to-tech-news2.com)
   🗞️ Источник новости
   📝 Краткое описание новости о технологиях...
```

## 🔄 Перспективы развития проекта

- **Многоязычная поддержка**: Добавление возможности получать новости на разных языках
- **Персонализированная лента**: Алгоритм подбора новостей на основе интересов пользователя
- **Расширенный поиск**: Поиск новостей по ключевым словам и фразам
- **Планировщик уведомлений**: Настройка регулярных уведомлений о важных новостях
- **Интеграция с другими сервисами**: Подключение дополнительных источников новостей
- **Статистика использования**: Аналитика для отслеживания популярных категорий и запросов

## 📜 Лицензия

Этот проект распространяется по лицензии MIT. Подробную информацию можно найти в файле LICENSE.

## 📞 Контакты

- **Разработчик**: [Ваше Имя](https://github.com/username)
- **Email**: your.email@example.com
- **Telegram**: [@your_telegram_username](https://t.me/your_telegram_username)

---

<div align="center">
  <sub>Создано с ❤️ для демонстрации навыков программирования</sub>
</div> 