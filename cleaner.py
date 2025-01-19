import pandas as pd

def check_data_types(file_path):
    """Load a CSV file and print the data types of each column."""
    df = pd.read_csv(file_path, dtype=str)  # Force all columns to be read as strings
    print(f"Data types in '{file_path}':")
    print(df.dtypes)

if __name__ == "__main__":
    check_data_types('largeds_cleaned.csv')  # Change to your specific file if needed
    check_data_types('frontds_cleaned.csv')  # Change to your specific file if needed