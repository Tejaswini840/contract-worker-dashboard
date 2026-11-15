@echo off
title Dashboard Refresh Tool
color 0A

echo.
echo  ============================================
echo   CONTRACT WORKER DASHBOARD - AUTO REFRESH
echo  ============================================
echo.

REM ── Ask for new Excel file path ──────────────────────────
set "DEFAULT_EXCEL=c:\Users\I758345\Downloads\C user dashboard as on 15th Nov (2).xlsx"
echo  Current Excel file:
echo  %DEFAULT_EXCEL%
echo.
set /p "NEW_EXCEL=  Enter new Excel path (or press ENTER to use above): "
if "%NEW_EXCEL%"=="" set "NEW_EXCEL=%DEFAULT_EXCEL%"

REM ── Check file exists ─────────────────────────────────────
if not exist "%NEW_EXCEL%" (
    echo.
    echo  [ERROR] File not found: %NEW_EXCEL%
    echo  Please check the path and try again.
    pause
    exit /b 1
)

echo.
echo  [1/4] Updating Excel source path...
python -c "import re,sys; f=open(r'c:\Users\I758345\Documents\GitHub\contract-worker-dashboard\clean_and_export.py',encoding='utf-8').read(); f2=re.sub(r'SRC\s*=\s*r\"[^\"]+\"','SRC  = r\"%s\"' % r'%NEW_EXCEL%'.replace('\\','\\\\'),f); open(r'c:\Users\I758345\Documents\GitHub\contract-worker-dashboard\clean_and_export.py','w',encoding='utf-8').write(f2)"
if errorlevel 1 (echo  [WARN] Could not update path, using existing) else (echo  [OK] Source path updated)

echo.
echo  [2/4] Cleaning Excel + Exporting JSON...
python "c:\Users\I758345\Documents\GitHub\contract-worker-dashboard\clean_and_export.py"
if errorlevel 1 (
    echo.
    echo  [ERROR] Clean/Export failed. Check the Excel file and try again.
    pause
    exit /b 1
)
echo  [OK] Data cleaned and exported

echo.
echo  [3/4] Rebuilding Dashboard HTML...
python "C:\Temp\build_chat.py"
if errorlevel 1 (
    echo.
    echo  [ERROR] Dashboard build failed.
    pause
    exit /b 1
)
echo  [OK] Dashboard rebuilt

echo.
echo  [4/4] Pushing to GitHub...
cd /d "c:\Users\I758345\Documents\GitHub\contract-worker-dashboard"

REM Get today's date
for /f "tokens=1-3 delims=/" %%a in ("%date%") do set TODAY=%%c-%%b-%%a
if "%TODAY%"=="" set TODAY=%date%

git add .
git commit -m "Dashboard refresh - %TODAY%"
git push origin main
if errorlevel 1 (
    echo.
    echo  [ERROR] Git push failed. Check your internet connection.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo   SUCCESS! Dashboard updated!
echo.
echo   Live URL:
echo   https://tejaswini840.github.io/contract-worker-dashboard/
echo.
echo   (Allow 1-2 minutes for GitHub Pages to update)
echo  ============================================
echo.
pause
