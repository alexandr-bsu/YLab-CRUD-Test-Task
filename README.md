### Инструкция по запуску 
1. Создать пустую папку и открыть её в терминале

2. Клонировать репозиторий в созданную папку
```git clone <ссылка с git-hub> ./```

3. Для работы требуется настроить файлы
     - ```.env``` - Переменные среды докер (для подстановки)
     - ```.test.env``` - Данные для подключения к тестовой БД
     - ```.prod.env``` - Данные для подключения к проду БД
     - **Для тестов можно оставить как есть**

4. Запустить команды в корневой папке проекта
     1. ```docker compose build```
     2. ``` docker compose -f docker-compose-test.yaml build```

5. Поднять контейнеры  ```docker compose up -d``` <br>
   Чтобы прекратить работу контейнеров воспользуйтесь командой ```docker compose down```
   
### Команда запуска тестов 

1. ```Открыть корневую папку в терминале```
3. Выполнить ```docker compose up && docker compose -f docker-compose-test.yaml up && docker compose -f docker-compose-test.yaml down```


### По поводу задания 2.3
ORM запрос на получения меню и подменю находятся в файле ```src/menu_query_generator.py``` и используются в ```src/menu_repo.py``` и ```src/submenu_repo.py```


