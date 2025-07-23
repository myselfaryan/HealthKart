import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="HealthKart Influencer Campaign ROI Dashboard",
    page_icon="📊",
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
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all datasets"""
    try:
        influencers_df = pd.read_csv("data/influencers.csv")
        posts_df = pd.read_csv("data/posts.csv")
        tracking_data_df = pd.read_csv("data/tracking_data.csv")
        payouts_df = pd.read_csv("data/payouts.csv")
        
        # Convert date columns
        posts_df['date'] = pd.to_datetime(posts_df['date'])
        tracking_data_df['date'] = pd.to_datetime(tracking_data_df['date'])
        
        return influencers_df, posts_df, tracking_data_df, payouts_df
    except FileNotFoundError:
        st.error("Data files not found. Please ensure all CSV files are in the 'data' directory.")
        return None, None, None, None

def calculate_roi_metrics(tracking_df, payouts_df):
    """Calculate ROI and ROAS metrics"""
    # Total revenue and costs
    total_revenue = tracking_df['revenue'].sum()
    total_payouts = payouts_df['total_payout'].sum()
    
    # ROI calculation
    roi = ((total_revenue - total_payouts) / total_payouts) * 100 if total_payouts > 0 else 0
    
    # ROAS calculation
    roas = total_revenue / total_payouts if total_payouts > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_payouts': total_payouts,
        'roi': roi,
        'roas': roas,
        'profit': total_revenue - total_payouts
    }

def main():
    # Header
    st.markdown('<h1 class="main-header">HealthKart Influencer Campaign ROI Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    influencers_df, posts_df, tracking_data_df, payouts_df = load_data()
    
    if influencers_df is None:
        return
    
    # Sidebar filters
    st.sidebar.markdown('<div class="sidebar-header">Filters</div>', unsafe_allow_html=True)
    
    # Platform filter
    platforms = ['All'] + list(influencers_df['platform'].unique())
    selected_platform = st.sidebar.selectbox("Platform", platforms)
    
    # Category filter
    categories = ['All'] + list(influencers_df['category'].unique())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Campaign filter
    campaigns = ['All'] + list(tracking_data_df['campaign'].unique())
    selected_campaign = st.sidebar.selectbox("Campaign", campaigns)
    
    # Product filter
    products = ['All'] + list(tracking_data_df['product'].unique())
    selected_product = st.sidebar.selectbox("Product", products)
    
    # Date range filter
    min_date = tracking_data_df['date'].min()
    max_date = tracking_data_df['date'].max()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply filters
    filtered_influencers = influencers_df.copy()
    filtered_posts = posts_df.copy()
    filtered_tracking = tracking_data_df.copy()
    filtered_payouts = payouts_df.copy()
    
    if selected_platform != 'All':
        filtered_influencers = filtered_influencers[filtered_influencers['platform'] == selected_platform]
        filtered_posts = filtered_posts[filtered_posts['platform'] == selected_platform]
        filtered_tracking = filtered_tracking[filtered_tracking['source'] == selected_platform]
    
    if selected_category != 'All':
        category_influencers = filtered_influencers[filtered_influencers['category'] == selected_category]['ID']
        filtered_posts = filtered_posts[filtered_posts['influencer_id'].isin(category_influencers)]
        filtered_tracking = filtered_tracking[filtered_tracking['influencer_id'].isin(category_influencers)]
        filtered_payouts = filtered_payouts[filtered_payouts['influencer_id'].isin(category_influencers)]
    
    if selected_campaign != 'All':
        filtered_tracking = filtered_tracking[filtered_tracking['campaign'] == selected_campaign]
    
    if selected_product != 'All':
        filtered_tracking = filtered_tracking[filtered_tracking['product'] == selected_product]
    
    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_posts = filtered_posts[
            (filtered_posts['date'] >= pd.to_datetime(start_date)) & 
            (filtered_posts['date'] <= pd.to_datetime(end_date))
        ]
        filtered_tracking = filtered_tracking[
            (filtered_tracking['date'] >= pd.to_datetime(start_date)) & 
            (filtered_tracking['date'] <= pd.to_datetime(end_date))
        ]
    
    # Calculate metrics
    metrics = calculate_roi_metrics(filtered_tracking, filtered_payouts)
    
    # Key Metrics Row
    st.subheader("📈 Key Performance Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Revenue", f"₹{metrics['total_revenue']:,.0f}")
    
    with col2:
        st.metric("Total Payouts", f"₹{metrics['total_payouts']:,.0f}")
    
    with col3:
        st.metric("Profit", f"₹{metrics['profit']:,.0f}")
    
    with col4:
        st.metric("ROI", f"{metrics['roi']:.1f}%")
    
    with col5:
        st.metric("ROAS", f"{metrics['roas']:.2f}x")
    
    # Charts Row 1
    st.subheader("📊 Campaign Performance Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Campaign
        campaign_revenue = filtered_tracking.groupby('campaign')['revenue'].sum().reset_index()
        fig_campaign = px.bar(
            campaign_revenue, 
            x='campaign', 
            y='revenue',
            title="Revenue by Campaign",
            color='revenue',
            color_continuous_scale='Blues'
        )
        fig_campaign.update_layout(height=400)
        st.plotly_chart(fig_campaign, use_container_width=True)
    
    with col2:
        # Revenue by Product
        product_revenue = filtered_tracking.groupby('product')['revenue'].sum().reset_index()
        fig_product = px.pie(
            product_revenue, 
            values='revenue', 
            names='product',
            title="Revenue Distribution by Product"
        )
        fig_product.update_layout(height=400)
        st.plotly_chart(fig_product, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform Performance
        platform_data = filtered_tracking.groupby('source').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        fig_platform = px.scatter(
            platform_data,
            x='orders',
            y='revenue',
            size='revenue',
            color='source',
            title="Platform Performance (Orders vs Revenue)",
            hover_data=['source']
        )
        fig_platform.update_layout(height=400)
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        # Revenue Trend Over Time
        daily_revenue = filtered_tracking.groupby('date')['revenue'].sum().reset_index()
        fig_trend = px.line(
            daily_revenue,
            x='date',
            y='revenue',
            title="Revenue Trend Over Time"
        )
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Influencer Performance Section
    st.subheader("👥 Top Influencer Performance")
    
    # Calculate influencer metrics
    influencer_metrics = filtered_tracking.groupby('influencer_id').agg({
        'revenue': 'sum',
        'orders': 'sum'
    }).reset_index()
    
    # Merge with influencer details
    influencer_metrics = influencer_metrics.merge(
        filtered_influencers[['ID', 'name', 'category', 'platform', 'follower_count']], 
        left_on='influencer_id', 
        right_on='ID'
    )
    
    # Merge with payouts
    influencer_payouts = filtered_payouts.groupby('influencer_id')['total_payout'].sum().reset_index()
    influencer_metrics = influencer_metrics.merge(influencer_payouts, on='influencer_id', how='left')
    influencer_metrics['total_payout'] = influencer_metrics['total_payout'].fillna(0)
    
    # Calculate ROI for each influencer
    influencer_metrics['roi'] = ((influencer_metrics['revenue'] - influencer_metrics['total_payout']) / 
                                influencer_metrics['total_payout'] * 100).fillna(0)
    
    # Top performers table
    top_performers = influencer_metrics.nlargest(10, 'revenue')[
        ['name', 'category', 'platform', 'follower_count', 'revenue', 'orders', 'total_payout', 'roi']
    ]
    
    st.dataframe(
        top_performers,
        column_config={
            "name": "Influencer Name",
            "category": "Category",
            "platform": "Platform",
            "follower_count": st.column_config.NumberColumn("Followers", format="%d"),
            "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
            "orders": st.column_config.NumberColumn("Orders", format="%d"),
            "total_payout": st.column_config.NumberColumn("Payout", format="₹%.0f"),
            "roi": st.column_config.NumberColumn("ROI", format="%.1f%%")
        },
        hide_index=True
    )
    
    # Export functionality
    st.subheader("📥 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Campaign Summary to CSV"):
            summary_data = {
                'Metric': ['Total Revenue', 'Total Payouts', 'Profit', 'ROI (%)', 'ROAS'],
                'Value': [metrics['total_revenue'], metrics['total_payouts'], 
                         metrics['profit'], metrics['roi'], metrics['roas']]
            }
            summary_df = pd.DataFrame(summary_data)
            csv = summary_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="campaign_summary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export Top Performers to CSV"):
            csv = top_performers.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="top_performers.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

