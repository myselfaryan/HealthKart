import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class InsightsGenerator:
    def __init__(self, analytics):
        self.analytics = analytics
        
    def generate_persona_analysis(self):
        """
        Analyze best performing personas (category + platform combinations)
        """
        # Get influencer performance data
        influencer_metrics = self.analytics.calculate_influencer_efficiency_metrics()
        
        # Create persona combinations
        influencer_metrics['persona'] = influencer_metrics['category'] + ' + ' + influencer_metrics['platform']
        
        # Analyze persona performance
        persona_performance = influencer_metrics.groupby('persona').agg({
            'revenue': ['sum', 'mean', 'count'],
            'roi': 'mean',
            'roas': 'mean',
            'total_payout': 'sum',
            'orders': 'sum'
        }).round(2)
        
        # Flatten column names
        persona_performance.columns = ['_'.join(col).strip() for col in persona_performance.columns]
        persona_performance = persona_performance.reset_index()
        
        # Calculate efficiency score
        persona_performance['efficiency_score'] = (
            persona_performance['roi_mean'] * 0.4 + 
            persona_performance['roas_mean'] * 20 + 
            persona_performance['revenue_sum'] / 1000
        )
        
        # Sort by efficiency score
        persona_performance = persona_performance.sort_values('efficiency_score', ascending=False)
        
        return persona_performance
    
    def generate_seasonal_trends(self):
        """
        Analyze seasonal trends in campaign performance
        """
        tracking_df = self.analytics.tracking_df.copy()
        tracking_df['date'] = pd.to_datetime(tracking_df['date'])
        tracking_df['month'] = tracking_df['date'].dt.month
        tracking_df['week'] = tracking_df['date'].dt.isocalendar().week
        tracking_df['day_of_week'] = tracking_df['date'].dt.day_name()
        
        # Monthly trends
        monthly_trends = tracking_df.groupby('month').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        monthly_trends['month_name'] = pd.to_datetime(monthly_trends['month'], format='%m').dt.month_name()
        
        # Weekly trends
        weekly_trends = tracking_df.groupby('week').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        # Day of week trends
        dow_trends = tracking_df.groupby('day_of_week').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_trends['day_of_week'] = pd.Categorical(dow_trends['day_of_week'], categories=day_order, ordered=True)
        dow_trends = dow_trends.sort_values('day_of_week')
        
        return {
            'monthly': monthly_trends,
            'weekly': weekly_trends,
            'day_of_week': dow_trends
        }
    
    def generate_engagement_analysis(self):
        """
        Analyze engagement metrics from posts data
        """
        posts_df = self.analytics.posts_df.copy()
        
        # Merge with influencer data
        posts_with_influencers = posts_df.merge(
            self.analytics.influencers_df[['ID', 'category', 'platform', 'follower_count']], 
            left_on='influencer_id', 
            right_on='ID',
            suffixes=('_post', '_influencer')
        )
        
        # Calculate engagement metrics
        posts_with_influencers['engagement_rate'] = (
            (posts_with_influencers['likes'] + posts_with_influencers['comments']) / 
            posts_with_influencers['reach'] * 100
        )
        posts_with_influencers['likes_per_follower'] = (
            posts_with_influencers['likes'] / posts_with_influencers['follower_count']
        )
        posts_with_influencers['reach_rate'] = (
            posts_with_influencers['reach'] / posts_with_influencers['follower_count'] * 100
        )
        
        # Analyze by category and platform
        engagement_by_category = posts_with_influencers.groupby('category').agg({
            'engagement_rate': 'mean',
            'likes_per_follower': 'mean',
            'reach_rate': 'mean',
            'reach': 'mean',
            'likes': 'mean',
            'comments': 'mean'
        }).round(2).reset_index()
        
        engagement_by_platform = posts_with_influencers.groupby('platform_influencer').agg({
            'engagement_rate': 'mean',
            'likes_per_follower': 'mean',
            'reach_rate': 'mean',
            'reach': 'mean',
            'likes': 'mean',
            'comments': 'mean'
        }).round(2).reset_index()
        
        return {
            'by_category': engagement_by_category,
            'by_platform': engagement_by_platform,
            'raw_data': posts_with_influencers
        }
    
    def generate_cost_efficiency_analysis(self):
        """
        Analyze cost efficiency across different dimensions
        """
        influencer_metrics = self.analytics.calculate_influencer_efficiency_metrics()
        
        # Cost efficiency by follower count segments
        influencer_metrics['follower_segment'] = pd.cut(
            influencer_metrics['follower_count'], 
            bins=[0, 50000, 200000, 500000, float('inf')],
            labels=['Micro (0-50K)', 'Mid (50K-200K)', 'Macro (200K-500K)', 'Mega (500K+)']
        )
        
        cost_by_segment = influencer_metrics.groupby('follower_segment').agg({
            'cost_per_order': 'mean',
            'revenue_per_follower': 'mean',
            'roi': 'mean',
            'roas': 'mean',
            'revenue': 'sum',
            'total_payout': 'sum'
        }).round(2).reset_index()
        
        # Cost efficiency by category
        cost_by_category = influencer_metrics.groupby('category').agg({
            'cost_per_order': 'mean',
            'revenue_per_follower': 'mean',
            'roi': 'mean',
            'roas': 'mean',
            'revenue': 'sum',
            'total_payout': 'sum'
        }).round(2).reset_index()
        
        # Cost efficiency by platform
        cost_by_platform = influencer_metrics.groupby('platform').agg({
            'cost_per_order': 'mean',
            'revenue_per_follower': 'mean',
            'roi': 'mean',
            'roas': 'mean',
            'revenue': 'sum',
            'total_payout': 'sum'
        }).round(2).reset_index()
        
        return {
            'by_segment': cost_by_segment,
            'by_category': cost_by_category,
            'by_platform': cost_by_platform
        }
    
    def generate_predictive_insights(self):
        """
        Generate predictive insights and recommendations
        """
        influencer_metrics = self.analytics.calculate_influencer_efficiency_metrics()
        campaign_performance = self.analytics.analyze_campaign_performance()
        platform_performance = self.analytics.analyze_platform_performance()
        
        insights = []
        
        # Top performing segments
        top_category = influencer_metrics.groupby('category')['roi'].mean().idxmax()
        top_platform = influencer_metrics.groupby('platform')['roi'].mean().idxmax()
        
        insights.append({
            'type': 'opportunity',
            'title': 'High-ROI Segment Identified',
            'description': f'{top_category} influencers on {top_platform} show highest average ROI',
            'action': f'Increase budget allocation to {top_category} + {top_platform} combinations',
            'impact': 'High'
        })
        
        # Underperforming segments
        poor_performers = self.analytics.identify_poor_performers()
        if len(poor_performers) > 0:
            worst_category = poor_performers['category'].mode().iloc[0] if not poor_performers['category'].mode().empty else 'N/A'
            insights.append({
                'type': 'risk',
                'title': 'Underperforming Segment Alert',
                'description': f'{len(poor_performers)} influencers underperforming, majority in {worst_category}',
                'action': f'Review and optimize {worst_category} influencer strategy',
                'impact': 'Medium'
            })
        
        # Budget optimization
        if not campaign_performance.empty:
            best_campaign = campaign_performance.loc[campaign_performance['roas'].idxmax()]
            insights.append({
                'type': 'optimization',
                'title': 'Budget Reallocation Opportunity',
                'description': f'{best_campaign["campaign"]} campaign shows highest ROAS ({best_campaign["roas"]:.2f}x)',
                'action': f'Reallocate budget from low-performing campaigns to {best_campaign["campaign"]} format',
                'impact': 'High'
            })
        
        # Scaling opportunities
        top_performers = self.analytics.identify_top_performers('efficiency', 5)
        if not top_performers.empty:
            avg_roi = top_performers['roi'].mean()
            insights.append({
                'type': 'growth',
                'title': 'Scaling Opportunity',
                'description': f'Top 5 performers average {avg_roi:.1f}% ROI',
                'action': 'Increase investment with top performers and find similar profiles',
                'impact': 'High'
            })
        
        return insights
    
    def create_executive_summary(self):
        """
        Create executive summary with key metrics and insights
        """
        overall_metrics = self.analytics.calculate_incremental_roas()
        top_performers = self.analytics.identify_top_performers('efficiency', 5)
        poor_performers = self.analytics.identify_poor_performers()
        campaign_performance = self.analytics.analyze_campaign_performance()
        
        summary = {
            'overview': {
                'total_revenue': overall_metrics['total_revenue'],
                'incremental_revenue': overall_metrics['incremental_revenue'],
                'total_spend': overall_metrics['total_spend'],
                'overall_roi': ((overall_metrics['total_revenue'] - overall_metrics['total_spend']) / 
                              overall_metrics['total_spend'] * 100) if overall_metrics['total_spend'] > 0 else 0,
                'incremental_roas': overall_metrics['incremental_roas']
            },
            'performance_highlights': {
                'top_performers_count': len(top_performers),
                'poor_performers_count': len(poor_performers),
                'best_campaign': campaign_performance.loc[campaign_performance['roi'].idxmax(), 'campaign'] if not campaign_performance.empty else 'N/A',
                'campaign_roi': campaign_performance['roi'].max() if not campaign_performance.empty else 0
            },
            'key_insights': self.generate_predictive_insights()[:3],  # Top 3 insights
            'recommendations': [
                'Focus investment on top-performing influencer segments',
                'Optimize or replace underperforming influencers',
                'Scale successful campaign formats',
                'Implement performance-based payout structures'
            ]
        }
        
        return summary
    
    def generate_visualization_data(self):
        """
        Generate data for advanced visualizations
        """
        persona_analysis = self.generate_persona_analysis()
        seasonal_trends = self.generate_seasonal_trends()
        engagement_analysis = self.generate_engagement_analysis()
        cost_efficiency = self.generate_cost_efficiency_analysis()
        
        return {
            'persona_analysis': persona_analysis,
            'seasonal_trends': seasonal_trends,
            'engagement_analysis': engagement_analysis,
            'cost_efficiency': cost_efficiency
        }

# Usage example
if __name__ == "__main__":
    from advanced_analytics import InfluencerROIAnalytics
    
    # Load data
    influencers_df = pd.read_csv("data/influencers.csv")
    posts_df = pd.read_csv("data/posts.csv")
    tracking_df = pd.read_csv("data/tracking_data.csv")
    payouts_df = pd.read_csv("data/payouts.csv")
    
    # Initialize analytics and insights
    analytics = InfluencerROIAnalytics(influencers_df, posts_df, tracking_df, payouts_df)
    insights_gen = InsightsGenerator(analytics)
    
    # Generate executive summary
    summary = insights_gen.create_executive_summary()
    
    print("=== EXECUTIVE SUMMARY ===")
    print(f"Total Revenue: ₹{summary['overview']['total_revenue']:,.0f}")
    print(f"Overall ROI: {summary['overview']['overall_roi']:.1f}%")
    print(f"Incremental ROAS: {summary['overview']['incremental_roas']:.2f}x")
    print(f"\nTop Performers: {summary['performance_highlights']['top_performers_count']}")
    print(f"Poor Performers: {summary['performance_highlights']['poor_performers_count']}")
    print(f"Best Campaign: {summary['performance_highlights']['best_campaign']}")
    
    print("\n=== KEY INSIGHTS ===")
    for insight in summary['key_insights']:
        print(f"• {insight['title']}: {insight['description']}")
    
    print("\n=== RECOMMENDATIONS ===")
    for i, rec in enumerate(summary['recommendations'], 1):
        print(f"{i}. {rec}")

