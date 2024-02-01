@echo off
REM run flake8 on py416.json
REM E501 is the "line too long" error
flake8 --extend-ignore=E501 ../src/py416/json.py
set /p tmp="Press enter to exit"