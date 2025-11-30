@echo off
rem Run backend (FastAPI) and frontend (Next.js) in separate cmd windows
setlocal enabledellayedexpansion

set REPO_ROOT=%~dp0
set BACKEND_DIR=%REPO_ROOT%backend
set FRONTEND_DIR=%REPO_ROOT%frontend
set BACKEND_PORT=8000
set FRONTEND_PORT=3000

echo Starting backend in a new window...
start "Cardano Backend" cmd /k "cd /d "%BACKEND_DIR%" && if not exist .venv (python -m venv .venv && .venv\Scripts\pip install -r requirements.txt) && call .venv\Scripts\activate.bat && set PORT=%BACKEND_PORT% && uvicorn main:app --host 0.0.0.0 --port %BACKEND_PORT%"

echo Starting frontend in a new window...
start "Cardano Frontend" cmd /k "cd /d "%FRONTEND_DIR%" && if not exist node_modules (npm install) && set PORT=%FRONTEND_PORT% && npm run dev"

echo Both services should now be running in separate windows.
echo - Backend: http://localhost:%BACKEND_PORT%  (FastAPI)
echo - Frontend: http://localhost:%FRONTEND_PORT% (Next.js)
echo Close the two command windows to stop the services.

endlocal
exit /b 0
