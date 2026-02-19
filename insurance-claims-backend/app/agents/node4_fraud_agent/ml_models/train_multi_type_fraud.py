# # train_multi_type_fraud.py
# import pandas as pd
# import numpy as np
# import xgboost as xgb
# from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
# from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
#                             f1_score, roc_auc_score, confusion_matrix,
#                             classification_report)
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.impute import SimpleImputer
# import joblib
# import os
# from datetime import datetime
# from pathlib import Path
# import warnings
# warnings.filterwarnings('ignore')

# class MultiTypeFraudTrainer:
#     """
#     Train XGBoost on multi-type insurance fraud dataset
#     Includes: vehicular, property, and personal injury claims
#     """
    
#     def __init__(self, data_path=None):
#         if data_path is None:
#             # Auto-detect data path
#             project_root = Path(__file__).parent.parent.parent.parent.parent
#             self.data_path = project_root / 'data' / 'mendeley_fraud' / 'insurance_claims.csv'
#         else:
#             self.data_path = Path(data_path)
        
#         self.model = None
#         self.scaler = StandardScaler()
#         self.label_encoders = {}
#         self.feature_names = []
#         self.metrics = {}
        
#     def load_and_preprocess(self):
#         """Load and preprocess the multi-type insurance dataset"""
#         print("\n" + "="*60)
#         print("📊 Loading Multi-Type Insurance Fraud Dataset")
#         print("="*60)
        
#         if not self.data_path.exists():
#             raise FileNotFoundError(f"Dataset not found at {self.data_path}. Run download script first.")
        
#         df = pd.read_csv(self.data_path)
#         print(f"\n✅ Dataset loaded successfully!")
#         print(f"   • Total records: {len(df):,}")
#         print(f"   • Total features: {len(df.columns)}")
        
#         # Identify target column (fraud)
#         target_col = None
#         for col in ['fraud_reported', 'fraud', 'is_fraud', 'fraud_label']:
#             if col in df.columns:
#                 target_col = col
#                 break
        
#         if not target_col:
#             # If no standard fraud column, check for 'claim_status' or similar
#             possible_targets = ['fraud', 'claim_status', 'outcome']
#             for col in possible_targets:
#                 if col in df.columns:
#                     target_col = col
#                     break
        
#         if not target_col:
#             raise ValueError("Could not identify fraud target column")
        
#         print(f"\n🎯 Target column: '{target_col}'")
        
#         # Identify insurance type column
#         type_col = None
#         for col in ['policy_type', 'insurance_type', 'coverage_type', 'product_type']:
#             if col in df.columns:
#                 type_col = col
#                 break
        
#         if type_col:
#             print(f"\n📋 Insurance type column: '{type_col}'")
#             print("\nInsurance type distribution:")
#             type_counts = df[type_col].value_counts()
#             for t, count in type_counts.items():
#                 print(f"   • {t}: {count:,} ({count/len(df)*100:.1f}%)")
        
#         # Separate features and target
#         X = df.drop(columns=[target_col])
#         y = df[target_col]
        
#         # Convert target to binary if needed
#         if y.dtype == 'object':
#             print("\n🔄 Converting target to binary...")
#             y = (y == 'Yes').astype(int)
        
#         # Store feature names
#         self.feature_names = X.columns.tolist()
#         print(f"\n🔧 Total features for training: {len(self.feature_names)}")
        
#         # Handle categorical columns
#         categorical_cols = X.select_dtypes(include=['object', 'category']).columns
#         print(f"   • Categorical features: {len(categorical_cols)}")
        
#         # Encode categorical variables
#         for col in categorical_cols:
#             le = LabelEncoder()
#             X[col] = X[col].fillna('MISSING')
#             X[col] = le.fit_transform(X[col].astype(str))
#             self.label_encoders[col] = le
        
#         # Handle numerical missing values
#         numerical_cols = X.select_dtypes(include=[np.number]).columns
#         imputer = SimpleImputer(strategy='median')
#         X[numerical_cols] = imputer.fit_transform(X[numerical_cols])
        
#         # Scale numerical features
#         print("   • Scaling numerical features...")
#         X_scaled = self.scaler.fit_transform(X)
#         X = pd.DataFrame(X_scaled, columns=X.columns)
        
#         # Final check
#         fraud_rate = y.mean() * 100
#         print(f"\n💰 Final fraud rate: {fraud_rate:.2f}%")
#         print(f"✅ Preprocessing complete. Final shape: {X.shape}")
        
#         return X, y, df[type_col] if type_col else None
    
#     def train_xgboost(self, X_train, y_train, X_val, y_val):
#         """Train XGBoost with hyperparameter tuning"""
#         print("\n" + "="*60)
#         print("🚀 Training XGBoost Model")
#         print("="*60)
        
#         # Calculate class weights
#         scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
#         print(f"\n📊 Class imbalance ratio: {scale_pos_weight:.2f}")
        
#         # Hyperparameter grid optimized for fraud detection
#         param_grid = {
#             'n_estimators': [100, 200, 300],
#             'max_depth': [4, 6, 8, 10],
#             'learning_rate': [0.01, 0.05, 0.1, 0.2],
#             'subsample': [0.6, 0.8, 1.0],
#             'colsample_bytree': [0.6, 0.8, 1.0],
#             'min_child_weight': [1, 3, 5],
#             'gamma': [0, 0.1, 0.2],
#             'scale_pos_weight': [scale_pos_weight],
#             'reg_alpha': [0, 0.1, 0.5],
#             'reg_lambda': [0.5, 1.0, 1.5]
#         }
        
#         # Base model
#         xgb_model = xgb.XGBClassifier(
#             objective='binary:logistic',
#             random_state=42,
#             use_label_encoder=False,
#             eval_metric=['logloss', 'auc'],
#             early_stopping_rounds=20
#         )
        
#         # Stratified K-Fold
#         cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
#         # Randomized search
#         random_search = RandomizedSearchCV(
#             xgb_model,
#             param_distributions=param_grid,
#             n_iter=30,
#             cv=cv,
#             scoring='roc_auc',
#             random_state=42,
#             n_jobs=-1,
#             verbose=1
#         )
        
#         print("\n🔄 Performing hyperparameter search (this may take 5-10 minutes)...")
#         random_search.fit(
#             X_train, y_train,
#             eval_set=[(X_val, y_val)],
#             verbose=False
#         )
        
#         self.model = random_search.best_estimator_
        
#         print(f"\n✅ Best parameters found:")
#         for param, value in random_search.best_params_.items():
#             print(f"   • {param}: {value}")
#         print(f"✅ Best CV Score (ROC-AUC): {random_search.best_score_:.4f}")
        
#         return self.model
    
#     def evaluate_model(self, X_test, y_test, name="Test"):
#         """Evaluate model performance"""
#         print(f"\n📊 {name} Set Performance:")
#         print("-" * 40)
        
#         y_pred = self.model.predict(X_test)
#         y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
#         # Calculate metrics
#         metrics = {
#             'accuracy': accuracy_score(y_test, y_pred),
#             'precision': precision_score(y_test, y_pred),
#             'recall': recall_score(y_test, y_pred),
#             'f1_score': f1_score(y_test, y_pred),
#             'roc_auc': roc_auc_score(y_test, y_pred_proba)
#         }
        
#         print(f"   Accuracy:  {metrics['accuracy']:.4f}")
#         print(f"   Precision: {metrics['precision']:.4f}")
#         print(f"   Recall:    {metrics['recall']:.4f}")
#         print(f"   F1-Score:  {metrics['f1_score']:.4f}")
#         print(f"   ROC-AUC:   {metrics['roc_auc']:.4f}")
        
#         # Confusion matrix
#         cm = confusion_matrix(y_test, y_pred)
#         print(f"\n   Confusion Matrix:")
#         print(f"   ┌──────────────┬──────────────┐")
#         print(f"   │ TN: {cm[0,0]:5d}      │ FP: {cm[0,1]:5d}      │")
#         print(f"   ├──────────────┼──────────────┤")
#         print(f"   │ FN: {cm[1,0]:5d}      │ TP: {cm[1,1]:5d}      │")
#         print(f"   └──────────────┴──────────────┘")
        
#         return metrics
    
#     def save_model(self, filepath="ml_models/fraud_model_multi_type.pkl"):
#         """Save trained model and artifacts"""
#         print(f"\n💾 Saving model to {filepath}...")
        
#         # Ensure directory exists
#         save_path = Path(__file__).parent / filepath
#         save_path.parent.mkdir(parents=True, exist_ok=True)
        
#         model_artifacts = {
#             'model': self.model,
#             'scaler': self.scaler,
#             'label_encoders': self.label_encoders,
#             'feature_names': self.feature_names,
#             'training_date': datetime.now().isoformat(),
#             'dataset': 'Mendeley Multi-Type Insurance Fraud Dataset',
#             'metrics': self.metrics
#         }
        
#         joblib.dump(model_artifacts, save_path)
#         print(f"✅ Model saved to: {save_path}")
        
#         return str(save_path)
    
#     def run_pipeline(self):
#         """Run complete training pipeline"""
        
#         # Load and preprocess data
#         X, y, insurance_types = self.load_and_preprocess()
        
#         # Split data
#         X_train, X_temp, y_train, y_temp = train_test_split(
#             X, y, test_size=0.3, random_state=42, stratify=y
#         )
#         X_val, X_test, y_val, y_test = train_test_split(
#             X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
#         )
        
#         print(f"\n📈 Data Split:")
#         print(f"   • Training:   {len(X_train):,} samples ({len(X_train)/len(X):.1%})")
#         print(f"   • Validation: {len(X_val):,} samples ({len(X_val)/len(X):.1%})")
#         print(f"   • Test:       {len(X_test):,} samples ({len(X_test)/len(X):.1%})")
        
#         # Train model
#         self.train_xgboost(X_train, y_train, X_val, y_val)
        
#         # Evaluate
#         train_metrics = self.evaluate_model(X_train, y_train, "Training")
#         val_metrics = self.evaluate_model(X_val, y_val, "Validation")
#         test_metrics = self.evaluate_model(X_test, y_test, "Test")
        
#         self.metrics = test_metrics
        
#         # Feature importance
#         feature_importance = pd.DataFrame({
#             'feature': self.feature_names,
#             'importance': self.model.feature_importances_
#         }).sort_values('importance', ascending=False)
        
#         print(f"\n📈 Top 10 Most Important Features:")
#         print("-" * 40)
#         for idx, row in feature_importance.head(10).iterrows():
#             print(f"   {row['feature']:30s} : {row['importance']:.4f}")
        
#         # Save model
#         model_path = self.save_model()
        
#         return {
#             'model_path': model_path,
#             'metrics': test_metrics,
#             'train_samples': len(X_train),
#             'val_samples': len(X_val),
#             'test_samples': len(X_test)
#         }

# # ============================================================
# # MAIN EXECUTION
# # ============================================================

# if __name__ == "__main__":
#     print("="*70)
#     print("🚀 MULTI-TYPE INSURANCE FRAUD DETECTION MODEL TRAINING")
#     print("="*70)
    
#     # Run training
#     trainer = MultiTypeFraudTrainer()
#     results = trainer.run_pipeline()
    
#     print("\n" + "="*70)
#     print("✅ TRAINING COMPLETE!")
#     print("="*70)
#     print(f"📊 Final Test Set Performance:")
#     print(f"   • ROC-AUC:   {results['metrics']['roc_auc']:.4f}")
#     print(f"   • F1-Score:  {results['metrics']['f1_score']:.4f}")
#     print(f"   • Precision: {results['metrics']['precision']:.4f}")
#     print(f"   • Recall:    {results['metrics']['recall']:.4f}")
#     print(f"   • Accuracy:  {results['metrics']['accuracy']:.4f}")
#     print(f"\n📁 Model saved to: {results['model_path']}")
#     print("="*70)





# train_multi_type_fraud.py
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix,
                            classification_report)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class MultiTypeFraudTrainer:
    """
    Train XGBoost on insurance fraud dataset
    """
    
    def __init__(self, data_path=None):
        if data_path is None:
            # Auto-detect data path
            project_root = Path(__file__).parent.parent.parent.parent.parent
            possible_paths = [
                project_root / 'data' / 'insurance_claims.csv',
                project_root / 'data' / 'insurance_claims (1).csv',
                project_root / 'data' / 'fraud_oracle.csv',
                project_root / 'data' / 'insurance_fraud_synthetic.csv'
            ]
            
            self.data_path = None
            for path in possible_paths:
                if path.exists():
                    self.data_path = path
                    print(f"✅ Found dataset at: {path}")
                    print(f"   File size: {path.stat().st_size} bytes")
                    break
            
            if self.data_path is None:
                print("\n❌ No dataset found! Please run download script first.")
                print("👉 Run: python force_download_dataset.py")
                self.data_path = None
        else:
            self.data_path = Path(data_path)
        
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.metrics = {}
        
    def load_and_preprocess(self):
        """Load and preprocess the insurance fraud dataset"""
        print("\n" + "="*60)
        print("📊 Loading Insurance Fraud Dataset")
        print("="*60)
        
        if self.data_path is None or not self.data_path.exists():
            raise FileNotFoundError(f"❌ Dataset not found. Please run the download script first.")
        
        print(f"📂 Reading file: {self.data_path}")
        df = pd.read_csv(self.data_path)
        
        print(f"\n✅ Dataset loaded successfully!")
        print(f"   • Total records: {len(df):,}")
        print(f"   • Total features: {len(df.columns)}")
        print(f"\n📋 First 5 columns: {df.columns[:5].tolist()}")
        print(f"\n📊 Data types:\n{df.dtypes.value_counts()}")
        
        # Identify target column (fraud)
        target_col = None
        fraud_keywords = ['fraud', 'is_fraud', 'fraud_reported', 'claim_fraud']
        
        for col in df.columns:
            col_lower = col.lower().replace('_', '').replace(' ', '')
            for keyword in fraud_keywords:
                if keyword in col_lower:
                    target_col = col
                    print(f"\n🎯 Found fraud column: '{target_col}'")
                    break
            if target_col:
                break
        
        if not target_col:
            # If no fraud column, look for binary columns
            binary_cols = [col for col in df.columns if df[col].nunique() == 2]
            if binary_cols:
                target_col = binary_cols[0]
                print(f"⚠️ Using '{target_col}' as target (binary column)")
        
        if not target_col:
            print("\n❌ Could not find fraud column!")
            print(f"Available columns: {list(df.columns)}")
            raise ValueError("Could not identify fraud target column")
        
        # Check target distribution
        fraud_rate = df[target_col].mean() * 100
        print(f"\n💰 Fraud rate: {fraud_rate:.2f}%")
        
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Convert target to binary if needed
        if y.dtype == 'object':
            print("🔄 Converting target to binary...")
            y = (y == 'Y').astype(int) if 'Y' in y.values else (y == 'Yes').astype(int)
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        print(f"\n🔧 Total features for training: {len(self.feature_names)}")
        
        # Handle categorical columns
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns
        print(f"   • Categorical features: {len(categorical_cols)}")
        
        # Encode categorical variables
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = X[col].fillna('MISSING')
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
        
        # Handle numerical missing values
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        imputer = SimpleImputer(strategy='median')
        X[numerical_cols] = imputer.fit_transform(X[numerical_cols])
        
        # Scale numerical features
        print("   • Scaling numerical features...")
        X_scaled = self.scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns)
        
        print(f"✅ Preprocessing complete. Final shape: {X.shape}")
        
        return X, y
    
    def train_xgboost(self, X_train, y_train, X_val, y_val):
        """Train XGBoost with hyperparameter tuning"""
        print("\n" + "="*60)
        print("🚀 Training XGBoost Model")
        print("="*60)
        
        # Calculate class weights
        scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
        print(f"\n📊 Class imbalance ratio: {scale_pos_weight:.2f}")
        
        # Hyperparameter grid
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [4, 6, 8],
            'learning_rate': [0.01, 0.05, 0.1],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0],
            'min_child_weight': [1, 3],
            'scale_pos_weight': [scale_pos_weight]
        }
        
        # Base model
        xgb_model = xgb.XGBClassifier(
            objective='binary:logistic',
            random_state=42,
            use_label_encoder=False,
            eval_metric='auc'
        )
        
        # Stratified K-Fold
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        
        # Randomized search
        random_search = RandomizedSearchCV(
            xgb_model,
            param_distributions=param_grid,
            n_iter=10,
            cv=cv,
            scoring='roc_auc',
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        print("\n🔄 Training model...")
        random_search.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
        
        self.model = random_search.best_estimator_
        
        print(f"\n✅ Best parameters found:")
        for param, value in random_search.best_params_.items():
            print(f"   • {param}: {value}")
        print(f"✅ Best CV Score (ROC-AUC): {random_search.best_score_:.4f}")
        
        return self.model
    
    def evaluate_model(self, X_test, y_test, name="Test"):
        """Evaluate model performance"""
        print(f"\n📊 {name} Set Performance:")
        print("-" * 40)
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
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
        print(f"   ┌──────────────┬──────────────┐")
        print(f"   │ TN: {cm[0,0]:5d}      │ FP: {cm[0,1]:5d}      │")
        print(f"   ├──────────────┼──────────────┤")
        print(f"   │ FN: {cm[1,0]:5d}      │ TP: {cm[1,1]:5d}      │")
        print(f"   └──────────────┴──────────────┘")
        
        return metrics
    
    def save_model(self, filepath="ml_models/fraud_model_multi_type.pkl"):
        """Save trained model and artifacts"""
        print(f"\n💾 Saving model to {filepath}...")
        
        # Ensure directory exists
        save_path = Path(__file__).parent / filepath
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        model_artifacts = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'training_date': datetime.now().isoformat(),
            'dataset': 'Insurance Fraud Dataset',
            'metrics': self.metrics
        }
        
        joblib.dump(model_artifacts, save_path)
        print(f"✅ Model saved to: {save_path}")
        print(f"   File size: {save_path.stat().st_size / 1024:.1f} KB")
        
        return str(save_path)
    
    def run_pipeline(self):
        """Run complete training pipeline"""
        
        # Load and preprocess data
        X, y = self.load_and_preprocess()
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )
        
        print(f"\n📈 Data Split:")
        print(f"   • Training:   {len(X_train):,} samples ({len(X_train)/len(X):.1%})")
        print(f"   • Validation: {len(X_val):,} samples ({len(X_val)/len(X):.1%})")
        print(f"   • Test:       {len(X_test):,} samples ({len(X_test)/len(X):.1%})")
        
        # Train model
        self.train_xgboost(X_train, y_train, X_val, y_val)
        
        # Evaluate
        train_metrics = self.evaluate_model(X_train, y_train, "Training")
        val_metrics = self.evaluate_model(X_val, y_val, "Validation")
        test_metrics = self.evaluate_model(X_test, y_test, "Test")
        
        self.metrics = test_metrics
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n📈 Top 10 Most Important Features:")
        print("-" * 40)
        for idx, row in feature_importance.head(10).iterrows():
            print(f"   {row['feature'][:30]:30s} : {row['importance']:.4f}")
        
        # Save model
        model_path = self.save_model()
        
        return {
            'model_path': model_path,
            'metrics': test_metrics,
            'train_samples': len(X_train),
            'val_samples': len(X_val),
            'test_samples': len(X_test)
        }

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("🚀 INSURANCE FRAUD DETECTION MODEL TRAINING")
    print("="*70)
    
    # Run training
    trainer = MultiTypeFraudTrainer()
    results = trainer.run_pipeline()
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print(f"📊 Final Test Set Performance:")
    print(f"   • ROC-AUC:   {results['metrics']['roc_auc']:.4f}")
    print(f"   • F1-Score:  {results['metrics']['f1_score']:.4f}")
    print(f"   • Precision: {results['metrics']['precision']:.4f}")
    print(f"   • Recall:    {results['metrics']['recall']:.4f}")
    print(f"   • Accuracy:  {results['metrics']['accuracy']:.4f}")
    print(f"\n📁 Model saved to: {results['model_path']}")
    print("="*70)