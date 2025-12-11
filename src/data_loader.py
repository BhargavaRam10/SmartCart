"""
Data loading utilities for SmartCart recommendation engine.
"""

from typing import Optional, Tuple
import pandas as pd
import os


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Load transaction data from CSV file.
    
    Args:
        file_path: Path to the transactions CSV file
        
    Returns:
        DataFrame with transaction data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Transaction file not found: {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Validate required columns
    required_columns = ['order_id', 'product', 'quantity', 'customer_id']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Basic data cleaning
    df = df.dropna(subset=['order_id', 'product', 'customer_id'])
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    
    return df


def load_customers(file_path: str) -> pd.DataFrame:
    """
    Load customer data from CSV file.
    
    Args:
        file_path: Path to the customers CSV file
        
    Returns:
        DataFrame with customer data
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Customer file not found: {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Basic data cleaning
    if 'customer_id' in df.columns:
        df = df.dropna(subset=['customer_id'])
    
    return df


def load_sample_data(data_dir: str = 'data') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load sample transaction and customer data.
    
    Args:
        data_dir: Directory containing data files
        
    Returns:
        Tuple of (transactions_df, customers_df)
    """
    transactions_path = os.path.join(data_dir, 'sample_transactions.csv')
    customers_path = os.path.join(data_dir, 'sample_customers.csv')
    
    transactions_df = load_transactions(transactions_path)
    customers_df = load_customers(customers_path)
    
    return transactions_df, customers_df


def validate_customer_id(df: pd.DataFrame, customer_id: int) -> bool:
    """
    Check if a customer ID exists in the transaction data.
    
    Args:
        df: Transaction DataFrame
        customer_id: Customer ID to validate
        
    Returns:
        True if customer exists, False otherwise
    """
    return customer_id in df['customer_id'].values

