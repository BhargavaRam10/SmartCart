"""
Utility functions for SmartCart recommendation engine.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np


def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that a DataFrame contains all required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        True if all columns exist, False otherwise
    """
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return True


def calculate_basic_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate basic metrics from transaction data.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        Dictionary with calculated metrics
    """
    metrics = {
        'total_orders': df['order_id'].nunique(),
        'total_customers': df['customer_id'].nunique(),
        'total_products': df['product'].nunique(),
        'total_transactions': len(df),
        'avg_items_per_order': df.groupby('order_id')['quantity'].sum().mean(),
        'top_products': df.groupby('product')['quantity'].sum().sort_values(ascending=False).head(10).to_dict()
    }
    return metrics


def format_currency(value: float) -> str:
    """
    Format a numeric value as currency.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted currency string
    """
    return f"${value:,.2f}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return if division by zero
        
    Returns:
        Division result or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator


def get_product_stats(df: pd.DataFrame, product: str) -> Dict[str, Any]:
    """
    Get statistics for a specific product.
    
    Args:
        df: Transaction DataFrame
        product: Product name
        
    Returns:
        Dictionary with product statistics
    """
    product_df = df[df['product'] == product]
    
    stats = {
        'total_orders': product_df['order_id'].nunique(),
        'total_quantity': product_df['quantity'].sum(),
        'unique_customers': product_df['customer_id'].nunique(),
        'avg_quantity_per_order': product_df.groupby('order_id')['quantity'].sum().mean()
    }
    
    return stats

