import pandas as pd
from sklearn.cluster import KMeans
import os
import numpy as np

os.environ['OMP_NUM_THREADS'] = '1'
# Load the data
file_path = r'D:\PythonProjects\datenSet\Data.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Convert 'CreatedAt' to datetime if needed
data['CreatedAt'] = pd.to_datetime(data['CreatedAt'], errors='coerce')
#region userGroupCreation
poster_stats = data.groupby('UserId').agg(
    #main info
    UserName=('UserScreenName', 'first'),
    Followers=('UserFollowersCount', 'first'),

    #tweet stuff
    TotalTweets=('UserId', 'count'),

    #likes
    TotalLikes=('FavoriteCount / LikeCount', 'sum'),
    AverageLikes=('FavoriteCount / LikeCount', 'median'),
    MeanLikes=('FavoriteCount / LikeCount', 'mean'),

    #replies
    TotalReplies=('IsReplyToStatusId', lambda x: x.notnull().sum()),
    AverageReplies=('IsReplyToStatusId', lambda x: x.notnull().median()),
    MeanReplies=('IsReplyToStatusId', lambda x: x.notnull().mean()),

    #extra
    TotalRetweets=('RetweetCount', 'sum'),
    AverageRetweets=('RetweetCount', 'median'),
    MeanRetweets=('RetweetCount', 'mean')
).reset_index()

poster_stats = poster_stats.round(2)
#endregion

#region K-Means preparation
poster_stats['LogFollowers'] = np.log1p(poster_stats['Followers'])
poster_stats['LogRetweets'] = np.log1p(poster_stats['TotalRetweets'])
X = poster_stats[['LogFollowers', 'LogRetweets']]
kmeans = KMeans(n_clusters=10, random_state=0)
poster_stats['PopularityCluster'] = kmeans.fit_predict(X)

#sorting
cluster_means = poster_stats.groupby('PopularityCluster')['Followers'].mean()
sorted_clusters = cluster_means.sort_values().index
cluster_mapping = {old_label: new_label for new_label, old_label in enumerate(sorted_clusters)}
poster_stats['PopularityCluster'] = poster_stats['PopularityCluster'].map(cluster_mapping)
poster_stats = poster_stats.sort_values(by=['PopularityCluster', 'Followers'], ascending=False).reset_index(drop=True)
poster_stats = poster_stats.round(2)
#endregion

#region globalGroupCreation
group_stats = poster_stats.groupby('PopularityCluster').agg(
    #UsersInfo
    TotalUsers=('UserId', 'count'),

    #followersInfo
    TotalFollowers=('Followers', 'sum'),
    AverageFollowers=('Followers', 'mean'),
    MedianFollowers=('Followers', 'median'),

    #PostsInfo
    TotalPosts=('TotalTweets', 'sum'),
    AveragePosts=('TotalTweets', 'mean'),
    MedianPosts=('TotalTweets', 'median'),

    #RepliesInfo
    TotalReplies=('TotalReplies', 'sum'),
    AverageReplies=('TotalReplies', 'mean'),
    MedianReplies=('TotalReplies', 'median'),

    #RetweetsInfo
    TotalRetweets=('TotalRetweets', 'sum'),
    AverageRetweets=('TotalRetweets', 'mean'),
    MedianRetweets=('TotalRetweets', 'median'),

    #LikesInfo
    TotalLikes=('TotalLikes', 'sum'),
    AverageLikes=('TotalLikes', 'mean'),
    MedianLikes=('TotalLikes', 'median')

).reset_index()

group_stats = group_stats.round(2)
#endregion

# Display the grouped poster statistics
poster_stats.to_csv(r'D:\PythonProjects\datenSet\poster_stats.csv', index=False)
group_stats.to_csv(r'D:\PythonProjects\datenSet\group_stats.csv', index=False)
print("finished successfully")

