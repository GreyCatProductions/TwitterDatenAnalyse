import pandas as pd

# Load your dataset
file_path = r'D:\PythonProjects\datenSet\Data.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Convert 'CreatedAt' and 'UserCreatedAt' to datetime format for analysis
data['CreatedAt'] = pd.to_datetime(data['CreatedAt'], errors='coerce')
data['UserCreatedAt'] = pd.to_datetime(data['UserCreatedAt'], errors='coerce')


# 1. Basic Information
def print_basic_info(data):
    print("Basic Dataset Information:")
    print(f"Total number of tweets: {len(data)}")
    print(f"Number of unique users: {data['UserId'].nunique()}")
    print(f"First tweet date: {data['CreatedAt'].min()}")
    print(f"Most recent tweet date: {data['CreatedAt'].max()}")
    print(f"Total retweets: {data['RetweetCount'].sum()}")
    print(f"Total likes: {data['FavoriteCount / LikeCount'].sum()}")
    print()


# 2. Top 5 Users by Follower Count
def top_users_by_followers(data):
    print("Top 5 Users by Follower Count:")
    top_users = data[['UserScreenName', 'UserFollowersCount']].drop_duplicates().sort_values(by='UserFollowersCount',
                                                                                             ascending=False)
    print(top_users.to_string(index=False))
    print()


# 3. Tweet Engagement (Retweets and Likes)
def tweet_engagement_stats(data):
    print("Tweet Engagement Stats:")
    avg_retweets = data['RetweetCount'].mean()
    avg_likes = data['FavoriteCount / LikeCount'].mean()
    max_retweets = data['RetweetCount'].max()
    max_likes = data['FavoriteCount / LikeCount'].max()

    print(f"Average retweets per tweet: {avg_retweets:.2f}")
    print(f"Average likes per tweet: {avg_likes:.2f}")
    print(f"Max retweets on a single tweet: {max_retweets}")
    print(f"Max likes on a single tweet: {max_likes}")
    print()


# 4. Most Active Users by Tweet Count
def most_active_users(data):
    print("Top 5 Most Active Users by Tweet Count:")
    active_users = data['UserScreenName'].value_counts().head(5)
    print(active_users.to_string())
    print()


# 5. Retweets vs Likes Correlation
def retweets_vs_likes_correlation(data):
    print("Retweets vs Likes Correlation:")
    correlation = data['RetweetCount'].corr(data['FavoriteCount / LikeCount'])
    print(f"Correlation between retweets and likes: {correlation:.2f}")
    print()


# 6. Interaction Spread (Using 'Ir' fields if they represent interaction)
def interaction_spread(data):
    if 'IrRetweetCount' in data.columns and 'IrFavoriteCount / IrLikeCount' in data.columns:
        print("Interaction Spread Stats (Interaction with Retweets and Likes):")
        total_ir_retweets = data['IrRetweetCount'].sum()
        total_ir_likes = data['IrFavoriteCount / IrLikeCount'].sum()
        avg_ir_retweets = data['IrRetweetCount'].mean()
        avg_ir_likes = data['IrFavoriteCount / IrLikeCount'].mean()

        print(f"Total retweets from interactions: {total_ir_retweets}")
        print(f"Total likes from interactions: {total_ir_likes}")
        print(f"Average retweets from interactions: {avg_ir_retweets:.2f}")
        print(f"Average likes from interactions: {avg_ir_likes:.2f}")
        print()


# Calling all functions to print the analysis
print_basic_info(data)
top_users_by_followers(data)
tweet_engagement_stats(data)
most_active_users(data)
retweets_vs_likes_correlation(data)
interaction_spread(data)

