"""
Data preprocessing utilities for SmartCart recommendation engine.
"""

from typing import List, Set
import pandas as pd
import numpy as np


def prepare_basket_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare transaction data for Market Basket Analysis.
    Creates a binary matrix where each row is an order and columns are products.
    
    Args:
        df: Transaction DataFrame with columns: order_id, product, quantity
        
    Returns:
        DataFrame with order_id as index and products as columns (binary values)
    """
    # Create binary basket matrix
    basket = df.groupby(['order_id', 'product'])['quantity'].sum().unstack().fillna(0)
    
    # Convert to binary (1 if product in basket, 0 otherwise)
    basket = (basket > 0).astype(int)
    
    return basket


def prepare_user_item_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare user-item interaction matrix for collaborative filtering.
    
    Args:
        df: Transaction DataFrame with columns: customer_id, product, quantity
        
    Returns:
        DataFrame with customer_id as index, products as columns, quantities as values
    """
    # Create user-item matrix with quantities
    user_item = df.groupby(['customer_id', 'product'])['quantity'].sum().unstack(fill_value=0)
    
    return user_item


def get_frequent_itemsets_data(basket_df: pd.DataFrame, min_support: float = 0.1) -> List[Set[str]]:
    """
    Convert basket DataFrame to list of transactions for Apriori algorithm.
    
    Args:
        basket_df: Binary basket matrix (orders x products)
        min_support: Minimum support threshold (not used here, but kept for consistency)
        
    Returns:
        List of sets, where each set contains products in a transaction
    """
    transactions = []
    
    for order_id in basket_df.index:
        # Get products in this order (where value is 1)
        products = set(basket_df.columns[basket_df.loc[order_id] == 1])
        if len(products) > 0:
            transactions.append(products)
    
    return transactions


def normalize_ratings(user_item_df: pd.DataFrame, method: str = 'min_max') -> pd.DataFrame:
    """
    Normalize user-item matrix ratings.
    
    Args:
        user_item_df: User-item matrix
        method: Normalization method ('min_max' or 'z_score')
        
    Returns:
        Normalized user-item matrix
    """
    if method == 'min_max':
        # Min-max normalization to [0, 1]
        min_val = user_item_df.min().min()
        max_val = user_item_df.max().max()
        if max_val > min_val:
            normalized = (user_item_df - min_val) / (max_val - min_val)
        else:
            normalized = user_item_df
    elif method == 'z_score':
        # Z-score normalization
        mean_val = user_item_df.mean().mean()
        std_val = user_item_df.std().std()
        if std_val > 0:
            normalized = (user_item_df - mean_val) / std_val
        else:
            normalized = user_item_df
    else:
        normalized = user_item_df
    
    return normalized


def filter_sparse_users_items(user_item_df: pd.DataFrame, 
                              min_user_interactions: int = 1,
                              min_item_interactions: int = 1) -> pd.DataFrame:
    """
    Filter out users and items with too few interactions.
    
    Args:
        user_item_df: User-item matrix
        min_user_interactions: Minimum interactions per user
        min_item_interactions: Minimum interactions per item
        
    Returns:
        Filtered user-item matrix
    """
    # Filter users
    user_counts = (user_item_df > 0).sum(axis=1)
    valid_users = user_counts[user_counts >= min_user_interactions].index
    filtered_df = user_item_df.loc[valid_users]
    
    # Filter items
    item_counts = (filtered_df > 0).sum(axis=0)
    valid_items = item_counts[item_counts >= min_item_interactions].index
    filtered_df = filtered_df[valid_items]
    
    return filtered_df

