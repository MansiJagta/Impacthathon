# download_multi_type_dataset.py
import requests
import zipfile
import os
import pandas as pd
from pathlib import Path
import sys

def download_mendeley_dataset():
    """Download the multi-type insurance fraud dataset from Mendeley"""
    
    print("="*60)
    print("📥 Multi-Type Insurance Fraud Dataset Downloader")
    print("="*60)
    
    # Create data directory
    project_root = Path(__file__).parent.parent.parent.parent.parent
    data_dir = project_root / 'data' / 'mendeley_fraud'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Mendeley dataset URL
    url = "https://data.mendeley.com/public-files/datasets/992mh7dk9y/files/6bc5b7c5-9b2d-4893-b0fd-36a845bf117b/file_downloaded"
    
    output_path = data_dir / "insurance_claims.csv"
    
    print(f"\n📂 Download location: {output_path}")
    print("\n🔄 Downloading dataset (this may take a minute)...")
    
    try:
        # Download with progress
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\r   Progress: {percent:.1f}%", end='')
        
        print(f"\n\n✅ Dataset downloaded successfully!")
        
        # Load and verify
        print("\n🔍 Verifying dataset...")
        df = pd.read_csv(output_path)
        
        print(f"\n📊 Dataset Info:")
        print(f"   • Total records: {len(df):,}")
        print(f"   • Total columns: {len(df.columns)}")
        print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        # Show column preview
        print(f"\n📋 First 10 columns:")
        for i, col in enumerate(df.columns[:10]):
            print(f"   {i+1:2d}. {col}")
        
        # Check for fraud column
        fraud_cols = ['fraud_reported', 'fraud', 'is_fraud']
        found_fraud = None
        for col in fraud_cols:
            if col in df.columns:
                found_fraud = col
                break
        
        if found_fraud:
            fraud_rate = df[found_fraud].mean() * 100
            print(f"\n💰 Fraud rate: {fraud_rate:.2f}%")
        
        # Check for insurance type column
        type_cols = ['policy_type', 'insurance_type', 'coverage_type']
        found_type = None
        for col in type_cols:
            if col in df.columns:
                found_type = col
                break
        
        if found_type:
            print(f"\n📋 Insurance type distribution:")
            type_counts = df[found_type].value_counts()
            for type_name, count in type_counts.items():
                print(f"   • {type_name}: {count:,} ({count/len(df)*100:.1f}%)")
        
        print(f"\n✅ Dataset ready for training!")
        print(f"   Location: {output_path}")
        
        return str(output_path)
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        print("\n💡 Alternative: You can manually download from:")
        print("   https://data.mendeley.com/datasets/992mh7dk9y")
        return None

if __name__ == "__main__":
    download_mendeley_dataset()