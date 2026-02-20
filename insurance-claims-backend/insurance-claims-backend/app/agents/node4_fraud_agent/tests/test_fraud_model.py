# tests/test_fraud_model.py
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import joblib
import pandas as pd
import numpy as np
from app.agents.node4_fraud_agent.ml_models.download_multi_type_dataset import download_mendeley_dataset

def test_model_loading():
    """Test if the trained model loads correctly"""
    print("\n" + "="*60)
    print("🔍 Testing Fraud Detection Model")
    print("="*60)
    
    # Find model file
    model_path = Path(__file__).parent.parent / 'app' / 'agents' / 'node4_fraud_agent' / 'ml_models' / 'fraud_model_multi_type.pkl'
    
    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        print("   Please run training script first:")
        print("   python app/agents/node4_fraud_agent/ml_models/train_multi_type_fraud.py")
        return False
    
    # Load model
    print(f"\n📂 Loading model from: {model_path}")
    artifacts = joblib.load(model_path)
    
    print(f"\n✅ Model loaded successfully!")
    print(f"   • Training date: {artifacts.get('training_date', 'Unknown')}")
    print(f"   • Dataset: {artifacts.get('dataset', 'Unknown')}")
    print(f"   • Features: {len(artifacts.get('feature_names', []))}")
    print(f"   • Model type: {type(artifacts['model']).__name__}")
    
    # Test prediction
    print(f"\n🧪 Testing prediction with sample data...")
    sample_data = np.random.rand(1, len(artifacts['feature_names']))
    prediction = artifacts['model'].predict(sample_data)
    probability = artifacts['model'].predict_proba(sample_data)[0]
    
    print(f"   • Prediction: {'Fraud' if prediction[0] == 1 else 'Genuine'}")
    print(f"   • Probability: {probability[1]:.4f} (fraud) / {probability[0]:.4f} (genuine)")
    
    return True

def test_dataset_download():
    """Test if dataset can be downloaded"""
    print("\n" + "="*60)
    print("📥 Testing Dataset Download")
    print("="*60)
    
    data_path = download_mendeley_dataset()
    
    if data_path:
        print(f"\n✅ Dataset test passed!")
        return True
    else:
        print(f"\n❌ Dataset test failed")
        return False

if __name__ == "__main__":
    # Test dataset download
    download_ok = test_dataset_download()
    
    # Test model loading (if exists)
    model_ok = test_model_loading()
    
    print("\n" + "="*60)
    if download_ok:
        print("✅ Dataset: Available")
    else:
        print("❌ Dataset: Not available")
    
    if model_ok:
        print("✅ Model: Trained and ready")
    else:
        print("⚠️ Model: Not trained yet - run training script")
    print("="*60)