import pandas as pd
import os


def load_csv(file_path):
    """
    Load a CSV file using pandas.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: The loaded dataframe
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        Exception: For other pandas-related errors
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        print(f"Successfully loaded CSV file: {file_path}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        return df
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        raise


def load_csv_with_options(file_path, **kwargs):
    """
    Load a CSV file with custom pandas options.
    
    Args:
        file_path (str): Path to the CSV file
        **kwargs: Additional arguments to pass to pd.read_csv()
        
    Returns:
        pd.DataFrame: The loaded dataframe
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        df = pd.read_csv(file_path, **kwargs)
        
        print(f"Successfully loaded CSV file with custom options: {file_path}")
        print(f"Shape: {df.shape}")
        
        return df
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        raise


def load_sales_data():
    """
    Load the sales performance data CSV file from the current directory.
    
    Returns:
        pd.DataFrame: The loaded sales performance dataframe
    """
    file_path = "sales_performance_data.csv"
    return load_csv(file_path)


if __name__ == "__main__":
    # Example usage - load the sales data
    try:
        sales_df = load_sales_data()
        print("\nFirst few rows of the data:")
        print(sales_df.head())
        print("\nData info:")
        print(sales_df.info())
    except Exception as e:
        print(f"Failed to load sales data: {e}")
