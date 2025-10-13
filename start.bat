@echo off
echo =========================================
echo Kripto Sinyal Takip Sistemi Baslatiliyor
echo =========================================
echo.

REM Tarayiciyi arka planda baslat
echo 1. Sinyal tarayici baslatiliyor...
start /B python scanner_core.py
echo    [OK] Tarayici baslatildi
echo.

REM 5 saniye bekle
echo 2. Dashboard hazirlaniyor (5 saniye)...
timeout /t 5 /nobreak > nul
echo.

REM Streamlit dashboard'u baslat
echo 3. Dashboard aciliyor (Gelismis Versiyon)...
echo    Tarayicinizda http://localhost:8501 acilacak
echo.
streamlit run dashboard_v2.py

pause

