import kagglehub
import pandas as pd
import os

def download_netflix_dataset():
    """Download the Netflix dataset from Kaggle"""
    try:
        # Download latest version
        path = kagglehub.dataset_download("shivamb/netflix-shows")
        print("Path to dataset files:", path)
        
        # List files in the downloaded path
        files = os.listdir(path)
        print("Files in dataset:", files)
        
        # Load the dataset
        csv_file = None
        for file in files:
            if file.endswith('.csv'):
                csv_file = os.path.join(path, file)
                break
        
        if csv_file:
            df = pd.read_csv(csv_file)
            print(f"\nDataset shape: {df.shape}")
            print(f"\nColumns: {df.columns.tolist()}")
            print(f"\nFirst few rows:")
            print(df.head())
            
            # Save a local copy for easy access
            local_path = "netflix_titles.csv"
            df.to_csv(local_path, index=False)
            print(f"\nDataset saved locally as: {local_path}")
            
            return df, local_path
        else:
            print("No CSV file found in the downloaded dataset")
            return None, None
            
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None, None

if __name__ == "__main__":
    df, local_path = download_netflix_dataset()
