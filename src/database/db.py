import sqlite3
import os
from typing import Dict, List, Optional, Tuple, Any
import asyncio
from loguru import logger


class Database:
    """Класс для работы с базой данных SQLite."""
    
    def __init__(self, db_path: str = "data/newspulsebot.db"):
        """Инициализация базы данных.
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
        
    def _init_db(self) -> None:
        """Инициализация базы данных и создание таблиц."""
        conn = self._get_connection()
        
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                favorite_category TEXT,
                last_command TEXT,
                language TEXT DEFAULT 'ru',
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            ''')
            
            conn.commit()
            logger.info("База данных инициализирована успешно")
        except Exception as e:
            logger.error("Ошибка при инициализации базы данных: {}", str(e))
            raise
        finally:
            conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Получение соединения с базой данных.
        
        Returns:
            Соединение с базой данных
        """
        return sqlite3.connect(self.db_path)
    
    async def execute(self, query: str, params: Tuple = ()) -> None:
        """Асинхронное выполнение запроса без возврата результата.
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._execute, query, params)
    
    def _execute(self, query: str, params: Tuple = ()) -> None:
        """Синхронное выполнение запроса без возврата результата.
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
        """
        conn = self._get_connection()
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            logger.error("Ошибка при выполнении запроса: {} - {}", query, str(e))
            raise
        finally:
            conn.close()
    
    async def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Асинхронное выполнение запроса с возвратом одной строки.
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            
        Returns:
            Словарь с результатом запроса или None
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._fetch_one, query, params)
    
    def _fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Синхронное выполнение запроса с возвратом одной строки.
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            
        Returns:
            Словарь с результатом запроса или None
        """
        conn = self._get_connection()
        
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            return dict(row) if row else None
        except Exception as e:
            logger.error("Ошибка при выполнении запроса: {} - {}", query, str(e))
            raise
        finally:
            conn.close()
    
    async def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Асинхронное выполнение запроса с возвратом всех строк.
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            
        Returns:
            Список словарей с результатами запроса
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._fetch_all, query, params)
    
    def _fetch_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Синхронное выполнение запроса с возвратом всех строк.
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            
        Returns:
            Список словарей с результатами запроса
        """
        conn = self._get_connection()
        
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error("Ошибка при выполнении запроса: {} - {}", query, str(e))
            raise
        finally:
            conn.close()
            
    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str) -> None:
        """Добавление нового пользователя или обновление существующего.
        
        Args:
            user_id: ID пользователя в Telegram
            username: Имя пользователя в Telegram
            first_name: Имя пользователя
            last_name: Фамилия пользователя
        """
        await self.execute(
            """
            INSERT INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name
            """,
            (user_id, username, first_name, last_name)
        )
        
        # Создаем запись о предпочтениях, если ее еще нет
        await self.execute(
            """
            INSERT OR IGNORE INTO user_preferences (user_id)
            VALUES (?)
            """,
            (user_id,)
        )
        
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение информации о пользователе.
        
        Args:
            user_id: ID пользователя в Telegram
            
        Returns:
            Словарь с информацией о пользователе или None
        """
        return await self.fetch_one(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        
    async def update_user_preference(self, user_id: int, favorite_category: Optional[str] = None, 
                                    last_command: Optional[str] = None, language: Optional[str] = None) -> None:
        """Обновление предпочтений пользователя.
        
        Args:
            user_id: ID пользователя в Telegram
            favorite_category: Любимая категория новостей
            last_command: Последняя выполненная команда
            language: Предпочитаемый язык
        """
        # Собираем только те поля, которые нужно обновить
        update_fields = []
        params = []
        
        if favorite_category is not None:
            update_fields.append("favorite_category = ?")
            params.append(favorite_category)
            
        if last_command is not None:
            update_fields.append("last_command = ?")
            params.append(last_command)
            
        if language is not None:
            update_fields.append("language = ?")
            params.append(language)
            
        if not update_fields:
            return
            
        query = f"""
            UPDATE user_preferences 
            SET {', '.join(update_fields)}
            WHERE user_id = ?
        """
        params.append(user_id)
        
        await self.execute(query, tuple(params))
        
    async def get_user_preferences(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение предпочтений пользователя.
        
        Args:
            user_id: ID пользователя в Telegram
            
        Returns:
            Словарь с предпочтениями пользователя или None
        """
        return await self.fetch_one(
            "SELECT * FROM user_preferences WHERE user_id = ?",
            (user_id,)
        ) 