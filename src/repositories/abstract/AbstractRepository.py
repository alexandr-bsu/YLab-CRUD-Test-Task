from abc import ABC, abstractmethod
from pydantic import BaseModel

class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: BaseModel, custom_query=None, **extra_params) -> dict:
        """
        Метод для добавления записи в таблицу
        :param data: объект pydantic модели
        :param custom_query: запрос, который вызывается вместо реализованого по-умолчанию
        :param extra_params: данные для колонок, которые не указаны в модели из data
        :returns: Объект с данными, содержащиеся в созданной записи БД
        """
        raise NotImplemented

    @abstractmethod
    async def find_all(self, custom_query=None, **filters) -> dict:
        """
        Метод для поиска всех записей в таблице, удовлетворяющие заданным условиям
        :param custom_query: запрос, который вызывается вместо реализованого по-умолчанию
        :param filters: фильтры по колонкам
        :returns: Объект с данными, содержащиеся в полученных записях БД
        """
        raise NotImplemented

    @abstractmethod
    async def find(self, custom_query=None, **filters) -> dict:
        """
        Метод для поиска одной записи в таблице, удовлетворяющей заданным условиям
        :param custom_query: запрос, который вызывается вместо реализованого по-умолчанию
        :param filters: фильтры по колонкам
         :returns: Объект с данными, содержащиеся в полученной записи БД
        """
        raise NotImplemented

    @abstractmethod
    async def update(self, data: BaseModel, custom_query=None, **filters) -> dict:
        """
        Метод для обновления записей в таблице, удовлетворяющей заданным условиям
        :param data: объект pydantic модели
        :param custom_query: запрос, который вызывается вместо реализованого по-умолчанию
        :param filters: фильтры по колонкам
         :returns: Объект с данными, содержащиеся в обновлённой записи БД
        """
        raise NotImplemented

    @abstractmethod
    async def delete(self, custom_query=None, **filters) -> dict:
        """
        Метод для удаления записей в таблице, удовлетворяющей заданным условиям
        :param custom_query: запрос, который вызывается вместо реализованого по-умолчанию
        :param filters: фильтры по колонкам
        """
        raise NotImplemented


