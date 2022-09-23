@echo off
REM run flake8 on py416.files
REM E501 is the "line too long" error
flake8 --extend-ignore=E501 ../src/py416/files.py
set /p tmp="Press enter to exit"