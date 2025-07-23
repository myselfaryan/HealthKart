
import pandas as pd

def validate_data():
    try:
        influencers_df = pd.read_csv("data/influencers.csv")
        posts_df = pd.read_csv("data/posts.csv")
        tracking_data_df = pd.read_csv("data/tracking_data.csv")
        payouts_df = pd.read_csv("data/payouts.csv")

        print("--- Data Loading Check ---")
        print(f"Influencers: {influencers_df.shape[0]} rows")
        print(f"Posts: {posts_df.shape[0]} rows")
        print(f"Tracking Data: {tracking_data_df.shape[0]} rows")
        print(f"Payouts: {payouts_df.shape[0]} rows")

        print("\n--- Data Integrity Checks ---")
        # Check for unique influencer IDs
        assert influencers_df["ID"].is_unique, "Influencer IDs are not unique!"
        print("Influencer IDs are unique.")

        # Check if all influencer_ids in posts, tracking_data, and payouts exist in influencers_df
        invalid_post_influencers = posts_df[~posts_df["influencer_id"].isin(influencers_df["ID"])]
        assert invalid_post_influencers.empty, f"Invalid influencer_ids in posts: {{invalid_post_influencers['influencer_id'].unique().tolist()}}"
        print("All influencer_ids in posts are valid.")

        invalid_tracking_influencers = tracking_data_df[~tracking_data_df["influencer_id"].isin(influencers_df["ID"])]
        assert invalid_tracking_influencers.empty, f"Invalid influencer_ids in tracking_data: {{invalid_tracking_influencers['influencer_id'].unique().tolist()}}"
        print("All influencer_ids in tracking_data are valid.")

        invalid_payout_influencers = payouts_df[~payouts_df["influencer_id"].isin(influencers_df["ID"])]
        assert invalid_payout_influencers.empty, f"Invalid influencer_ids in payouts: {{invalid_payout_influencers['influencer_id'].unique().tolist()}}"
        print("All influencer_ids in payouts are valid.")

        # Check for expected columns
        expected_influencer_cols = ["ID", "name", "category", "gender", "follower_count", "platform"]
        assert all(col in influencers_df.columns for col in expected_influencer_cols), "Missing columns in influencers_df"
        print("Influencers DataFrame has all expected columns.")

        expected_posts_cols = ["influencer_id", "platform", "date", "URL", "caption", "reach", "likes", "comments"]
        assert all(col in posts_df.columns for col in expected_posts_cols), "Missing columns in posts_df"
        print("Posts DataFrame has all expected columns.")

        expected_tracking_cols = ["source", "campaign", "influencer_id", "user_id", "product", "date", "orders", "revenue"]
        assert all(col in tracking_data_df.columns for col in expected_tracking_cols), "Missing columns in tracking_data_df"
        print("Tracking Data DataFrame has all expected columns.")

        expected_payouts_cols = ["influencer_id", "basis", "rate", "orders", "total_payout"]
        assert all(col in payouts_df.columns for col in expected_payouts_cols), "Missing columns in payouts_df"
        print("Payouts DataFrame has all expected columns.")

        print("\nData validation successful!")

    except AssertionError as e:
        print(f"Data validation failed: {e}")
    except FileNotFoundError as e:
                print(f"Error: {e}. Make sure data files are in the data/ directory")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    validate_data()


