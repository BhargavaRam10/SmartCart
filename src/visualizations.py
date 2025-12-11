"""
Visualization utilities for SmartCart recommendation engine.
"""

from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx


def create_association_rules_heatmap(rules_df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """
    Create a heatmap of association rules metrics.
    
    Args:
        rules_df: DataFrame with association rules
        top_n: Number of top rules to display
        
    Returns:
        Plotly figure object
    """
    if len(rules_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No association rules found", xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    # Get top N rules by lift
    top_rules = rules_df.nlargest(top_n, 'lift')
    
    # Create rule labels
    rule_labels = []
    for _, rule in top_rules.iterrows():
        antecedents = ', '.join(list(rule['antecedents']))
        consequents = ', '.join(list(rule['consequents']))
        label = f"{antecedents} → {consequents}"
        rule_labels.append(label)
    
    # Prepare data for heatmap
    metrics = ['support', 'confidence', 'lift']
    z_data = top_rules[metrics].values.T
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=rule_labels,
        y=metrics,
        colorscale='Viridis',
        colorbar=dict(title="Value"),
        hovertemplate='<b>%{y}</b><br>%{x}<br>Value: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Top Association Rules Heatmap',
        xaxis_title='Rules',
        yaxis_title='Metrics',
        height=400,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


def create_product_network_graph(rules_df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    """
    Create a network graph of product associations.
    
    Args:
        rules_df: DataFrame with association rules
        top_n: Number of top rules to include
        
    Returns:
        Plotly figure object
    """
    if len(rules_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No association rules found", xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    # Get top N rules
    top_rules = rules_df.nlargest(top_n, 'lift')
    
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add edges with weights
    for _, rule in top_rules.iterrows():
        antecedents = list(rule['antecedents'])
        consequents = list(rule['consequents'])
        lift = rule['lift']
        
        for ant in antecedents:
            for cons in consequents:
                if ant != cons:
                    if G.has_edge(ant, cons):
                        G[ant][cons]['weight'] += lift
                    else:
                        G.add_edge(ant, cons, weight=lift)
    
    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No product associations found", xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    # Get positions using spring layout
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Extract edge information
    edge_x = []
    edge_y = []
    edge_weights = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_weights.append(G[edge[0]][edge[1]]['weight'])
    
    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Extract node information
    node_x = []
    node_y = []
    node_text = []
    node_sizes = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        # Size based on degree
        node_sizes.append(10 + G.degree(node) * 2)
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="middle center",
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=node_sizes,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left"
            ),
            line=dict(width=2)
        )
    )
    
    # Color nodes by degree
    node_adjacencies = []
    for node in G.nodes():
        node_adjacencies.append(G.degree(node))
    
    node_trace.marker.color = node_adjacencies
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='Product Association Network',
                       titlefont_size=16,
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       annotations=[dict(
                           text="Node size indicates number of associations",
                           showarrow=False,
                           xref="paper", yref="paper",
                           x=0.005, y=-0.002,
                           xanchor="left", yanchor="bottom",
                           font=dict(color="#888", size=12)
                       )],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       height=600
                   ))
    
    return fig


def create_top_bundles_chart(bundles: List[Dict], n: int = 10) -> go.Figure:
    """
    Create a bar chart of top product bundles.
    
    Args:
        bundles: List of bundle dictionaries
        n: Number of bundles to display
        
    Returns:
        Plotly figure object
    """
    if len(bundles) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No bundles found", xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    # Get top N bundles
    top_bundles = bundles[:n]
    
    # Prepare data
    bundle_labels = []
    support_values = []
    
    for bundle in top_bundles:
        products = ', '.join(bundle['products'])
        bundle_labels.append(products)
        support_values.append(bundle['support'])
    
    fig = go.Figure(data=[
        go.Bar(
            x=support_values,
            y=bundle_labels,
            orientation='h',
            marker=dict(color='steelblue'),
            text=[f"{s:.3f}" for s in support_values],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Top {n} Product Bundles',
        xaxis_title='Support',
        yaxis_title='Product Bundle',
        height=max(400, len(top_bundles) * 40),
        yaxis=dict(autorange="reversed")
    )
    
    return fig


def create_frequently_bought_together_chart(pairs: List[Dict], n: int = 10) -> go.Figure:
    """
    Create a bar chart of frequently bought together pairs.
    
    Args:
        pairs: List of product pair dictionaries
        n: Number of pairs to display
        
    Returns:
        Plotly figure object
    """
    if len(pairs) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No pairs found", xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    # Get top N pairs
    top_pairs = pairs[:n]
    
    # Prepare data
    pair_labels = []
    lift_values = []
    confidence_values = []
    
    for pair in top_pairs:
        label = f"{pair['product_a']} + {pair['product_b']}"
        pair_labels.append(label)
        lift_values.append(pair['lift'])
        confidence_values.append(pair['confidence'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Lift',
        x=pair_labels,
        y=lift_values,
        marker_color='steelblue',
        text=[f"{l:.2f}" for l in lift_values],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Confidence',
        x=pair_labels,
        y=confidence_values,
        marker_color='lightblue',
        text=[f"{c:.2f}" for c in confidence_values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'Top {n} Frequently Bought Together Pairs',
        xaxis_title='Product Pairs',
        yaxis_title='Metric Value',
        barmode='group',
        height=500,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


def create_product_popularity_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a bar chart of most popular products.
    
    Args:
        df: Transaction DataFrame
        top_n: Number of top products to display
        
    Returns:
        Plotly figure object
    """
    product_counts = df.groupby('product')['quantity'].sum().sort_values(ascending=False).head(top_n)
    
    fig = go.Figure(data=[
        go.Bar(
            x=product_counts.index,
            y=product_counts.values,
            marker=dict(color='coral'),
            text=product_counts.values,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} Most Popular Products',
        xaxis_title='Product',
        yaxis_title='Total Quantity Sold',
        height=400,
        xaxis=dict(tickangle=-45)
    )
    
    return fig


def create_correlation_heatmap(basket_df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """
    Create a correlation heatmap of products.
    
    Args:
        basket_df: Binary basket matrix
        top_n: Number of top products to include
        
    Returns:
        Plotly figure object
    """
    # Get top N products by frequency
    product_counts = basket_df.sum().sort_values(ascending=False).head(top_n)
    top_products = product_counts.index.tolist()
    
    # Calculate correlation matrix
    correlation_matrix = basket_df[top_products].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        colorbar=dict(title="Correlation"),
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Product Correlation Heatmap',
        xaxis_title='Product',
        yaxis_title='Product',
        height=600,
        xaxis=dict(tickangle=-45)
    )
    
    return fig

