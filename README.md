## Инструкции по запуску приложения

1) Запустить Postgres и создать в нём базу данных с любым названием (название нужно потом вставть в DB_NAME в .env)

2) Создать пустую папку и склонировать туда репозиторий с кодом
git clone https://github.com/alexandr-bsu/YLab-CRUD-Test-Task.git ./

3) переименовать .env_test в .env, подставить в поля данные для подключения к БД

3) Создать виртуальное окружение 
python -m venv venv

4) Запустить виртуальное окружение
venv\Scripts\activate

5) Установить зависимости из файла requirements.txt
pip install -r requirements.txt

6) ТОЛЬКО ПРИ ПЕРВОМ ЗАПУСКЕ ПРИЛОЖЕНИЯ! Запустить файл main.py для создания таблиц

7) Запустить сервер api
uvicorn main:app --reload
