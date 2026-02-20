@echo off
REM scripts/train_model.bat
echo ========================================
echo 🚀 Insurance Fraud Model Training Pipeline
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Step 1: Download dataset
echo Step 1: Downloading dataset...
python app/agents/node4_fraud_agent/ml_models/download_multi_type_dataset.py
if %errorlevel% neq 0 (
    echo ❌ Dataset download failed!
    pause
    exit /b %errorlevel%
)

echo.
REM Step 2: Train model
echo Step 2: Training XGBoost model...
python app/agents/node4_fraud_agent/ml_models/train_multi_type_fraud.py
if %errorlevel% neq 0 (
    echo ❌ Model training failed!
    pause
    exit /b %errorlevel%
)

echo.
REM Step 3: Test model
echo Step 3: Testing model...
python tests/test_fraud_model.py

echo.
echo ✅ Training pipeline complete!
pause