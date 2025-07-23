
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_influencers(num_influencers=50):
    categories = ['Fitness', 'Beauty', 'Gaming', 'Lifestyle', 'Food']
    platforms = ['Instagram', 'YouTube', 'Twitter', 'TikTok']
    genders = ['Male', 'Female', 'Other']
    
    data = {
        'ID': [f'INF{i:03d}' for i in range(num_influencers)],
        'name': [f'Influencer_{i}' for i in range(num_influencers)],
        'category': np.random.choice(categories, num_influencers),
        'gender': np.random.choice(genders, num_influencers),
        'follower_count': np.random.randint(10000, 1000000, num_influencers),
        'platform': np.random.choice(platforms, num_influencers, p=[0.4, 0.3, 0.2, 0.1])
    }
    return pd.DataFrame(data)

def generate_posts(influencers_df, num_posts=200):
    posts = []
    start_date = datetime(2024, 1, 1)
    for _ in range(num_posts):
        influencer = influencers_df.sample(1).iloc[0]
        post_date = start_date + timedelta(days=np.random.randint(0, 365))
        posts.append({
            'influencer_id': influencer['ID'],
            'platform': influencer['platform'],
            'date': post_date.strftime('%Y-%m-%d'),
            'URL': f'http://example.com/post/{np.random.randint(1000, 9999)}',
            'caption': f'Check out this amazing product! #{np.random.choice(["HealthKart", "MuscleBlaze", "HKVitals"])}',
            'reach': np.random.randint(5000, 500000),
            'likes': np.random.randint(1000, 100000),
            'comments': np.random.randint(50, 5000)
        })
    return pd.DataFrame(posts)

def generate_tracking_data(influencers_df, num_entries=1000):
    tracking_data = []
    products = ['Protein Powder', 'Vitamins', 'Weight Gainer', 'Kids Nutrition']
    campaigns = ['SummerSale', 'NewYearPromo', 'FitnessChallenge']
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_entries):
        influencer = influencers_df.sample(1).iloc[0]
        entry_date = start_date + timedelta(days=np.random.randint(0, 365))
        tracking_data.append({
            'source': influencer['platform'],
            'campaign': np.random.choice(campaigns),
            'influencer_id': influencer['ID'],
            'user_id': f'USER{np.random.randint(10000, 99999)}',
            'product': np.random.choice(products),
            'date': entry_date.strftime('%Y-%m-%d'),
            'orders': np.random.randint(1, 10),
            'revenue': np.random.uniform(50, 500)
        })
    return pd.DataFrame(tracking_data)

def generate_payouts(influencers_df, tracking_df, num_payouts=100):
    payouts = []
    basis_options = ['post', 'order']
    
    for _ in range(num_payouts):
        influencer = influencers_df.sample(1).iloc[0]
        basis = np.random.choice(basis_options)
        rate = np.random.uniform(50, 500) if basis == 'post' else np.random.uniform(5, 20)
        
        if basis == 'order':
            # Link payouts to actual orders from tracking_data for more realistic simulation
            influencer_orders = tracking_df[tracking_df['influencer_id'] == influencer['ID']]['orders'].sum()
            total_payout = influencer_orders * rate
            orders_count = influencer_orders
        else:
            total_payout = rate
            orders_count = 0 # Not applicable for post-based payouts

        payouts.append({
            'influencer_id': influencer['ID'],
            'basis': basis,
            'rate': rate,
            'orders': orders_count,
            'total_payout': total_payout
        })
    return pd.DataFrame(payouts)

if __name__ == '__main__':
    influencers_df = generate_influencers()
    posts_df = generate_posts(influencers_df)
    tracking_data_df = generate_tracking_data(influencers_df)
    payouts_df = generate_payouts(influencers_df, tracking_data_df)

    influencers_df.to_csv('data/influencers.csv', index=False)
    posts_df.to_csv('data/posts.csv', index=False)
    tracking_data_df.to_csv('data/tracking_data.csv', index=False)
    payouts_df.to_csv('data/payouts.csv', index=False)

        print("Simulated datasets saved to data/")


