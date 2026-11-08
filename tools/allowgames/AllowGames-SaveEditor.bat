@echo off
rem Allow Games Save Editor: drag a progress.sav onto this file. A backup is made first.
setlocal
set "PY=%~dp0..\tools\python\python.exe"
if not exist "%PY%" set "PY=python"
if "%~1"=="" (
  echo Arrastra un progress.sav sobre este archivo / Drag a progress.sav onto this file.
  echo Carpeta / Folder: ^<juego^>\user\save\^<cuenta^>\slot_NN\progress.sav
  pause
  exit /b 1
)
"%PY%" -I "%~dp0ag_save_editor.py" "%~1" all
"%PY%" -I "%~dp0ag_save_editor.py" "%~1" show
pause
