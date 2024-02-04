from abc import ABC, abstractmethod


class AbstractCrud(ABC):

    @abstractmethod
    async def create(self, data, parent_id):
        ...

    @abstractmethod
    async def find_all(self, parent_id):
        ...

    @abstractmethod
    async def find(self, id):
        ...

    @abstractmethod
    async def update(self, data, id):
        ...

    @abstractmethod
    async def delete(self, id):
        ...

    @abstractmethod
    async def delete_all(self, parent_id):
        ...

