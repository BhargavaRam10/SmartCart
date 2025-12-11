"""
Collaborative Filtering recommendation engine with content-based fallback.
"""

from typing import List, Dict, Optional, Tuple, Any
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
import warnings
warnings.filterwarnings('ignore')


class RecommenderEngine:
    """
    Collaborative Filtering recommendation engine with fallback strategies.
    """
    
    def __init__(self, n_components: int = 10, n_recommendations: int = 10):
        """
        Initialize Recommender Engine.
        
        Args:
            n_components: Number of components for matrix factorization
            n_recommendations: Default number of recommendations to return
        """
        self.n_components = n_components
        self.n_recommendations = n_recommendations
        self.user_item_matrix = None
        self.model = None
        self.user_similarity = None
        self.item_similarity = None
        self.user_ids = None
        self.item_ids = None
        
    def fit(self, user_item_df: pd.DataFrame) -> None:
        """
        Fit the recommendation model on user-item matrix.
        
        Args:
            user_item_df: User-item matrix with customer_id as index and products as columns
        """
        self.user_item_matrix = user_item_df.copy()
        self.user_ids = user_item_df.index.values
        self.item_ids = user_item_df.columns.values
        
        # Normalize the matrix (handle zeros)
        matrix = user_item_df.values
        matrix_normalized = matrix / (matrix.max() + 1e-8)  # Avoid division by zero
        
        # Compute user-user similarity
        self.user_similarity = cosine_similarity(matrix_normalized)
        
        # Compute item-item similarity
        self.item_similarity = cosine_similarity(matrix_normalized.T)
        
        # Fit NMF model for matrix factorization
        try:
            self.model = NMF(n_components=min(self.n_components, min(matrix.shape) - 1), 
                           random_state=42, max_iter=500)
            self.model.fit(matrix_normalized)
        except Exception as e:
            # Fallback if NMF fails
            self.model = None
    
    def get_user_recommendations(self, customer_id: int, n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get personalized recommendations for a customer.
        
        Args:
            customer_id: Customer ID
            n: Number of recommendations (defaults to self.n_recommendations)
            
        Returns:
            List of recommendation dictionaries with product and score
        """
        if n is None:
            n = self.n_recommendations
        
        if self.user_item_matrix is None:
            return []
        
        # Check if customer exists
        if customer_id not in self.user_ids:
            return self._get_cold_start_recommendations(n)
        
        # Get user index
        user_idx = np.where(self.user_ids == customer_id)[0][0]
        
        # Get user's current purchases
        user_vector = self.user_item_matrix.iloc[user_idx].values
        
        # Method 1: User-based collaborative filtering
        user_sim_scores = self.user_similarity[user_idx]
        
        # Weight items by similarity to similar users
        weighted_items = np.dot(user_sim_scores, self.user_item_matrix.values)
        
        # Method 2: Matrix factorization (if available)
        if self.model is not None:
            try:
                user_features = self.model.transform([user_vector])
                item_features = self.model.components_.T
                mf_scores = np.dot(user_features, item_features.T)[0]
                # Combine both methods
                final_scores = 0.6 * weighted_items + 0.4 * mf_scores
            except:
                final_scores = weighted_items
        else:
            final_scores = weighted_items
        
        # Remove items already purchased
        final_scores[user_vector > 0] = -np.inf
        
        # Get top N recommendations
        top_indices = np.argsort(final_scores)[::-1][:n]
        
        recommendations = []
        for idx in top_indices:
            if final_scores[idx] > 0:
                recommendations.append({
                    'product': self.item_ids[idx],
                    'score': float(final_scores[idx]),
                    'reasoning': 'Collaborative filtering based on similar users'
                })
        
        # If not enough recommendations, use content-based fallback
        if len(recommendations) < n:
            content_recs = self._get_content_based_recommendations(customer_id, n - len(recommendations))
            recommendations.extend(content_recs)
        
        return recommendations[:n]
    
    def _get_content_based_recommendations(self, customer_id: int, n: int) -> List[Dict[str, Any]]:
        """
        Content-based recommendations using item similarity.
        
        Args:
            customer_id: Customer ID
            n: Number of recommendations
            
        Returns:
            List of recommendation dictionaries
        """
        if customer_id not in self.user_ids:
            return []
        
        user_idx = np.where(self.user_ids == customer_id)[0][0]
        user_vector = self.user_item_matrix.iloc[user_idx].values
        
        # Get items user has purchased
        purchased_indices = np.where(user_vector > 0)[0]
        
        if len(purchased_indices) == 0:
            return []
        
        # Aggregate similarity scores from purchased items
        item_scores = np.zeros(len(self.item_ids))
        
        for purchased_idx in purchased_indices:
            item_scores += self.item_similarity[purchased_idx] * user_vector[purchased_idx]
        
        # Remove already purchased items
        item_scores[purchased_indices] = -np.inf
        
        # Get top N
        top_indices = np.argsort(item_scores)[::-1][:n]
        
        recommendations = []
        for idx in top_indices:
            if item_scores[idx] > 0:
                recommendations.append({
                    'product': self.item_ids[idx],
                    'score': float(item_scores[idx]),
                    'reasoning': 'Content-based: similar to your purchases'
                })
        
        return recommendations
    
    def _get_cold_start_recommendations(self, n: int) -> List[Dict[str, Any]]:
        """
        Get recommendations for cold-start users (new users with no history).
        
        Args:
            n: Number of recommendations
            
        Returns:
            List of popular product recommendations
        """
        if self.user_item_matrix is None:
            return []
        
        # Get most popular products
        product_popularity = self.user_item_matrix.sum(axis=0).sort_values(ascending=False)
        
        recommendations = []
        for product, score in product_popularity.head(n).items():
            recommendations.append({
                'product': product,
                'score': float(score),
                'reasoning': 'Popular items: trending products'
            })
        
        return recommendations
    
    def get_similar_users(self, customer_id: int, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get users similar to a given customer.
        
        Args:
            customer_id: Customer ID
            n: Number of similar users to return
            
        Returns:
            List of similar user dictionaries
        """
        if customer_id not in self.user_ids:
            return []
        
        user_idx = np.where(self.user_ids == customer_id)[0][0]
        user_sim_scores = self.user_similarity[user_idx]
        
        # Get top N similar users (excluding self)
        top_indices = np.argsort(user_sim_scores)[::-1][1:n+1]
        
        similar_users = []
        for idx in top_indices:
            similar_users.append({
                'customer_id': int(self.user_ids[idx]),
                'similarity': float(user_sim_scores[idx])
            })
        
        return similar_users
    
    def get_similar_products(self, product: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get products similar to a given product.
        
        Args:
            product: Product name
            n: Number of similar products to return
            
        Returns:
            List of similar product dictionaries
        """
        if product not in self.item_ids:
            return []
        
        product_idx = np.where(self.item_ids == product)[0][0]
        product_sim_scores = self.item_similarity[product_idx]
        
        # Get top N similar products (excluding self)
        top_indices = np.argsort(product_sim_scores)[::-1][1:n+1]
        
        similar_products = []
        for idx in top_indices:
            similar_products.append({
                'product': self.item_ids[idx],
                'similarity': float(product_sim_scores[idx])
            })
        
        return similar_products

