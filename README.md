### Инструкция по запуску 
1. Создать пустую папку и открыть её в терминале

2. Клонировать репозиторий в созданную папку
```git clone <ссылка с git-hub> ./```

3. Для работы требуется настроить файлы
     - ```.env``` - Переменные среды докер (для подстановки)
     - ```.test.env``` - Данные для подключения к тестовой БД
     - ```.prod.env``` - Данные для подключения к проду БД

4. Поднять контейнеры  ```docker compose up``` <br>
   Чтобы прекратить работу контейнеров воспользуйтесь командой ```docker compose down```
   
### Команда запуска тестов 
1. ```Открыть папку в терминале```
2. ```docker compose start pytest``` - запускает тесты
3. ```docker compose logs -f pytest``` - показывает результаты тестирований за всё время

### По поводу задания 2.3
ORM запрос на получения меню и подменю находятся в файле ```src/menu_query_generator.py``` и используются в ```src/menu_repo.py``` и ```src/submenu_repo.py```


