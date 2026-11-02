@echo off
"%~dp0.venv\Scripts\python.exe" "%~dp0scripts\serve_dashboard.py"
exit /b %errorlevel%
