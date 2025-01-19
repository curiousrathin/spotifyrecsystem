import pandas as pd

def permanently_convert_to_strings(file_paths):
    """Permanently convert CSV files to use string values."""
    for file_path in file_paths:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert all columns to strings
        df = df.astype(str)
        
        # Save back to CSV with string values
        df.to_csv(file_path, index=False, quoting=1)  # quoting=1 ensures all fields are quoted
        print(f"Converted {file_path} to strings")
        
        # Verify the conversion
        df_check = pd.read_csv(file_path, dtype=str)
        print(f"Verification of {file_path} data types:")
        print(df_check.dtypes)
        print("\n")

if __name__ == "__main__":
    files = ['largeds_cleaned.csv', 'frontds_cleaned.csv']
    permanently_convert_to_strings(files)