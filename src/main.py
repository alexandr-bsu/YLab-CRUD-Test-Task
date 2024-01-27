from fastapi import FastAPI
from routers import menu, submenu, dish
from database import init_db
from fastapi.middleware.cors import CORSMiddleware
import asyncio


app = FastAPI(root_path='/api/v1')
app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == '__main__':
    asyncio.run(init_db())