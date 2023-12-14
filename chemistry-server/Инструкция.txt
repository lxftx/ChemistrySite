Чтобы запустить сервер вам потребуется Python. 
1. Его можно скачать с официального сайта "https://www.python.org/downloads/", 
2. Либо с Microsoft Store.

Установите прожимая Далее.

Скопируйте директорию(папку) "chemistry-server" и вставьте на диск C
Проект должен лежать именно так С:\chemistry-server

Внутри директории(папки) "chemistry-server" лежат два Bat-файла, один из них для версии Windows 10 "RunServerW10.bat" и
для версии Windows 11 "RunServerW11.bat". Отличие двух файлов связанно с командой "python". В Windows 11 после этой команды нас
перенаправляет на Microsoft Store для скачивания Python. Поэтому в Windows 11 используется команда "py".

Запустите файл исходя из версии вашей операционной системы.

Приложу содержимое файлов "RunServerW10.bat" и "RunServerW11.bat":

-- Для "RunServerW10.bat":
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


-- Для "RunServerW11.bat":
cd C:\chemistry-server

rem Создание виртуального окружения
py -m venv venv

rem Активация виртуального окружения (если используется)
call C:\chemistry-server\venv\Scripts\activate

rem Установка необходимых библиотек
pip install -r requirements.txt

rem Переход в директорию с вашим Django проектом
cd C:\chemistry-server\ChemistrySite

rem Запуск миграций (если необходимо)
py manage.py makemigrations
py manage.py migrate

rem Запуск сервера Django
py manage.py runserver

pause
