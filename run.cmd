@echo off
rem Активируем виртуальное окружение
call venv\Scripts\activate.bat
rem Запускаем приложение
python app.py > weather.html
rem Деактивируем виртуальное окружение
call venv\Scripts\deactivate.bat


