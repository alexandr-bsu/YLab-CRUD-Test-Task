import pytest
from src.config import settings, Mode
from fastapi.testclient import TestClient
from src.main import app
from httpx import AsyncClient
from database import init_db
import asyncio


# fix problem "different event loop"
# more about problem: https://github.com/pytest-dev/pytest-asyncio/issues/38
# https://github.com/pytest-dev/pytest-asyncio/issues/207?ysclid=lrvse25g7y347904505
@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
@pytest.fixture(scope="session", autouse=True)
async def init_db_fixture():
    assert settings.MODE == Mode.TEST
    await init_db()
    yield


@pytest.fixture(scope='session')
def post_menu():
    return {
        'title': 'Menu 1',
        'description': 'Menu 1 description'
    }

@pytest.fixture(scope='session')
def update_menu():
    return {
            'title': 'Updated menu 1',
            'description': 'Updated menu 1 description'
        }

@pytest.fixture(scope='session')
def post_submenu():
    return {
        'title': 'Submenu 1',
        'description': 'Submenu 1 description'
    }


@pytest.fixture(scope='session')
def update_submenu():
    return {
        'title': 'Updated submenu 1',
        'description': 'Updated submenu 1 description'
    }

@pytest.fixture(scope='session')
def post_dish_1():
    return {
        'title': 'Dish 1',
        'description': 'Dish 1 description',
        'price': '25.80'
    }


@pytest.fixture(scope='session')
def update_dish_1():
    return {
        'title': 'Updated dish 1',
        'description': 'Updated dish 1 description',
        'price': '40.30'
    }


@pytest.fixture(scope='session')
def post_dish_2():
    return {
        'title': 'Dish 2',
        'description': 'Dish 2 description',
        'price': '560.00'
    }


@pytest.fixture(scope='session')
def update_dish_2():
    return {
        'title': 'Updated dish 2',
        'description': 'Updated dish 2 description',
        'price': '570.00'
    }


# Хранит данные в тест-сессии (аналог environment в postman)
@pytest.fixture(scope='session')
def session_storage():
    return {}

