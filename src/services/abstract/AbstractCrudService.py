from abc import ABC, abstractmethod
class AbstractCrudService(ABC):

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def find(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def delete_all(self, *args, **kwargs):
        raise NotImplemented
