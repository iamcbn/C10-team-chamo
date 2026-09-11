import os
import zipfile
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
KAGGLE_DIR = Path.home() / ".kaggle"

def verify_kaggle_credentials():
    if not (KAGGLE_DIR / "kaggle.json").exists():
        print(f"ERROR: Kaggle credentials not found at {KAGGLE_DIR / 'kaggle.json'}")
        print("Please download your kaggle.json from Kaggle Account settings and place it in the ~/.kaggle/ directory.")
        return False
    return True

def download_and_extract(dataset_id, extract_path):
    print(f"Downloading {dataset_id}...")
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    
    api.dataset_download_files(dataset_id, path=str(extract_path), unzip=True)
    print(f"Successfully downloaded and extracted {dataset_id} to {extract_path}")

if __name__ == '__main__':
    print("Setting up Data Directories...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if verify_kaggle_credentials():
        try:
            download_and_extract(
                "suchintikasarkar/sentiment-analysis-for-mental-health", 
                DATA_DIR / "sentiment-analysis-for-mental-health"
            )
            download_and_extract(
                "kushagra3204/sentiment-and-emotion-analysis-dataset", 
                DATA_DIR / "sentiment-and-emotion-analysis-dataset"
            )
            print("\nData download complete! Datasets are located in the /data/ directory.")
        except Exception as e:
            print(f"An error occurred during download: {e}")
            print("Make sure you have installed the kaggle library: pip install kaggle")
