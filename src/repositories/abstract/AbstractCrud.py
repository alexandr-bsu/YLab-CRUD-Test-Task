from abc import ABC, abstractmethod


class AbstractCrud(ABC):

    @abstractmethod
    async def create(self, data, parent_id):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, parent_id):
        raise NotImplementedError

    @abstractmethod
    async def find(self, id):
        raise NotImplementedError

    @abstractmethod
    async def update(self, data, id):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id):
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, parent_id):
        raise NotImplementedError
