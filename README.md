# SmartCart — E-Commerce Recommendation Engine

An interactive recommendation system for e-commerce that answers three questions: which products are bought together, what should we recommend to each customer, and which bundles are worth promoting. It combines **market basket analysis** (Apriori) with **collaborative filtering** (NMF matrix factorization), served through a Streamlit app with an insights dashboard.

## Why two techniques

Market basket analysis finds *product* relationships — association rules with support, confidence, and lift. Good for "customers who bought X also buy Y" bundles, but it knows nothing about individual customers. Collaborative filtering fills that gap with *personalized* picks per customer, using NMF latent factors with cosine similarity; a content-based fallback covers the cold-start case for new customers with no history. Using both means the app serves anonymous browsers and known customers from the same data.

## What it does

- **Market basket analysis** — Apriori frequent itemsets, association rules sortable by lift / confidence / support, product network graph, top-bundle charts
- **Personalized recommendations** — per-customer suggestions with purchase history and similar-user context
- **Insights dashboard** — key metrics, product popularity, frequently-bought-together pairs, exportable results (CSV)

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`. Sample data ships in `data/`; you can drop in your own transactions in the same format. `download_server.py` serves the sample CSVs over HTTP for quick inspection (`python download_server.py`, then `http://localhost:8000`).

## Data

Sample transaction data for demo purposes:

- `sample_transactions.csv` — `order_id`, `product`, `quantity`, `customer_id`
- `sample_customers.csv` — `customer_id`, `age`, `segment` (Premium / Standard / Basic)
- `market_basket_sample.csv` — larger sample set for the basket analysis view

## Stack

Python, Streamlit, pandas, NumPy, scikit-learn (NMF, cosine similarity), mlxtend (Apriori), Plotly, NetworkX.

## Project structure

```
smartcart/
├── app.py                 # Streamlit application
├── download_server.py     # Helper HTTP server for downloading sample CSVs
├── requirements.txt
├── .streamlit/            # Streamlit app config
├── src/
│   ├── data_loader.py     # Data loading
│   ├── preprocessing.py   # Preprocessing
│   ├── mba_engine.py      # Market basket analysis engine
│   ├── recommender.py     # Collaborative filtering engine
│   ├── visualizations.py  # Plotly / NetworkX charts
│   └── utils.py
└── data/
    ├── sample_transactions.csv
    ├── sample_customers.csv
    └── market_basket_sample.csv
```

Model parameters (`min_support`, `min_confidence`, NMF components, recommendation count) are adjustable in the Streamlit UI.

## Limitations and next steps

- Thresholds and factor counts are tuned for the bundled sample data; a real catalog needs re-tuning
- NMF factors are fit per run — no incremental updates as new transactions arrive
- Next: a real-time serving API and A/B testing of recommendation strategies

## Author

Sai Bhargava Ram Rangappagari — [LinkedIn](https://www.linkedin.com/in/sai-bhargava-ram)

Open source under the MIT License.
