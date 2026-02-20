# force_download_dataset.py
import requests
import zipfile
import io
import pandas as pd
from pathlib import Path

def force_download():
    print("="*60)
    print("📥 FORCE DOWNLOAD: Insurance Claims Dataset")
    print("="*60)
    
    # Setup paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # DIRECT DOWNLOAD LINK (100% working)
    url = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/992mh7dk9y-2.zip"
    
    print(f"\n📂 Downloading from Mendeley...")
    print(f"   URL: {url}")
    
    try:
        # Download the file
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        # Save zip file
        zip_path = data_dir / 'dataset.zip'
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Download complete! File saved to: {zip_path}")
        print(f"   Size: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # Extract the zip file
        print(f"\n📦 Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
            print(f"   Files extracted to: {data_dir}")
            
            # Show extracted files
            files = zip_ref.namelist()
            for f in files:
                print(f"   • {f}")
        
        # Find the CSV file
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            csv_path = csv_files[0]
            print(f"\n✅ Found CSV file: {csv_path}")
            
            # Verify it has data
            df = pd.read_csv(csv_path)
            print(f"\n📊 DATASET VERIFICATION:")
            print(f"   • Rows: {len(df)}")
            print(f"   • Columns: {len(df.columns)}")
            print(f"   • Column names: {list(df.columns[:5])}...")
            
            # Check for fraud column
            fraud_cols = ['fraud_reported', 'fraud', 'is_fraud']
            found = None
            for col in fraud_cols:
                if col in df.columns:
                    found = col
                    break
            
            if found:
                fraud_rate = df[found].mean() * 100
                print(f"   • Fraud column: '{found}'")
                print(f"   • Fraud rate: {fraud_rate:.2f}%")
            
            return csv_path
        else:
            print("❌ No CSV file found in the extracted contents!")
            return None
            
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return None

if __name__ == "__main__":
    csv_file = force_download()
    
    if csv_file:
        print(f"\n🎯 Dataset ready at: {csv_file}")
        print("\n👉 Now run your training script:")
        print(f"   python app/agents/node4_fraud_agent/ml_models/train_multi_type_fraud.py")
    else:
        print("\n❌ Download failed. Please check your internet connection.")