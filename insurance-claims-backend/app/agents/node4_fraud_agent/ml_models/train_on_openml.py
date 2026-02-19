# app/agents/node4_fraud_agent/ml_models/train_on_openml.py

import openml
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os
import json
from datetime import datetime

class OpenMLFraudTrainer:
    """
    Train XGBoost model on OpenML fraud dataset
    """
    
    def __init__(self, dataset_id=None, dataset_name=None):
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        
    def find_fraud_dataset(self):
        """Search for fraud-related datasets on OpenML"""
        print("🔍 Searching for fraud datasets on OpenML...")
        
        # List all datasets
        datasets = openml.datasets.list_datasets(output_format="dataframe")
        
        # Filter for fraud-related terms
        fraud_keywords = ['fraud', 'insurance', 'claim', 'creditcard', 'transaction']
        mask = datasets['name'].astype(str).str.lower().apply(
            lambda x: any(keyword in str(x) for keyword in fraud_keywords)
        )
        fraud_datasets = datasets[mask]
        
        print(f"\n📊 Found {len(fraud_datasets)} potential fraud datasets:")
        for idx, row in fraud_datasets.head(10).iterrows():
            dataset_id = row.get('did')
            dataset_name = str(row.get('name', ''))
            instances = row.get('NumberOfInstances')

            try:
                dataset_id_text = f"{int(float(dataset_id)):6d}"
            except (TypeError, ValueError):
                dataset_id_text = "   n/a"

            try:
                instances_text = f"{int(float(instances)):7,d}"
            except (TypeError, ValueError):
                instances_text = "    n/a"

            print(f"   ID: {dataset_id_text} | {dataset_name[:40]:40s} | Instances: {instances_text}")
        
        return fraud_datasets
    
    def load_dataset(self, dataset_id=None):
        """Load dataset from OpenML by ID"""
        if dataset_id:
            self.dataset_id = dataset_id
        
        if not self.dataset_id:
            raise ValueError("No dataset ID provided")
        
        print(f"\n📥 Loading dataset ID: {self.dataset_id} from OpenML...")
        
        # Download dataset
        dataset = openml.datasets.get_dataset(self.dataset_id)
        
        print(f"   Dataset: {dataset.name}")
        print(f"   Description: {dataset.description[:200]}...")
        
        # Get the data
        X, y, categorical_indicator, attribute_names = dataset.get_data(
            target=dataset.default_target_attribute
        )
        
        # Convert to DataFrame
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=attribute_names)
        
        print(f"   Shape: {X.shape}")
        print(f"   Features: {len(attribute_names)}")
        print(f"   Target: {dataset.default_target_attribute}")
        
        # Store feature names
        self.feature_names = attribute_names
        
        return X, y, dataset
    
    def preprocess_data(self, X, y):
        """Preprocess the data for XGBoost"""
        print("\n🛠️ Preprocessing data...")
        
        X_processed = X.copy()
        
        # Handle categorical columns
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns
        print(f"   Categorical columns: {list(categorical_cols)}")
        
        for col in categorical_cols:
            le = LabelEncoder()
            X_processed[col] = le.fit_transform(X_processed[col].astype(str))
            self.label_encoders[col] = le
        
        # Handle missing values
        imputer = SimpleImputer(strategy='median')
        numeric_cols = X_processed.select_dtypes(include=[np.number]).columns
        X_processed[numeric_cols] = imputer.fit_transform(X_processed[numeric_cols])
        
        # Scale numerical features
        X_processed[numeric_cols] = self.scaler.fit_transform(X_processed[numeric_cols])
        
        # Encode target if needed
        if y.dtype == 'object' or isinstance(y, pd.Series) and y.dtype == 'object':
            y = LabelEncoder().fit_transform(y)
        
        print(f"   Preprocessed shape: {X_processed.shape}")
        
        return X_processed, y
    
    def train_xgboost(self, X_train, y_train, X_val=None, y_val=None):
        """Train XGBoost model with hyperparameter tuning"""
        print("\n🚀 Training XGBoost model...")
        
        # Calculate class weights for imbalance
        scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum() if 1 in y_train else 1
        
        # Define hyperparameter grid
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [4, 6, 8, 10],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.6, 0.8, 1.0],
            'min_child_weight': [1, 3, 5],
            'gamma': [0, 0.1, 0.2],
            'scale_pos_weight': [scale_pos_weight]
        }
        
        # Base model
        xgb_model = xgb.XGBClassifier(
            objective='binary:logistic',
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        # Randomized search for hyperparameters
        random_search = RandomizedSearchCV(
            xgb_model,
            param_distributions=param_grid,
            n_iter=20,
            cv=3,
            scoring='roc_auc',
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        print("   Performing hyperparameter search...")
        random_search.fit(X_train, y_train)
        
        self.model = random_search.best_estimator_
        
        print(f"\n✅ Best parameters: {random_search.best_params_}")
        print(f"✅ Best CV Score: {random_search.best_score_:.4f}")
        
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("\n📊 Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='binary'),
            'recall': recall_score(y_test, y_pred, average='binary'),
            'f1_score': f1_score(y_test, y_pred, average='binary'),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        print(f"   Accuracy:  {metrics['accuracy']:.4f}")
        print(f"   Precision: {metrics['precision']:.4f}")
        print(f"   Recall:    {metrics['recall']:.4f}")
        print(f"   F1-Score:  {metrics['f1_score']:.4f}")
        print(f"   ROC-AUC:   {metrics['roc_auc']:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n   Confusion Matrix:")
        print(f"   TN: {cm[0,0]:5d}  FP: {cm[0,1]:5d}")
        print(f"   FN: {cm[1,0]:5d}  TP: {cm[1,1]:5d}")
        
        return metrics
    
    def save_model(self, filepath="ml_models/fraud_model_openml.pkl"):
        """Save trained model and preprocessors"""
        print(f"\n💾 Saving model to {filepath}...")
        
        model_artifacts = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'dataset_id': self.dataset_id,
            'training_date': datetime.now().isoformat()
        }
        
        joblib.dump(model_artifacts, filepath)
        print("✅ Model saved successfully!")
        
        return filepath
    
    def run_pipeline(self, dataset_id=None):
        """Run complete training pipeline"""
        
        # Load data
        X, y, dataset = self.load_dataset(dataset_id)
        
        # Preprocess
        X_processed, y_processed = self.preprocess_data(X, y)
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            X_processed, y_processed, test_size=0.3, random_state=42, stratify=y_processed
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )
        
        print(f"\n📈 Data split:")
        print(f"   Train: {len(X_train)} samples")
        print(f"   Validation: {len(X_val)} samples")
        print(f"   Test: {len(X_test)} samples")
        
        # Train model
        self.train_xgboost(X_train, y_train, X_val, y_val)
        
        # Evaluate
        metrics = self.evaluate_model(X_test, y_test)
        
        # Save model
        model_path = self.save_model()
        
        return {
            'model_path': model_path,
            'metrics': metrics,
            'dataset': dataset.name,
            'dataset_id': self.dataset_id
        }

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train XGBoost on OpenML fraud dataset')
    parser.add_argument('--dataset_id', type=int, help='OpenML dataset ID')
    parser.add_argument('--search', action='store_true', help='Search for fraud datasets')
    args = parser.parse_args()
    
    trainer = OpenMLFraudTrainer()
    
    if args.search:
        # Search for fraud datasets
        datasets = trainer.find_fraud_dataset()
        
        # Ask user to select one
        print("\n" + "="*60)
        selected_id = input("Enter dataset ID to train on (or press Enter to skip): ")
        if selected_id:
            args.dataset_id = int(selected_id)
    
    if args.dataset_id:
        # Train on specified dataset
        results = trainer.run_pipeline(dataset_id=args.dataset_id)
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print(f"   Dataset: {results['dataset']}")
        print(f"   Model saved: {results['model_path']}")
        print(f"   ROC-AUC: {results['metrics']['roc_auc']:.4f}")
    else:
        print("\nℹ️ No dataset ID provided. Use --search to find datasets or --dataset_id to specify.")