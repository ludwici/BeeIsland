@echo off
Chcp 65001
cd ..
set main_folder=%cd%\src\
cd res
cd images
for /r %%i in (*.qrc) do (
echo %%i
if not exist %main_folder%%%~ni_rc.py (
D:\Python\BeeIsland\venv\Scripts\pyrcc5 %%~nxi -o %main_folder%%%~ni_rc.py
)
)