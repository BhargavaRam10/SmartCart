"""
Market Basket Analysis engine using Apriori algorithm.
"""

from typing import List, Dict, Tuple, Set, Any
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


class MBAEngine:
    """
    Market Basket Analysis engine using Apriori algorithm.
    """
    
    def __init__(self, min_support: float = 0.1, min_confidence: float = 0.5):
        """
        Initialize MBA Engine.
        
        Args:
            min_support: Minimum support threshold for frequent itemsets
            min_confidence: Minimum confidence threshold for association rules
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = None
        self.rules = None
        self.basket_df = None
        
    def fit(self, basket_df: pd.DataFrame) -> None:
        """
        Fit the MBA model on basket data.
        
        Args:
            basket_df: Binary basket matrix (orders x products)
        """
        self.basket_df = basket_df
        
        # Generate frequent itemsets using Apriori
        self.frequent_itemsets = apriori(
            basket_df, 
            min_support=self.min_support, 
            use_colnames=True
        )
        
        # Generate association rules
        if len(self.frequent_itemsets) > 0:
            self.rules = association_rules(
                self.frequent_itemsets,
                metric="confidence",
                min_threshold=self.min_confidence
            )
        else:
            self.rules = pd.DataFrame()
    
    def get_top_rules(self, n: int = 10, metric: str = 'lift', ascending: bool = False) -> pd.DataFrame:
        """
        Get top N association rules by a specified metric.
        
        Args:
            n: Number of rules to return
            metric: Metric to sort by ('lift', 'confidence', 'support')
            ascending: Sort order
            
        Returns:
            DataFrame with top N rules
        """
        if self.rules is None or len(self.rules) == 0:
            return pd.DataFrame()
        
        if metric not in self.rules.columns:
            metric = 'lift'
        
        top_rules = self.rules.nlargest(n, metric) if not ascending else self.rules.nsmallest(n, metric)
        return top_rules
    
    def get_product_recommendations(self, product: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get product recommendations based on association rules.
        
        Args:
            product: Product name to get recommendations for
            n: Number of recommendations to return
            
        Returns:
            List of recommendation dictionaries with product, confidence, and lift
        """
        if self.rules is None or len(self.rules) == 0:
            return []
        
        # Filter rules where product is in antecedents
        product_rules = self.rules[
            self.rules['antecedents'].apply(lambda x: product in x if isinstance(x, frozenset) else False)
        ]
        
        if len(product_rules) == 0:
            return []
        
        # Extract consequents and aggregate by confidence/lift
        recommendations = []
        seen_products = set()
        
        # Sort by lift (descending)
        product_rules = product_rules.sort_values('lift', ascending=False)
        
        for _, rule in product_rules.iterrows():
            consequents = rule['consequents']
            if isinstance(consequents, frozenset):
                for consequent in consequents:
                    if consequent != product and consequent not in seen_products:
                        recommendations.append({
                            'product': consequent,
                            'confidence': rule['confidence'],
                            'lift': rule['lift'],
                            'support': rule['support']
                        })
                        seen_products.add(consequent)
                        if len(recommendations) >= n:
                            break
            
            if len(recommendations) >= n:
                break
        
        return recommendations
    
    def get_frequently_bought_together(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get frequently bought together product pairs.
        
        Args:
            n: Number of pairs to return
            
        Returns:
            List of dictionaries with product pairs and metrics
        """
        if self.rules is None or len(self.rules) == 0:
            return []
        
        # Filter rules with single item antecedents and consequents
        pairs = []
        
        for _, rule in self.rules.iterrows():
            antecedents = rule['antecedents']
            consequents = rule['consequents']
            
            if isinstance(antecedents, frozenset) and isinstance(consequents, frozenset):
                if len(antecedents) == 1 and len(consequents) == 1:
                    pair = {
                        'product_a': list(antecedents)[0],
                        'product_b': list(consequents)[0],
                        'confidence': rule['confidence'],
                        'lift': rule['lift'],
                        'support': rule['support']
                    }
                    pairs.append(pair)
        
        # Sort by lift and return top N
        pairs = sorted(pairs, key=lambda x: x['lift'], reverse=True)
        return pairs[:n]
    
    def get_top_bundles(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get top product bundles (itemsets with multiple items).
        
        Args:
            n: Number of bundles to return
            
        Returns:
            List of dictionaries with bundle information
        """
        if self.frequent_itemsets is None or len(self.frequent_itemsets) == 0:
            return []
        
        # Filter itemsets with 2+ items
        bundles = []
        
        for _, itemset in self.frequent_itemsets.iterrows():
            items = itemset['itemsets']
            if isinstance(items, frozenset) and len(items) >= 2:
                bundle = {
                    'products': list(items),
                    'support': itemset['support'],
                    'size': len(items)
                }
                bundles.append(bundle)
        
        # Sort by support and return top N
        bundles = sorted(bundles, key=lambda x: x['support'], reverse=True)
        return bundles[:n]
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of association rules.
        
        Returns:
            Dictionary with summary metrics
        """
        if self.rules is None or len(self.rules) == 0:
            return {
                'total_rules': 0,
                'avg_confidence': 0,
                'avg_lift': 0,
                'max_lift': 0
            }
        
        return {
            'total_rules': len(self.rules),
            'avg_confidence': self.rules['confidence'].mean(),
            'avg_lift': self.rules['lift'].mean(),
            'max_lift': self.rules['lift'].max(),
            'min_confidence': self.rules['confidence'].min(),
            'max_confidence': self.rules['confidence'].max()
        }

