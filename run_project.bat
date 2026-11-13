@echo off
REM ============================================================================
REM Reproducible Batch Runner
REM Customer Churn Prediction & Retention Decision Support System
REM ============================================================================

echo ============================================================================
echo Starting Customer Churn Prediction and Decision Support System Pipeline...
echo ============================================================================

REM Check Python installation
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Optional: Install requirements
if exist "requirements.txt" (
    echo Verifying Python dependencies...
    pip install -r requirements.txt --quiet
)

REM Run the master pipeline
python run_analysis.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================================
    echo PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
    echo All data, models, visualisations, SQL scripts, and Power BI assets are ready.
    echo ============================================================================
) else (
    echo.
    echo ============================================================================
    echo An error occurred during pipeline execution.
    echo ============================================================================
)

pause
