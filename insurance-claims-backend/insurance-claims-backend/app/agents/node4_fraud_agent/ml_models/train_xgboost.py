# app/agents/node4_fraud_agent/ml_models/train_xgboost.py

import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

def generate_mock_training_data(n_samples: int = 10000):
    """
    Generate mock training data for fraud detection
    In production, use real historical claims data
    """
    np.random.seed(42)
    
    data = {
        'claim_amount': np.random.uniform(1000, 500000, n_samples),
        'days_since_policy': np.random.randint(0, 365, n_samples),
        'days_to_report': np.random.randint(0, 60, n_samples),
        'document_count': np.random.randint(1, 10, n_samples),
        'round_amount_flag': np.random.randint(0, 2, n_samples),
        'provider_volume': np.random.randint(0, 50, n_samples),
        'claimant_history': np.random.randint(0, 10, n_samples),
        'network_density': np.random.uniform(0, 1, n_samples),
        'name_match_score': np.random.uniform(0.5, 1, n_samples),
        'address_match_score': np.random.uniform(0.5, 1, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate fraud labels (1 for fraud, 0 for legitimate)
    # Based on realistic patterns
    fraud_prob = (
        0.3 * (df['claim_amount'] > 400000).astype(int) +
        0.2 * (df['days_since_policy'] < 7).astype(int) +
        0.2 * (df['provider_volume'] > 30).astype(int) +
        0.15 * (df['claimant_history'] > 5).astype(int) +
        0.15 * (df['round_amount_flag'] == 1).astype(int)
    )
    
    df['fraud_label'] = (fraud_prob + np.random.normal(0, 0.1, n_samples)) > 0.3
    df['fraud_label'] = df['fraud_label'].astype(int)
    
    return df

def train_model():
    """
    Train XGBoost model for fraud detection
    Accuracy target: 92-95%
    """
    print("🚀 Training XGBoost Fraud Detection Model...")
    
    # Generate training data
    df = generate_mock_training_data(10000)
    
    # Prepare features and target
    feature_cols = [col for col in df.columns if col != 'fraud_label']
    X = df[feature_cols]
    y = df['fraud_label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Calculate class weights (fraud is usually imbalanced)
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    # Create XGBoost model
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    # Train model
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=10,
        verbose=False
    )
    
    # Evaluate
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"✅ Model trained successfully!")
    print(f"📊 Performance Metrics:")
    print(f"   Accuracy:  {accuracy:.3f}")
    print(f"   Precision: {precision:.3f}")
    print(f"   Recall:    {recall:.3f}")
    print(f"   F1-Score:  {f1:.3f}")
    
    # Feature importance
    importance = model.feature_importances_
    print("\n📈 Feature Importance:")
    for name, imp in zip(feature_cols, importance):
        print(f"   {name}: {imp:.3f}")
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), "fraud_model.pkl")
    joblib.dump(model, model_path)
    print(f"💾 Model saved to {model_path}")
    
    return model

if __name__ == "__main__":
    train_model()