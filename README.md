
# Foodgram - "Продуктовый помощник"
![workflow](https://github.com/Timoha23/foodgram-project-react/actions/workflows/Foodgram.yml/badge.svg)
## Описание

Данный проект является базой кулинарных рецептов. Именно здесь пользователи могут создавать свои рецепты, редактировать их, а так же читать рецепты других пользователей, подписываться на интересных авторов, добавлять понравившиеся рецепты в избранное и добавлять рецепты в список покупок, после чего скачивать данный список на свои устройства.

## Использованные технологии

* Python 3.9;
* Django 2.2.16;
* Django REST Framework 3.12.4;
* Pillow 9.3.0;
* Djoser 2.1.0;
* Gunicorn 2.1.0;
* Psycopg 2.8.6;
* Docker;
* PostgreSQL.

## Запуск проекта
Клонируем репозиторий:

    git clone https://github.com/Timoha23/foodgram-project-react.git
Устанавливаем и активируем виртуальное окружение:

    python -m venv venv
    source venv/Scripts/activate
Устанавливаем все зависимости из файла requirements.txt:

    pip install -r requirements.txt
Применяем миграции:

    python manage.py migrate
Так же в папке backend расположен файл с дампом базы данных, в котором хранятся ингредиенты, добавить их в базу можно следующей командой:
  

    python manage.py loaddata dump.json


## Сборка контейнеров

Переходим в директорию с файлом docker-compsoe:

    cd foodgram-project-react/infra/

Запускаем docker-compose:

    docker-compose up -d  --build
Выполняем миграции:

    docker-compose exec backend python manage.py migrate
Собираем статику:

    docker-compose exec backand python manage.py collectstatic
 Создаем суперпользователя:

     docker-compose exec backend python manage.py createsuperuser
## Пример заполнения .env файла
В директории infra создаем .env файл и заполняем его как в примере ниже (данные подставляйте свои):

    DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
    
    DB_NAME=postgres # имя базы данных
    
    POSTGRES_USER=postgres # логин для подключения к базе данных
    
    POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
    
    DB_HOST=db # название сервиса (контейнера)
    
    DB_PORT=5432 # порт для подключения к БД
    
    SECRET_KEY=your_secret_key # SECRET_KEY из settings.py
 ## Адрес сайта
http://158.160.1.14/

**Автор бэкенда:**
*Ершов Тимофей Сергеевич*
