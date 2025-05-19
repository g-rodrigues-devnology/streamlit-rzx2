from praw import Reddit
import json

reddit: Reddit = Reddit(
    client_id="Nr2kMFxXC7Y4egyczqe4Mw",
    client_secret="UZU2tfn5U2w8mx7CZIWRX0MSP2b7qg",
    user_agent="unemat-foradecasa/0.1 by u/bwowndwawf",
)

sub = 'foradecasa'

def get_after(json) -> str | None:
    return json['data']['after']

def fetch_all_data(sort: str):
    subreddit = reddit.subreddit(sub)

    if sort == 'new':
        posts = subreddit.new(limit=None)
    elif sort == 'hot':
        posts = subreddit.hot(limit=None)
    elif sort == 'top':
        posts = subreddit.top(limit=None)
    else:
        raise ValueError(f"Unsupported sort type: {sort}")

    all_data = []
    i = 0

    for post in posts:
        print(f'Fetching post {i + 1} of "unknown"')
        i += 1

        post_data = {
            'id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'url': post.url,
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'ups': post.ups,
            'downs': post.downs,
            'permalink': post.permalink,
            'flair': post.link_flair_text,
            'author': post.author.name if post.author else None,
            'comments': []
        }

        post.comments.replace_more(limit=None)

        for comment in post.comments:
            post_data['comments'].append(
                map_comments(comment)
            )

        all_data.append(post_data)

    return all_data
    
def map_comments(comment):
    data = {
        'id': comment.id,
        'body': comment.body,
        'score': comment.score,
        'created_utc': comment.created_utc,
        'author': comment.author.name if comment.author else None,
        'controversiality': comment.controversiality,
        'permalink': comment.permalink,
        'distinguished': comment.distinguished,
        'is_submitter': comment.is_submitter,
        'ups': comment.ups,
        'downs': comment.downs,
        'replies': [],
    }

    for child in comment.replies:
        data['replies'].append(
            map_comments(child)
        )
    
    return data

def write_to_file(sort: str, posts: list):
    with open(f'{sort}.json', 'w') as f:
        data = json.dumps(posts, indent=4)
        f.write(data)

new = fetch_all_data('new')
write_to_file('data', new)

print(f'Fetched {len(new)} new posts')


