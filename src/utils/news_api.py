import os
from typing import Dict, List, Optional, Any
import aiohttp
from loguru import logger
from pydantic import BaseModel


class Article(BaseModel):
    """Модель для представления новостной статьи."""
    source: str
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: str
    published_at: str
    

class NewsAPIClient:
    """Клиент для работы с NewsAPI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Инициализация клиента NewsAPI.
        
        Args:
            api_key: API ключ для NewsAPI. Если не указан, берется из переменной окружения.
        """
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise ValueError("API ключ для NewsAPI не найден.")
        
        self.base_url = "https://newsapi.org/v2"
        
    async def get_top_headlines(
        self, 
        category: Optional[str] = None, 
        country: str = "ru", 
        page_size: int = 5
    ) -> List[Article]:
        """Получение главных новостей.
        
        Args:
            category: Категория новостей (бизнес, развлечения, здоровье, наука, спорт, технологии)
            country: Код страны (по умолчанию - Россия)
            page_size: Количество новостей
            
        Returns:
            Список новостных статей
        """
        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": page_size
        }
        
        if category:
            params["category"] = category
            
        logger.debug("Запрос заголовков новостей: {}", params)
        
        try:
            articles = await self._make_request("top-headlines", params)
            return self._parse_articles(articles)
        except Exception as e:
            logger.error("Ошибка при получении заголовков новостей: {}", str(e))
            raise
    
    async def get_everything(
        self, 
        query: str, 
        language: str = "ru", 
        sort_by: str = "publishedAt", 
        page_size: int = 5
    ) -> List[Article]:
        """Поиск новостей по ключевым словам.
        
        Args:
            query: Поисковый запрос
            language: Язык новостей
            sort_by: Сортировка (relevancy, popularity, publishedAt)
            page_size: Количество новостей
            
        Returns:
            Список новостных статей
        """
        params = {
            "apiKey": self.api_key,
            "q": query,
            "language": language,
            "sortBy": sort_by,
            "pageSize": page_size
        }
        
        logger.debug("Поиск новостей: {}", params)
        
        try:
            articles = await self._make_request("everything", params)
            return self._parse_articles(articles)
        except Exception as e:
            logger.error("Ошибка при поиске новостей: {}", str(e))
            raise
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Выполнение запроса к API.
        
        Args:
            endpoint: Конечная точка API
            params: Параметры запроса
            
        Returns:
            Список статей из ответа API
        """
        url = f"{self.base_url}/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    text = await response.text()
                    logger.error(f"Ошибка API: {response.status} - {text}")
                    raise Exception(f"API вернул статус {response.status}: {text}")
                
                data = await response.json()
                
                if data.get("status") != "ok":
                    logger.error(f"Ошибка API: {data.get('message', 'Неизвестная ошибка')}")
                    raise Exception(f"API вернул ошибку: {data.get('message', 'Неизвестная ошибка')}")
                
                return data.get("articles", [])
    
    def _parse_articles(self, articles: List[Dict[str, Any]]) -> List[Article]:
        """Преобразование статей из API в модель Article.
        
        Args:
            articles: Список статей из ответа API
            
        Returns:
            Список объектов Article
        """
        result = []
        
        for article in articles:
            try:
                result.append(
                    Article(
                        source=article.get("source", {}).get("name", "Неизвестный источник"),
                        author=article.get("author"),
                        title=article.get("title", ""),
                        description=article.get("description"),
                        url=article.get("url", ""),
                        published_at=article.get("publishedAt", "")
                    )
                )
            except Exception as e:
                logger.warning(f"Не удалось обработать статью: {str(e)}")
                
        return result 