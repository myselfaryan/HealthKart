import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class InfluencerROIAnalytics:
    def __init__(self, influencers_df, posts_df, tracking_df, payouts_df):
        self.influencers_df = influencers_df
        self.posts_df = posts_df
        self.tracking_df = tracking_df
        self.payouts_df = payouts_df
    
    def calculate_incremental_roas(self, baseline_period_days=30):
        """
        Calculate incremental ROAS by comparing performance with and without influencer campaigns
        """
        # Get baseline performance (assuming organic sales without influencer campaigns)
        total_revenue = self.tracking_df['revenue'].sum()
        total_orders = self.tracking_df['orders'].sum()
        
        # Estimate baseline conversion rate (assuming 2% baseline without influencers)
        baseline_conversion_rate = 0.02
        
        # Calculate incremental metrics
        incremental_revenue = total_revenue * (1 - baseline_conversion_rate)
        total_spend = self.payouts_df['total_payout'].sum()
        
        incremental_roas = incremental_revenue / total_spend if total_spend > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'incremental_revenue': incremental_revenue,
            'total_spend': total_spend,
            'incremental_roas': incremental_roas,
            'baseline_conversion_rate': baseline_conversion_rate
        }
    
    def calculate_influencer_efficiency_metrics(self):
        """
        Calculate efficiency metrics for each influencer
        """
        # Merge tracking data with influencer info
        influencer_performance = self.tracking_df.groupby('influencer_id').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        # Merge with payouts
        influencer_payouts = self.payouts_df.groupby('influencer_id')['total_payout'].sum().reset_index()
        influencer_performance = influencer_performance.merge(influencer_payouts, on='influencer_id', how='left')
        influencer_performance['total_payout'] = influencer_performance['total_payout'].fillna(0)
        
        # Merge with influencer details
        influencer_performance = influencer_performance.merge(
            self.influencers_df[['ID', 'name', 'category', 'platform', 'follower_count']], 
            left_on='influencer_id', 
            right_on='ID'
        )
        
        # Calculate efficiency metrics
        influencer_performance['roi'] = ((influencer_performance['revenue'] - influencer_performance['total_payout']) / 
                                       influencer_performance['total_payout'] * 100).fillna(0)
        influencer_performance['roas'] = (influencer_performance['revenue'] / 
                                        influencer_performance['total_payout']).fillna(0)
        influencer_performance['cost_per_order'] = (influencer_performance['total_payout'] / 
                                                   influencer_performance['orders']).fillna(0)
        influencer_performance['revenue_per_follower'] = (influencer_performance['revenue'] / 
                                                        influencer_performance['follower_count']).fillna(0)
        
        return influencer_performance
    
    def identify_top_performers(self, metric='roi', top_n=10):
        """
        Identify top performing influencers based on specified metric
        """
        influencer_metrics = self.calculate_influencer_efficiency_metrics()
        
        if metric == 'roi':
            top_performers = influencer_metrics.nlargest(top_n, 'roi')
        elif metric == 'roas':
            top_performers = influencer_metrics.nlargest(top_n, 'roas')
        elif metric == 'revenue':
            top_performers = influencer_metrics.nlargest(top_n, 'revenue')
        elif metric == 'efficiency':
            # Custom efficiency score combining multiple factors
            influencer_metrics['efficiency_score'] = (
                influencer_metrics['roi'] * 0.4 + 
                influencer_metrics['roas'] * 20 + 
                influencer_metrics['revenue_per_follower'] * 1000
            )
            top_performers = influencer_metrics.nlargest(top_n, 'efficiency_score')
        else:
            top_performers = influencer_metrics.nlargest(top_n, 'revenue')
        
        return top_performers
    
    def identify_poor_performers(self, roi_threshold=50, roas_threshold=2.0):
        """
        Identify poorly performing influencers based on ROI and ROAS thresholds
        """
        influencer_metrics = self.calculate_influencer_efficiency_metrics()
        
        poor_performers = influencer_metrics[
            (influencer_metrics['roi'] < roi_threshold) | 
            (influencer_metrics['roas'] < roas_threshold)
        ]
        
        return poor_performers.sort_values('roi')
    
    def analyze_campaign_performance(self):
        """
        Analyze performance by campaign
        """
        campaign_performance = self.tracking_df.groupby('campaign').agg({
            'revenue': 'sum',
            'orders': 'sum',
            'influencer_id': 'nunique'
        }).reset_index()
        
        campaign_performance.rename(columns={'influencer_id': 'unique_influencers'}, inplace=True)
        
        # Calculate campaign-level payouts
        campaign_payouts = self.tracking_df.merge(
            self.payouts_df, on='influencer_id', how='left'
        ).groupby('campaign')['total_payout'].sum().reset_index()
        
        campaign_performance = campaign_performance.merge(campaign_payouts, on='campaign', how='left')
        campaign_performance['total_payout'] = campaign_performance['total_payout'].fillna(0)
        
        # Calculate campaign metrics
        campaign_performance['roi'] = ((campaign_performance['revenue'] - campaign_performance['total_payout']) / 
                                     campaign_performance['total_payout'] * 100).fillna(0)
        campaign_performance['roas'] = (campaign_performance['revenue'] / 
                                      campaign_performance['total_payout']).fillna(0)
        campaign_performance['avg_revenue_per_influencer'] = (campaign_performance['revenue'] / 
                                                            campaign_performance['unique_influencers'])
        
        return campaign_performance
    
    def analyze_platform_performance(self):
        """
        Analyze performance by platform
        """
        platform_performance = self.tracking_df.groupby('source').agg({
            'revenue': 'sum',
            'orders': 'sum',
            'influencer_id': 'nunique'
        }).reset_index()
        
        platform_performance.rename(columns={'source': 'platform', 'influencer_id': 'unique_influencers'}, inplace=True)
        
        # Calculate platform-level payouts
        platform_payouts = self.tracking_df.merge(
            self.payouts_df, on='influencer_id', how='left'
        ).groupby('source')['total_payout'].sum().reset_index()
        platform_payouts.rename(columns={'source': 'platform'}, inplace=True)
        
        platform_performance = platform_performance.merge(platform_payouts, on='platform', how='left')
        platform_performance['total_payout'] = platform_performance['total_payout'].fillna(0)
        
        # Calculate platform metrics
        platform_performance['roi'] = ((platform_performance['revenue'] - platform_performance['total_payout']) / 
                                      platform_performance['total_payout'] * 100).fillna(0)
        platform_performance['roas'] = (platform_performance['revenue'] / 
                                       platform_performance['total_payout']).fillna(0)
        platform_performance['avg_order_value'] = (platform_performance['revenue'] / 
                                                  platform_performance['orders']).fillna(0)
        
        return platform_performance
    
    def calculate_cohort_analysis(self):
        """
        Perform cohort analysis based on influencer onboarding dates
        """
        # Simulate onboarding dates (in real scenario, this would be actual data)
        np.random.seed(42)
        onboarding_dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='W')
        
        influencer_cohorts = self.influencers_df.copy()
        influencer_cohorts['onboarding_date'] = np.random.choice(onboarding_dates, len(self.influencers_df))
        influencer_cohorts['cohort_month'] = influencer_cohorts['onboarding_date'].dt.to_period('M')
        
        # Merge with performance data
        cohort_performance = self.tracking_df.merge(
            influencer_cohorts[['ID', 'cohort_month']], 
            left_on='influencer_id', 
            right_on='ID'
        )
        
        # Calculate cohort metrics
        cohort_metrics = cohort_performance.groupby('cohort_month').agg({
            'revenue': 'sum',
            'orders': 'sum',
            'influencer_id': 'nunique'
        }).reset_index()
        
        return cohort_metrics
    
    def generate_insights_summary(self):
        """
        Generate comprehensive insights summary
        """
        incremental_roas = self.calculate_incremental_roas()
        top_performers = self.identify_top_performers('efficiency', 5)
        poor_performers = self.identify_poor_performers()
        campaign_performance = self.analyze_campaign_performance()
        platform_performance = self.analyze_platform_performance()
        
        insights = {
            'overall_performance': {
                'total_revenue': incremental_roas['total_revenue'],
                'incremental_revenue': incremental_roas['incremental_revenue'],
                'total_spend': incremental_roas['total_spend'],
                'incremental_roas': incremental_roas['incremental_roas'],
                'overall_roi': ((incremental_roas['total_revenue'] - incremental_roas['total_spend']) / 
                              incremental_roas['total_spend'] * 100) if incremental_roas['total_spend'] > 0 else 0
            },
            'top_performers': top_performers[['name', 'category', 'platform', 'revenue', 'roi', 'roas']].to_dict('records'),
            'poor_performers_count': len(poor_performers),
            'best_campaign': campaign_performance.loc[campaign_performance['roi'].idxmax(), 'campaign'] if not campaign_performance.empty else 'N/A',
            'best_platform': platform_performance.loc[platform_performance['roi'].idxmax(), 'platform'] if not platform_performance.empty else 'N/A',
            'recommendations': self._generate_recommendations(top_performers, poor_performers, campaign_performance, platform_performance)
        }
        
        return insights
    
    def _generate_recommendations(self, top_performers, poor_performers, campaign_performance, platform_performance):
        """
        Generate actionable recommendations based on analysis
        """
        recommendations = []
        
        # Top performer insights
        if not top_performers.empty:
            top_category = top_performers['category'].mode().iloc[0] if not top_performers['category'].mode().empty else 'N/A'
            top_platform = top_performers['platform'].mode().iloc[0] if not top_performers['platform'].mode().empty else 'N/A'
            recommendations.append(f"Focus on {top_category} influencers on {top_platform} platform for highest ROI")
        
        # Poor performer insights
        if len(poor_performers) > 0:
            recommendations.append(f"Review and optimize {len(poor_performers)} underperforming influencers")
        
        # Campaign insights
        if not campaign_performance.empty:
            best_campaign = campaign_performance.loc[campaign_performance['roi'].idxmax()]
            recommendations.append(f"Replicate success factors from '{best_campaign['campaign']}' campaign (ROI: {best_campaign['roi']:.1f}%)")
        
        # Platform insights
        if not platform_performance.empty:
            best_platform = platform_performance.loc[platform_performance['roas'].idxmax()]
            recommendations.append(f"Increase investment in {best_platform['platform']} platform (ROAS: {best_platform['roas']:.2f}x)")
        
        return recommendations

# Usage example
if __name__ == "__main__":
    # Load data
    influencers_df = pd.read_csv("data/influencers.csv")
    posts_df = pd.read_csv("data/posts.csv")
    tracking_df = pd.read_csv("data/tracking_data.csv")
    payouts_df = pd.read_csv("data/payouts.csv")
    
    # Initialize analytics
    analytics = InfluencerROIAnalytics(influencers_df, posts_df, tracking_df, payouts_df)
    
    # Generate insights
    insights = analytics.generate_insights_summary()
    
    print("=== HealthKart Influencer Campaign Analytics ===")
    print(f"Total Revenue: ₹{insights['overall_performance']['total_revenue']:,.0f}")
    print(f"Incremental Revenue: ₹{insights['overall_performance']['incremental_revenue']:,.0f}")
    print(f"Total Spend: ₹{insights['overall_performance']['total_spend']:,.0f}")
    print(f"Incremental ROAS: {insights['overall_performance']['incremental_roas']:.2f}x")
    print(f"Overall ROI: {insights['overall_performance']['overall_roi']:.1f}%")
    print(f"\nTop Performers: {len(insights['top_performers'])}")
    print(f"Poor Performers: {insights['poor_performers_count']}")
    print(f"Best Campaign: {insights['best_campaign']}")
    print(f"Best Platform: {insights['best_platform']}")
    print("\nRecommendations:")
    for i, rec in enumerate(insights['recommendations'], 1):
        print(f"{i}. {rec}")

