import pandas as pd
file_path = r'D:\PythonProjects\datenSet\Data.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

data['CreatedAt'] = pd.to_datetime(data['CreatedAt'], errors='coerce')
data['TotalEngagement'] = data['RetweetCount'] + data['FavoriteCount / LikeCount']

top_misinfo_posts = data.sort_values(by='TotalEngagement', ascending=False).head(10)

responses_to_top_posts = data[data['IsReplyToStatusId'].isin(top_misinfo_posts['Id'])]

merged_data = top_misinfo_posts.merge(
    responses_to_top_posts,
    left_on='Id',
    right_on='IsReplyToStatusId',
    suffixes=('_misinfo', '_response'),
    how='left'
)

merged_data.sort_values(by='TotalEngagement_misinfo', ascending=False)

for post_id, group in merged_data.groupby(by='Id_misinfo', sort=False):
    original_post = group.iloc[0]
    print(f"\nMisinformation Post (Id: {post_id}):")
    print(f"Poster: {original_post['UserScreenName_misinfo']}")
    print(f"Text: \n{original_post['Text_misinfo']}\n-  -  -  -  -  -")
    print(f"Retweets: {original_post['RetweetCount_misinfo']}, Likes: {original_post['FavoriteCount / LikeCount_misinfo']}")

    responses = group[['UserScreenName_response', 'Text_response', 'RetweetCount_response', 'FavoriteCount / LikeCount_response']]
    print(f"\nResponses ({len(responses)} total):")
    print(responses.to_string(index=False))
    print("-" * 80)
