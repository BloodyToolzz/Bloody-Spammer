@echo off
color 0C
cls
pip install -r requirements.txt
cls
echo [INFO] Adding start.bat
ping localhost -n 2 >nul
echo python Bloody_Spammer_V2.py >> start.bat
echo [INFO] Done!
ping localhost -n 2 >nul
echo [INFO] Deleting setup.bat
del setup.bat
ping localhost -n 2 >nul
echo [INFO] Done!
pause