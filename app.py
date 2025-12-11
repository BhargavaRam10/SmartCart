"""
SmartCart: E-Commerce Recommendation Engine
Streamlit Application
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import load_transactions, load_customers, load_sample_data, validate_customer_id
from preprocessing import prepare_basket_data, prepare_user_item_matrix
from mba_engine import MBAEngine
from recommender import RecommenderEngine
from visualizations import (
    create_association_rules_heatmap,
    create_product_network_graph,
    create_top_bundles_chart,
    create_frequently_bought_together_chart,
    create_product_popularity_chart,
    create_correlation_heatmap
)
from utils import calculate_basic_metrics, get_product_stats

# Page configuration
st.set_page_config(
    page_title="SmartCart - E-Commerce Recommendation Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(uploaded_file=None):
    """Load and cache transaction data."""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        transactions_df, _ = load_sample_data()
        return transactions_df


@st.cache_resource
def initialize_models(transactions_df):
    """Initialize and cache MBA and Recommender models."""
    # Prepare data
    basket_df = prepare_basket_data(transactions_df)
    user_item_df = prepare_user_item_matrix(transactions_df)
    
    # Initialize models
    mba_engine = MBAEngine(min_support=0.1, min_confidence=0.3)
    mba_engine.fit(basket_df)
    
    recommender = RecommenderEngine(n_components=5, n_recommendations=10)
    recommender.fit(user_item_df)
    
    return mba_engine, recommender, basket_df, user_item_df


def main():
    """Main application function."""
    
    # Sidebar navigation
    st.sidebar.title("🛒 SmartCart")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Navigate",
        ["Home", "Market Basket Analysis", "Personalized Recommendations", "Insights Dashboard"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Options")
    use_sample = st.sidebar.checkbox("Use Sample Data", value=True)
    
    uploaded_file = None
    if not use_sample:
        uploaded_file = st.sidebar.file_uploader(
            "Upload Transaction CSV",
            type=['csv'],
            help="CSV should have columns: order_id, product, quantity, customer_id"
        )
    
    # Load data
    if use_sample or uploaded_file is not None:
        try:
            with st.spinner("Loading data..."):
                transactions_df = load_data(uploaded_file)
                
            # Initialize models
            with st.spinner("Initializing models..."):
                mba_engine, recommender, basket_df, user_item_df = initialize_models(transactions_df)
            
            # Route to appropriate page
            if page == "Home":
                show_home_page(transactions_df)
            elif page == "Market Basket Analysis":
                show_mba_page(mba_engine, transactions_df, basket_df)
            elif page == "Personalized Recommendations":
                show_recommendations_page(recommender, transactions_df)
            elif page == "Insights Dashboard":
                show_dashboard_page(mba_engine, transactions_df, basket_df)
                
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.info("Please check your data format or use sample data.")
    else:
        st.info("👈 Please upload a CSV file or use sample data to get started.")


def show_home_page(transactions_df):
    """Display home page."""
    st.markdown('<div class="main-header">🛒 SmartCart</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">E-Commerce Recommendation Engine</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Overview
    st.header("📋 Overview")
    st.markdown("""
    **SmartCart** is a comprehensive prescriptive analytics product for e-commerce that combines:
    
    - **Market Basket Analysis (Apriori Algorithm)**: Identifies product associations and frequently bought together items
    - **Collaborative Filtering**: Provides personalized product recommendations based on user behavior
    - **Insights Dashboard**: Visualizes trends, bundles, and product relationships
    
    ### How It Works
    
    1. **Market Basket Analysis**: Uses the Apriori algorithm to find association rules between products.
       - **Support**: How frequently items appear together
       - **Confidence**: Probability that item Y is purchased given item X
       - **Lift**: How much more likely Y is purchased when X is purchased
    
    2. **Collaborative Filtering**: Recommends products based on similar users' preferences.
       - User-based filtering: Finds users with similar purchase patterns
       - Matrix factorization: Decomposes user-item interactions
       - Content-based fallback: For new users with no purchase history
    
    3. **Prescriptive Insights**: Provides actionable recommendations:
       - "Customers who bought X also buy..."
       - "Best bundle options to increase cross-sell"
       - "Recommended products for Customer 123"
    """)
    
    # Metrics
    st.markdown("---")
    st.header("📊 Dataset Statistics")
    
    metrics = calculate_basic_metrics(transactions_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", metrics['total_orders'])
    with col2:
        st.metric("Total Customers", metrics['total_customers'])
    with col3:
        st.metric("Total Products", metrics['total_products'])
    with col4:
        st.metric("Total Transactions", metrics['total_transactions'])
    
    st.metric("Average Items per Order", f"{metrics['avg_items_per_order']:.2f}")
    
    # Top Products
    st.markdown("---")
    st.header("🏆 Top Products")
    top_products_df = pd.DataFrame(
        list(metrics['top_products'].items()),
        columns=['Product', 'Total Quantity']
    )
    st.dataframe(top_products_df, use_container_width=True)


def show_mba_page(mba_engine, transactions_df, basket_df):
    """Display Market Basket Analysis page."""
    st.header("🛍️ Market Basket Analysis")
    st.markdown("Analyze product associations and generate recommendations based on purchase patterns.")
    
    # Parameters
    col1, col2 = st.columns(2)
    with col1:
        min_support = st.slider("Minimum Support", 0.05, 0.5, 0.1, 0.05)
    with col2:
        min_confidence = st.slider("Minimum Confidence", 0.1, 1.0, 0.3, 0.05)
    
    # Reinitialize if parameters changed
    if min_support != mba_engine.min_support or min_confidence != mba_engine.min_confidence:
        with st.spinner("Updating model..."):
            mba_engine.min_support = min_support
            mba_engine.min_confidence = min_confidence
            mba_engine.fit(basket_df)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Association Rules", 
        "Product Recommendations", 
        "Visualizations",
        "Export Results"
    ])
    
    with tab1:
        st.subheader("Association Rules")
        
        n_rules = st.slider("Number of Rules to Display", 5, 50, 10)
        metric = st.selectbox("Sort by Metric", ["lift", "confidence", "support"])
        
        top_rules = mba_engine.get_top_rules(n=n_rules, metric=metric)
        
        if len(top_rules) > 0:
            # Format rules for display
            display_rules = top_rules.copy()
            display_rules['Rule'] = display_rules.apply(
                lambda row: f"{', '.join(list(row['antecedents']))} → {', '.join(list(row['consequents']))}",
                axis=1
            )
            
            display_cols = ['Rule', 'support', 'confidence', 'lift']
            st.dataframe(
                display_rules[display_cols].round(3),
                use_container_width=True
            )
            
            # Summary statistics
            st.subheader("Rules Summary")
            summary = mba_engine.get_rules_summary()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rules", summary['total_rules'])
            with col2:
                st.metric("Avg Confidence", f"{summary['avg_confidence']:.3f}")
            with col3:
                st.metric("Avg Lift", f"{summary['avg_lift']:.3f}")
            with col4:
                st.metric("Max Lift", f"{summary['max_lift']:.3f}")
        else:
            st.warning("No association rules found. Try lowering the minimum support or confidence thresholds.")
    
    with tab2:
        st.subheader("Product-Based Recommendations")
        
        # Get unique products
        products = sorted(transactions_df['product'].unique())
        selected_product = st.selectbox("Select a Product", products)
        
        n_recs = st.slider("Number of Recommendations", 1, 10, 5)
        
        if st.button("Get Recommendations"):
            recommendations = mba_engine.get_product_recommendations(selected_product, n=n_recs)
            
            if recommendations:
                st.success(f"Customers who bought **{selected_product}** also buy:")
                
                recs_df = pd.DataFrame(recommendations)
                recs_df.index = range(1, len(recs_df) + 1)
                st.dataframe(
                    recs_df[['product', 'confidence', 'lift', 'support']].round(3),
                    use_container_width=True
                )
            else:
                st.info(f"No strong associations found for {selected_product}. Try selecting a different product.")
    
    with tab3:
        st.subheader("Visualizations")
        
        viz_type = st.selectbox(
            "Select Visualization",
            [
                "Association Rules Heatmap",
                "Product Network Graph",
                "Top Bundles",
                "Frequently Bought Together",
                "Product Correlation Heatmap"
            ]
        )
        
        if viz_type == "Association Rules Heatmap":
            n_viz = st.slider("Number of Rules", 5, 30, 15)
            fig = create_association_rules_heatmap(mba_engine.rules, top_n=n_viz)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Product Network Graph":
            n_viz = st.slider("Number of Rules", 10, 50, 30)
            fig = create_product_network_graph(mba_engine.rules, top_n=n_viz)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Top Bundles":
            n_viz = st.slider("Number of Bundles", 5, 20, 10)
            bundles = mba_engine.get_top_bundles(n=n_viz)
            fig = create_top_bundles_chart(bundles, n=n_viz)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Frequently Bought Together":
            n_viz = st.slider("Number of Pairs", 5, 20, 10)
            pairs = mba_engine.get_frequently_bought_together(n=n_viz)
            fig = create_frequently_bought_together_chart(pairs, n=n_viz)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Product Correlation Heatmap":
            n_viz = st.slider("Number of Products", 5, 20, 15)
            fig = create_correlation_heatmap(basket_df, top_n=n_viz)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Export Results")
        
        if mba_engine.rules is not None and len(mba_engine.rules) > 0:
            # Format rules for export
            export_rules = mba_engine.rules.copy()
            export_rules['antecedents'] = export_rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            export_rules['consequents'] = export_rules['consequents'].apply(lambda x: ', '.join(list(x)))
            
            csv = export_rules.to_csv(index=False)
            st.download_button(
                label="Download Association Rules as CSV",
                data=csv,
                file_name="association_rules.csv",
                mime="text/csv"
            )
        else:
            st.info("No rules to export. Generate rules first.")


def show_recommendations_page(recommender, transactions_df):
    """Display Personalized Recommendations page."""
    st.header("👤 Personalized Recommendations")
    st.markdown("Get personalized product recommendations for customers based on collaborative filtering.")
    
    # Customer selection
    customer_ids = sorted(transactions_df['customer_id'].unique())
    
    col1, col2 = st.columns([2, 1])
    with col1:
        customer_id = st.selectbox("Select Customer ID", customer_ids)
    with col2:
        n_recs = st.number_input("Number of Recommendations", min_value=1, max_value=20, value=10)
    
    if st.button("Get Recommendations"):
        with st.spinner("Generating recommendations..."):
            recommendations = recommender.get_user_recommendations(customer_id, n=n_recs)
            
            if recommendations:
                st.success(f"Top {len(recommendations)} Recommendations for Customer {customer_id}")
                
                # Display recommendations
                recs_df = pd.DataFrame(recommendations)
                recs_df.index = range(1, len(recs_df) + 1)
                recs_df['rank'] = recs_df.index
                recs_df = recs_df[['rank', 'product', 'score', 'reasoning']]
                st.dataframe(recs_df, use_container_width=True)
                
                # Customer purchase history
                st.subheader("Customer Purchase History")
                customer_history = transactions_df[transactions_df['customer_id'] == customer_id]
                if len(customer_history) > 0:
                    history_summary = customer_history.groupby('product')['quantity'].sum().reset_index()
                    history_summary.columns = ['Product', 'Total Quantity']
                    st.dataframe(history_summary, use_container_width=True)
                else:
                    st.info("No purchase history found for this customer.")
                
                # Similar users
                st.subheader("Similar Users")
                similar_users = recommender.get_similar_users(customer_id, n=5)
                if similar_users:
                    similar_df = pd.DataFrame(similar_users)
                    similar_df.index = range(1, len(similar_df) + 1)
                    st.dataframe(similar_df, use_container_width=True)
            else:
                st.info("No recommendations available. This might be a new customer with no purchase history.")


def show_dashboard_page(mba_engine, transactions_df, basket_df):
    """Display Insights Dashboard page."""
    st.header("📊 Insights Dashboard")
    st.markdown("Comprehensive analytics and insights for your e-commerce business.")
    
    # Key Metrics
    st.subheader("Key Metrics")
    metrics = calculate_basic_metrics(transactions_df)
    summary = mba_engine.get_rules_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Orders", metrics['total_orders'])
    with col2:
        st.metric("Total Customers", metrics['total_customers'])
    with col3:
        st.metric("Association Rules", summary['total_rules'])
    with col4:
        st.metric("Avg Items/Order", f"{metrics['avg_items_per_order']:.2f}")
    
    # Visualizations
    st.markdown("---")
    st.subheader("Product Popularity")
    fig_popularity = create_product_popularity_chart(transactions_df, top_n=10)
    st.plotly_chart(fig_popularity, use_container_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Product Bundles")
        bundles = mba_engine.get_top_bundles(n=10)
        fig_bundles = create_top_bundles_chart(bundles, n=10)
        st.plotly_chart(fig_bundles, use_container_width=True)
    
    with col2:
        st.subheader("Frequently Bought Together")
        pairs = mba_engine.get_frequently_bought_together(n=10)
        fig_pairs = create_frequently_bought_together_chart(pairs, n=10)
        st.plotly_chart(fig_pairs, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Product Association Network")
    fig_network = create_product_network_graph(mba_engine.rules, top_n=30)
    st.plotly_chart(fig_network, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Product Correlation Matrix")
    fig_corr = create_correlation_heatmap(basket_df, top_n=15)
    st.plotly_chart(fig_corr, use_container_width=True)


if __name__ == "__main__":
    main()

