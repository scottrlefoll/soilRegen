@echo off
cd venv\Scripts
call activate
cd ..\..
python manage.py runserver
