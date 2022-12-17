@echo off
set /p tmp="run tox? make sure OneDrive is paused! y/[n]: "
if "%tmp%"=="y" (
    tox --workdir ..
)
set /p tmp="Press enter to exit"
