from fastapi import FastAPI
from routers import Menu, Submenu, Dish
import asyncio
from database.engine import init_db

app = FastAPI(root_path='/api/v1')
app.include_router(Menu.router)
app.include_router(Submenu.router)
app.include_router(Dish.router)

# if __name__ == '__main__':
#    asyncio.run(init_db())
