# 🛒 SmartCart: E-Commerce Recommendation Engine

A comprehensive prescriptive analytics product for e-commerce that combines **Market Basket Analysis** (Apriori algorithm) and **Collaborative Filtering** to provide actionable product recommendations and insights.

## 📋 Overview

SmartCart is a full end-to-end recommendation system that helps e-commerce businesses:

- **Identify product associations** using Market Basket Analysis
- **Provide personalized recommendations** using Collaborative Filtering
- **Visualize insights** through interactive dashboards
- **Generate prescriptive analytics** for cross-selling and upselling

## 🎯 Problem Statement

E-commerce businesses need to understand:
- Which products are frequently bought together?
- What should we recommend to each customer?
- How can we increase average order value through cross-selling?
- What are the best product bundles to promote?

SmartCart addresses these questions by combining multiple recommendation techniques and providing actionable insights.

## 🚀 Features

### 1. Market Basket Analysis
- **Apriori Algorithm**: Identifies frequent itemsets and association rules
- **Association Rules**: Generates rules with support, confidence, and lift metrics
- **Product Recommendations**: "Customers who bought X also buy Y"
- **Bundle Identification**: Finds optimal product bundles for cross-selling

### 2. Collaborative Filtering
- **User-Based Filtering**: Recommends based on similar users' preferences
- **Matrix Factorization**: Uses NMF for latent factor modeling
- **Content-Based Fallback**: Handles cold-start problem for new users
- **Personalized Recommendations**: Tailored product suggestions per customer

### 3. Visualizations
- **Association Rules Heatmap**: Visual representation of rule metrics
- **Product Network Graph**: Network visualization of product associations
- **Top Bundles Chart**: Bar chart of most popular product bundles
- **Correlation Heatmap**: Product correlation matrix
- **Popularity Charts**: Product popularity and trends

### 4. Insights Dashboard
- Key metrics and statistics
- Top products and bundles
- Frequently bought together pairs
- Product association networks
- Exportable results

## 📊 Dataset Description

The project includes sample data:

- **sample_transactions.csv**: Transaction data with columns:
  - `order_id`: Unique order identifier
  - `product`: Product name
  - `quantity`: Quantity purchased
  - `customer_id`: Customer identifier

- **sample_customers.csv**: Customer metadata with columns:
  - `customer_id`: Customer identifier
  - `age`: Customer age
  - `segment`: Customer segment (Premium, Standard, Basic)

You can upload your own transaction data following the same format.

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **scikit-learn**: Machine learning algorithms (NMF, cosine similarity)
- **mlxtend**: Apriori algorithm and association rules
- **Plotly**: Interactive visualizations
- **NetworkX**: Network graph analysis

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the repository**

```bash
cd SmartCart
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 🚀 Running Locally

1. **Start the Streamlit application**

```bash
streamlit run app.py
```

2. **Open your browser**

The app will automatically open at `http://localhost:8501`

3. **Navigate through the app**

- **Home**: Overview and dataset statistics
- **Market Basket Analysis**: Association rules and product recommendations
- **Personalized Recommendations**: Customer-specific recommendations
- **Insights Dashboard**: Comprehensive analytics and visualizations

## ☁️ Deployment to Streamlit Cloud

1. **Push your code to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to `app.py`
   - Click "Deploy"

3. **Your app will be live!**

The app will be accessible at `https://your-app-name.streamlit.app`

## 📖 Usage Guide

### Market Basket Analysis

1. Navigate to "Market Basket Analysis"
2. Adjust minimum support and confidence thresholds
3. View association rules sorted by lift, confidence, or support
4. Select a product to see recommendations
5. Explore visualizations (heatmaps, network graphs)
6. Export rules as CSV

### Personalized Recommendations

1. Navigate to "Personalized Recommendations"
2. Select a customer ID from the dropdown
3. Choose number of recommendations
4. View personalized product suggestions
5. See customer purchase history and similar users

### Insights Dashboard

1. Navigate to "Insights Dashboard"
2. View key metrics and statistics
3. Explore product popularity charts
4. Analyze top bundles and frequently bought together pairs
5. Visualize product association networks

## 📸 Example Screenshots

*(Placeholder for screenshots)*

- Home page with dataset statistics
- Market Basket Analysis with association rules
- Personalized recommendations interface
- Insights dashboard with visualizations

## 🔧 Configuration

### Adjusting Model Parameters

**Market Basket Analysis:**
- `min_support`: Minimum support threshold (default: 0.1)
- `min_confidence`: Minimum confidence threshold (default: 0.3)

**Collaborative Filtering:**
- `n_components`: Number of components for matrix factorization (default: 5)
- `n_recommendations`: Default number of recommendations (default: 10)

These can be adjusted in the Streamlit UI or directly in the code.

## 🎯 Future Extensions

- [ ] **Deep Learning Models**: Implement neural collaborative filtering
- [ ] **Real-time Recommendations**: API endpoints for real-time serving
- [ ] **A/B Testing Framework**: Test recommendation strategies
- [ ] **Multi-armed Bandit**: Explore-exploit optimization
- [ ] **Time-based Recommendations**: Seasonal and trending products
- [ ] **Category-based Filtering**: Recommendations by product category
- [ ] **Customer Segmentation**: Advanced customer clustering
- [ ] **Price Optimization**: Bundle pricing recommendations
- [ ] **Inventory Integration**: Stock-aware recommendations
- [ ] **Performance Metrics**: Click-through rate, conversion tracking

## 📝 Code Structure

```
smartcart/
│── app.py                         # Streamlit application
│── requirements.txt               # Python dependencies
│── README.md                      # Project documentation
│── src/
│    ├── data_loader.py           # Data loading utilities
│    ├── preprocessing.py          # Data preprocessing
│    ├── mba_engine.py             # Market Basket Analysis engine
│    ├── recommender.py            # Collaborative filtering engine
│    ├── visualizations.py         # Visualization functions
│    ├── utils.py                  # Utility functions
│── data/
│    ├── sample_transactions.csv   # Sample transaction data
│    ├── sample_customers.csv      # Sample customer data
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ for e-commerce analytics

## 🙏 Acknowledgments

- mlxtend library for Apriori implementation
- Streamlit for the amazing framework
- Plotly for beautiful visualizations

---

**Happy Recommending! 🛒✨**

