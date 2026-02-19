# train_with_correct_path.py
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
from pathlib import Path

print("="*70)
print("🚀 TRAINING WITH CORRECT PATH")
print("="*70)

# ============================================================
# CORRECT PATH
# ============================================================
data_path = Path("app/data/insurance_claims.csv")

if not data_path.exists():
    print(f"❌ File not found at: {data_path.absolute()}")
    exit(1)

print(f"✅ Found dataset at: {data_path.absolute()}")
print(f"   File size: {data_path.stat().st_size / 1024:.1f} KB")

# ============================================================
# LOAD DATASET
# ============================================================
df = pd.read_csv(data_path)
print(f"\n📊 Dataset loaded:")
print(f"   • Records: {len(df):,}")
print(f"   • Columns: {len(df.columns)}")
print(f"   • Column names: {df.columns[:10].tolist()}...")

# ============================================================
# FIND TARGET COLUMN
# ============================================================
target_col = None
for col in df.columns:
    if 'fraud' in col.lower():
        target_col = col
        break

if target_col is None:
    print("\n❌ No fraud column found!")
    exit(1)

print(f"\n🎯 Target column: '{target_col}'")
print(f"   Unique values: {df[target_col].unique()}")

# ============================================================
# CONVERT TARGET TO NUMERIC (FIX FOR THE ERROR)
# ============================================================
# Convert common string labels to numeric (supports Arrow string dtype)
raw_target = df[target_col]
if pd.api.types.is_numeric_dtype(raw_target):
    y = raw_target.astype(float)
else:
    normalized = raw_target.astype(str).str.strip().str.upper()
    mapping = {
        "Y": 1,
        "N": 0,
        "YES": 1,
        "NO": 0,
        "TRUE": 1,
        "FALSE": 0,
        "1": 1,
        "0": 0,
    }
    y = normalized.map(mapping)

    if y.isna().any():
        unknown_values = sorted(normalized[y.isna()].unique().tolist())
        raise ValueError(f"Unsupported target labels in '{target_col}': {unknown_values}")

    y = y.astype(int)
    print(f"   Converted '{target_col}' to numeric labels (0/1)")

fraud_rate = y.mean() * 100
print(f"   Fraud rate: {fraud_rate:.2f}%")
print(f"   • Legitimate (0): {(y == 0).sum():,}")
print(f"   • Fraudulent (1): {(y == 1).sum():,}")

# ============================================================
# PREPROCESS FEATURES
# ============================================================
print(f"\n🛠️ Preprocessing features...")

# Separate features
X = df.drop(columns=[target_col])

# Handle categorical columns
label_encoders = {}
categorical_cols = X.select_dtypes(include=['object']).columns
print(f"   • Categorical columns: {len(categorical_cols)}")

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Fill missing values
X = X.fillna(X.median())

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

print(f"   • Features shape: {X_scaled.shape}")

# ============================================================
# TRAIN-TEST SPLIT
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 Data split:")
print(f"   • Training: {len(X_train):,} samples")
print(f"   • Test: {len(X_test):,} samples")

# ============================================================
# TRAIN XGBOOST
# ============================================================
print(f"\n🚀 Training XGBoost model...")

model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

model.fit(X_train, y_train)

# ============================================================
# EVALUATE
# ============================================================
print(f"\n📊 Model Performance:")

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'f1_score': f1_score(y_test, y_pred),
    'roc_auc': roc_auc_score(y_test, y_proba)
}

for metric, value in metrics.items():
    print(f"   • {metric}: {value:.4f}")

# ============================================================
# FEATURE IMPORTANCE
# ============================================================
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n📈 Top 10 Most Important Features:")
print("-" * 50)
for i, row in feature_importance.head(10).iterrows():
    print(f"   {row['feature'][:30]:30s} : {row['importance']:.4f}")

# ============================================================
# SAVE MODEL
# ============================================================
model_dir = Path("app/agents/node4_fraud_agent/ml_models")
model_dir.mkdir(parents=True, exist_ok=True)
model_path = model_dir / "fraud_model_multi_type.pkl"

model_artifacts = {
    'model': model,
    'scaler': scaler,
    'label_encoders': label_encoders,
    'feature_names': X.columns.tolist(),
    'metrics': metrics,
    'training_date': pd.Timestamp.now().isoformat()
}

joblib.dump(model_artifacts, model_path)
print(f"\n✅ Model saved to: {model_path}")
print(f"   File size: {model_path.stat().st_size / 1024:.1f} KB")

print("\n" + "="*70)
print("✅ TRAINING COMPLETE!")
print("="*70)