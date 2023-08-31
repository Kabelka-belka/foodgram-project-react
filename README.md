![example workflow](https://github.com/Kabelka-belka/foodgram-project-react/actions/workflows/foodgram_main.yml/badge.svg)

## Сервис доступен по адресу:
http://158.160.101.62/
## Запуск проекта:

### 1. Клонируйте проект:
https://github.com/Kabelka-belka/foodgram-project-react.git

### 2. Подготовьте сервер:
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/

### 3. Установите docker и docker-compose:
sudo apt install docker.io 
sudo apt install docker-compose

### 4. Соберите контейнер и выполните миграции:
sudo docker-compose up -d --build
sudo docker-compose exec backend python manage.py migrate

### 5. Создайте суперюзера и соберите статику:
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input

### 6. Скопируйте предустановленные данные json:
sudo docker-compose exec backend python manage.py loadmodels --path 'recipes/data/ingredients.json'
sudo docker-compose exec backend python manage.py loadmodels --path 'recipes/data/tags.json'

### 7. Данные для проверки работы приложения: Суперпользователь:
email: 
password:
