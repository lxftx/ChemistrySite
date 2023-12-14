cd C:\chemistry-server

rem Создание виртуального окружения
python -m venv venv

rem Активация виртуального окружения (если используется)
call C:\chemistry-server\venv\Scripts\activate

rem Установка необходимых библиотек
pip install -r requirements.txt

rem Переход в директорию с вашим Django проектом
cd C:\chemistry-server\ChemistrySite

rem Запуск миграций (если необходимо)
python manage.py makemigrations
python manage.py migrate

rem Запуск сервера Django
python manage.py runserver

pause