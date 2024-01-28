from fastapi import FastAPI
from routers import menu, submenu, dish
from database import init_db
import asyncio

app = FastAPI(root_path='/api/v1')
app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)

if __name__ == '__main__':
    asyncio.run(init_db())
