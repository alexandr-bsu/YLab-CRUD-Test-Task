from fastapi import FastAPI
from routers import menu, submenu, dish


app = FastAPI(root_path='/api/v1')
app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)


@app.get('/healthy', status_code=200)
async def check():
    return 'OK'

# if __name__ == '__main__':
#     asyncio.run(init_db())
