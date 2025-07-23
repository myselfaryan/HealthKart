import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from advanced_analytics import InfluencerROIAnalytics

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
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        color: #31333F; /* Set text color for contrast */
    }
    .insight-box h4 {
        color: #1f77b4; /* Match header color */
    }
    .recommendation {
        background-color: #f0f9ff;
        padding: 0.8rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3b82f6;
        color: #31333F; /* Set text color for contrast */
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

def main():
    # Header
    st.markdown('<h1 class="main-header">HealthKart Influencer Campaign ROI Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    influencers_df, posts_df, tracking_data_df, payouts_df = load_data()
    
    if influencers_df is None:
        return
    
    # Initialize analytics
    analytics = InfluencerROIAnalytics(influencers_df, posts_df, tracking_data_df, payouts_df)
    
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
    
    # Create filtered analytics instance
    filtered_analytics = InfluencerROIAnalytics(filtered_influencers, filtered_posts, filtered_tracking, filtered_payouts)
    
    # Generate insights
    insights = filtered_analytics.generate_insights_summary()
    incremental_roas = filtered_analytics.calculate_incremental_roas()
    
    # Key Metrics Row
    st.subheader("📈 Key Performance Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Revenue", f"₹{insights['overall_performance']['total_revenue']:,.0f}")
    
    with col2:
        st.metric("Incremental Revenue", f"₹{insights['overall_performance']['incremental_revenue']:,.0f}")
    
    with col3:
        st.metric("Total Spend", f"₹{insights['overall_performance']['total_spend']:,.0f}")
    
    with col4:
        st.metric("Overall ROI", f"{insights['overall_performance']['overall_roi']:.1f}%")
    
    with col5:
        st.metric("Incremental ROAS", f"{insights['overall_performance']['incremental_roas']:.2f}x")
    
    with col6:
        st.metric("Poor Performers", insights['poor_performers_count'])
    
    # Insights Summary
    st.subheader("🎯 Key Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏆 Best Performing Campaign</h4>
            <p><strong>{insights['best_campaign']}</strong></p>
            <p>Focus resources on replicating this campaign's success factors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <h4>📱 Best Performing Platform</h4>
            <p><strong>{insights['best_platform']}</strong></p>
            <p>Highest ROI platform for influencer partnerships</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("💡 Strategic Recommendations")
    for i, recommendation in enumerate(insights['recommendations'], 1):
        st.markdown(f"""
        <div class="recommendation">
            <strong>{i}.</strong> {recommendation}
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row 1
    st.subheader("📊 Campaign Performance Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Campaign
        campaign_performance = filtered_analytics.analyze_campaign_performance()
        if not campaign_performance.empty:
            fig_campaign = px.bar(
                campaign_performance, 
                x='campaign', 
                y='revenue',
                title="Revenue by Campaign",
                color='roi',
                color_continuous_scale='RdYlGn',
                hover_data=['roi', 'roas', 'unique_influencers']
            )
            fig_campaign.update_layout(height=400)
            st.plotly_chart(fig_campaign, use_container_width=True)
    
    with col2:
        # Platform Performance
        platform_performance = filtered_analytics.analyze_platform_performance()
        if not platform_performance.empty:
            fig_platform = px.scatter(
                platform_performance,
                x='orders',
                y='revenue',
                size='unique_influencers',
                color='roi',
                title="Platform Performance (Orders vs Revenue)",
                hover_data=['platform', 'roas', 'avg_order_value'],
                color_continuous_scale='RdYlGn'
            )
            fig_platform.update_layout(height=400)
            st.plotly_chart(fig_platform, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Performers Analysis
        top_performers = filtered_analytics.identify_top_performers('efficiency', 10)
        if not top_performers.empty:
            fig_top = px.bar(
                top_performers.head(10),
                x='name',
                y='roi',
                title="Top 10 Influencers by ROI",
                color='category',
                hover_data=['revenue', 'roas', 'platform']
            )
            fig_top.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        # Revenue Trend Over Time
        daily_revenue = filtered_tracking.groupby('date')['revenue'].sum().reset_index()
        if not daily_revenue.empty:
            fig_trend = px.line(
                daily_revenue,
                x='date',
                y='revenue',
                title="Revenue Trend Over Time"
            )
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # Detailed Analytics Tabs
    st.subheader("🔍 Detailed Analytics")
    tab1, tab2, tab3, tab4 = st.tabs(["Top Performers", "Poor Performers", "Campaign Analysis", "Platform Analysis"])
    
    with tab1:
        st.subheader("🏆 Top Performing Influencers")
        top_performers = filtered_analytics.identify_top_performers('efficiency', 20)
        if not top_performers.empty:
            st.dataframe(
                top_performers[['name', 'category', 'platform', 'follower_count', 'revenue', 'orders', 'total_payout', 'roi', 'roas', 'revenue_per_follower']],
                column_config={
                    "name": "Influencer Name",
                    "category": "Category",
                    "platform": "Platform",
                    "follower_count": st.column_config.NumberColumn("Followers", format="%d"),
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                    "orders": st.column_config.NumberColumn("Orders", format="%d"),
                    "total_payout": st.column_config.NumberColumn("Payout", format="₹%.0f"),
                    "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                    "revenue_per_follower": st.column_config.NumberColumn("Revenue/Follower", format="₹%.4f")
                },
                hide_index=True
            )
    
    with tab2:
        st.subheader("⚠️ Poor Performing Influencers")
        poor_performers = filtered_analytics.identify_poor_performers()
        if not poor_performers.empty:
            st.dataframe(
                poor_performers[['name', 'category', 'platform', 'follower_count', 'revenue', 'orders', 'total_payout', 'roi', 'roas']],
                column_config={
                    "name": "Influencer Name",
                    "category": "Category",
                    "platform": "Platform",
                    "follower_count": st.column_config.NumberColumn("Followers", format="%d"),
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                    "orders": st.column_config.NumberColumn("Orders", format="%d"),
                    "total_payout": st.column_config.NumberColumn("Payout", format="₹%.0f"),
                    "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx")
                },
                hide_index=True
            )
        else:
            st.info("No poor performers found with current filters!")
    
    with tab3:
        st.subheader("📈 Campaign Performance Details")
        campaign_performance = filtered_analytics.analyze_campaign_performance()
        if not campaign_performance.empty:
            st.dataframe(
                campaign_performance,
                column_config={
                    "campaign": "Campaign",
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                    "orders": st.column_config.NumberColumn("Orders", format="%d"),
                    "unique_influencers": st.column_config.NumberColumn("Influencers", format="%d"),
                    "total_payout": st.column_config.NumberColumn("Total Payout", format="₹%.0f"),
                    "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                    "avg_revenue_per_influencer": st.column_config.NumberColumn("Avg Revenue/Influencer", format="₹%.0f")
                },
                hide_index=True
            )
    
    with tab4:
        st.subheader("📱 Platform Performance Details")
        platform_performance = filtered_analytics.analyze_platform_performance()
        if not platform_performance.empty:
            st.dataframe(
                platform_performance,
                column_config={
                    "platform": "Platform",
                    "revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                    "orders": st.column_config.NumberColumn("Orders", format="%d"),
                    "unique_influencers": st.column_config.NumberColumn("Influencers", format="%d"),
                    "total_payout": st.column_config.NumberColumn("Total Payout", format="₹%.0f"),
                    "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                    "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                    "avg_order_value": st.column_config.NumberColumn("Avg Order Value", format="₹%.0f")
                },
                hide_index=True
            )
    
    # Export functionality
    st.subheader("📥 Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Insights Summary"):
            insights_data = {
                'Metric': ['Total Revenue', 'Incremental Revenue', 'Total Spend', 'Overall ROI', 'Incremental ROAS', 'Poor Performers'],
                'Value': [
                    f"₹{insights['overall_performance']['total_revenue']:,.0f}",
                    f"₹{insights['overall_performance']['incremental_revenue']:,.0f}",
                    f"₹{insights['overall_performance']['total_spend']:,.0f}",
                    f"{insights['overall_performance']['overall_roi']:.1f}%",
                    f"{insights['overall_performance']['incremental_roas']:.2f}x",
                    insights['poor_performers_count']
                ]
            }
            insights_df = pd.DataFrame(insights_data)
            csv = insights_df.to_csv(index=False)
            st.download_button(
                label="Download Insights CSV",
                data=csv,
                file_name="insights_summary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export Top Performers"):
            top_performers = filtered_analytics.identify_top_performers('efficiency', 20)
            if not top_performers.empty:
                csv = top_performers.to_csv(index=False)
                st.download_button(
                    label="Download Top Performers CSV",
                    data=csv,
                    file_name="top_performers.csv",
                    mime="text/csv"
                )
    
    with col3:
        if st.button("Export Campaign Analysis"):
            campaign_performance = filtered_analytics.analyze_campaign_performance()
            if not campaign_performance.empty:
                csv = campaign_performance.to_csv(index=False)
                st.download_button(
                    label="Download Campaign Analysis CSV",
                    data=csv,
                    file_name="campaign_analysis.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()

