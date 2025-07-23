#!/usr/bin/env python3
"""
Test validation script for HealthKart Influencer Campaign ROI Dashboard
"""

import pandas as pd
import numpy as np
import sys
import os
from advanced_analytics import InfluencerROIAnalytics
from insights_generator import InsightsGenerator

def test_data_loading():
    """Test data loading functionality"""
    print("Testing data loading...")
    try:
        influencers_df = pd.read_csv("data/influencers.csv")
        posts_df = pd.read_csv("data/posts.csv")
        tracking_df = pd.read_csv("data/tracking_data.csv")
        payouts_df = pd.read_csv("data/payouts.csv")
        
        print(f"✓ Influencers data: {len(influencers_df)} records")
        print(f"✓ Posts data: {len(posts_df)} records")
        print(f"✓ Tracking data: {len(tracking_df)} records")
        print(f"✓ Payouts data: {len(payouts_df)} records")
        
        return influencers_df, posts_df, tracking_df, payouts_df
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return None, None, None, None

def test_analytics_calculations(influencers_df, posts_df, tracking_df, payouts_df):
    """Test analytics calculations"""
    print("\nTesting analytics calculations...")
    try:
        analytics = InfluencerROIAnalytics(influencers_df, posts_df, tracking_df, payouts_df)
        
        # Test incremental ROAS calculation
        incremental_roas = analytics.calculate_incremental_roas()
        print(f"✓ Incremental ROAS: {incremental_roas['incremental_roas']:.2f}x")
        
        # Test influencer efficiency metrics
        influencer_metrics = analytics.calculate_influencer_efficiency_metrics()
        print(f"✓ Influencer metrics calculated for {len(influencer_metrics)} influencers")
        
        # Test top performers identification
        top_performers = analytics.identify_top_performers('efficiency', 5)
        print(f"✓ Top performers identified: {len(top_performers)} influencers")
        
        # Test poor performers identification
        poor_performers = analytics.identify_poor_performers()
        print(f"✓ Poor performers identified: {len(poor_performers)} influencers")
        
        # Test campaign performance analysis
        campaign_performance = analytics.analyze_campaign_performance()
        print(f"✓ Campaign analysis completed for {len(campaign_performance)} campaigns")
        
        # Test platform performance analysis
        platform_performance = analytics.analyze_platform_performance()
        print(f"✓ Platform analysis completed for {len(platform_performance)} platforms")
        
        return analytics
    except Exception as e:
        print(f"✗ Analytics calculations failed: {e}")
        return None

def test_insights_generation(analytics):
    """Test insights generation"""
    print("\nTesting insights generation...")
    try:
        insights_gen = InsightsGenerator(analytics)
        
        # Test persona analysis
        persona_analysis = insights_gen.generate_persona_analysis()
        print(f"✓ Persona analysis: {len(persona_analysis)} personas analyzed")
        
        # Test seasonal trends
        seasonal_trends = insights_gen.generate_seasonal_trends()
        print(f"✓ Seasonal trends: Monthly, weekly, and daily patterns analyzed")
        
        # Test engagement analysis
        engagement_analysis = insights_gen.generate_engagement_analysis()
        print(f"✓ Engagement analysis: Category and platform metrics calculated")
        
        # Test cost efficiency analysis
        cost_efficiency = insights_gen.generate_cost_efficiency_analysis()
        print(f"✓ Cost efficiency: Segment, category, and platform analysis completed")
        
        # Test predictive insights
        predictive_insights = insights_gen.generate_predictive_insights()
        print(f"✓ Predictive insights: {len(predictive_insights)} insights generated")
        
        # Test executive summary
        executive_summary = insights_gen.create_executive_summary()
        print(f"✓ Executive summary: Complete overview generated")
        
        return insights_gen
    except Exception as e:
        print(f"✗ Insights generation failed: {e}")
        return None

def test_data_validation():
    """Test data validation and integrity"""
    print("\nTesting data validation...")
    try:
        influencers_df = pd.read_csv("data/influencers.csv")
        posts_df = pd.read_csv("data/posts.csv")
        tracking_df = pd.read_csv("data/tracking_data.csv")
        payouts_df = pd.read_csv("data/payouts.csv")
        
        # Check for required columns
        required_influencer_cols = ['ID', 'name', 'category', 'gender', 'follower_count', 'platform']
        required_posts_cols = ['influencer_id', 'platform', 'date', 'URL', 'caption', 'reach', 'likes', 'comments']
        required_tracking_cols = ['source', 'campaign', 'influencer_id', 'user_id', 'product', 'date', 'orders', 'revenue']
        required_payouts_cols = ['influencer_id', 'basis', 'rate', 'orders', 'total_payout']
        
        missing_cols = []
        for col in required_influencer_cols:
            if col not in influencers_df.columns:
                missing_cols.append(f"influencers.{col}")
        
        for col in required_posts_cols:
            if col not in posts_df.columns:
                missing_cols.append(f"posts.{col}")
        
        for col in required_tracking_cols:
            if col not in tracking_df.columns:
                missing_cols.append(f"tracking.{col}")
        
        for col in required_payouts_cols:
            if col not in payouts_df.columns:
                missing_cols.append(f"payouts.{col}")
        
        if missing_cols:
            print(f"✗ Missing required columns: {missing_cols}")
            return False
        else:
            print("✓ All required columns present")
        
        # Check data relationships
        influencer_ids = set(influencers_df['ID'])
        posts_influencer_ids = set(posts_df['influencer_id'])
        tracking_influencer_ids = set(tracking_df['influencer_id'])
        payouts_influencer_ids = set(payouts_df['influencer_id'])
        
        orphaned_posts = posts_influencer_ids - influencer_ids
        orphaned_tracking = tracking_influencer_ids - influencer_ids
        orphaned_payouts = payouts_influencer_ids - influencer_ids
        
        if orphaned_posts:
            print(f"⚠ Warning: {len(orphaned_posts)} orphaned posts (no matching influencer)")
        if orphaned_tracking:
            print(f"⚠ Warning: {len(orphaned_tracking)} orphaned tracking records")
        if orphaned_payouts:
            print(f"⚠ Warning: {len(orphaned_payouts)} orphaned payout records")
        
        if not (orphaned_posts or orphaned_tracking or orphaned_payouts):
            print("✓ Data relationships validated")
        
        # Check for null values in critical columns
        critical_nulls = []
        if influencers_df['ID'].isnull().any():
            critical_nulls.append("influencer IDs")
        if tracking_df['revenue'].isnull().any():
            critical_nulls.append("revenue data")
        if payouts_df['total_payout'].isnull().any():
            critical_nulls.append("payout data")
        
        if critical_nulls:
            print(f"✗ Critical null values found in: {critical_nulls}")
            return False
        else:
            print("✓ No critical null values found")
        
        return True
    except Exception as e:
        print(f"✗ Data validation failed: {e}")
        return False

def test_calculations_accuracy():
    """Test calculation accuracy with known values"""
    print("\nTesting calculation accuracy...")
    try:
        # Load data
        tracking_df = pd.read_csv("data/tracking_data.csv")
        payouts_df = pd.read_csv("data/payouts.csv")
        
        # Manual calculations for verification
        total_revenue = tracking_df['revenue'].sum()
        total_orders = tracking_df['orders'].sum()
        total_payouts = payouts_df['total_payout'].sum()
        manual_roi = ((total_revenue - total_payouts) / total_payouts * 100) if total_payouts > 0 else 0
        manual_roas = (total_revenue / total_payouts) if total_payouts > 0 else 0
        
        print(f"✓ Manual calculations:")
        print(f"  Total Revenue: ₹{total_revenue:,.0f}")
        print(f"  Total Orders: {total_orders:,.0f}")
        print(f"  Total Payouts: ₹{total_payouts:,.0f}")
        print(f"  Manual ROI: {manual_roi:.1f}%")
        print(f"  Manual ROAS: {manual_roas:.2f}x")
        
        # Compare with analytics calculations
        influencers_df = pd.read_csv("data/influencers.csv")
        posts_df = pd.read_csv("data/posts.csv")
        analytics = InfluencerROIAnalytics(influencers_df, posts_df, tracking_df, payouts_df)
        incremental_roas = analytics.calculate_incremental_roas()
        
        calculated_roi = ((incremental_roas['total_revenue'] - incremental_roas['total_spend']) / 
                         incremental_roas['total_spend'] * 100) if incremental_roas['total_spend'] > 0 else 0
        
        # Allow for small floating point differences
        revenue_match = abs(total_revenue - incremental_roas['total_revenue']) < 1
        payouts_match = abs(total_payouts - incremental_roas['total_spend']) < 1
        roi_match = abs(manual_roi - calculated_roi) < 0.1
        
        if revenue_match and payouts_match and roi_match:
            print("✓ Calculation accuracy verified")
            return True
        else:
            print("✗ Calculation discrepancies found")
            print(f"  Revenue match: {revenue_match}")
            print(f"  Payouts match: {payouts_match}")
            print(f"  ROI match: {roi_match}")
            return False
    except Exception as e:
        print(f"✗ Calculation accuracy test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("HealthKart Dashboard Test Suite")
    print("=" * 60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    test_results = []
    
    # Test 1: Data Loading
    influencers_df, posts_df, tracking_df, payouts_df = test_data_loading()
    test_results.append(all(df is not None for df in [influencers_df, posts_df, tracking_df, payouts_df]))
    
    if not test_results[-1]:
        print("\n✗ Cannot proceed with other tests due to data loading failure")
        sys.exit(1)
    
    # Test 2: Data Validation
    test_results.append(test_data_validation())
    
    # Test 3: Analytics Calculations
    analytics = test_analytics_calculations(influencers_df, posts_df, tracking_df, payouts_df)
    test_results.append(analytics is not None)
    
    # Test 4: Insights Generation
    if analytics:
        insights_gen = test_insights_generation(analytics)
        test_results.append(insights_gen is not None)
    else:
        test_results.append(False)
    
    # Test 5: Calculation Accuracy
    test_results.append(test_calculations_accuracy())
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    test_names = [
        "Data Loading",
        "Data Validation", 
        "Analytics Calculations",
        "Insights Generation",
        "Calculation Accuracy"
    ]
    
    passed = sum(test_results)
    total = len(test_results)
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{i+1}. {name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please review and fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

