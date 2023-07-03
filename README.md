###Описание проекта:
- Проект api_yamdb - это API для проекта YaMDb, который собирает отзывы пользователей на произведения

###Запуск проекта

- Cоздать и активировать виртуальное окружение:



    python3 -m venv venv
    source venv/bin/activate
- Установить зависимости из файла requirements.txt:



    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
- Выполнить миграции:



    python3 manage.py migrate
- Запустить проект:



    python3 manage.py runserver