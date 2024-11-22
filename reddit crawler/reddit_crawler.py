import praw
from prawcore import NotFound
import csv
from datetime import datetime, timedelta
import time
# Reddit API credentials
# reddit = praw.Reddit(
#     client_id='your_client_id',
#     client_secret='your_client_secret',
#     user_agent='your_user_agent'
# )


reddit = praw.Reddit(
    client_id= os.environ['RD_CLIENT_ID'],          # config.RD_CLIENT_ID,
    client_secret= os.environ['RD_CLIENT_SECRET'],  # config.RD_CLIENT_SECRET,
    password = os.environ['RD_PASS'],                # config.RD_PASS, 
    user_agent= "test2",
    username= os.environ['USERNAME'],
)


# Function to check if a user's latest post is older than one month
def is_post_older_than_one_month(user):
    try:
        # if not post and not comment (True: means post/comment both are older than 1 month)
        is_post_older = True
        is_comment_older = True
        redditor = reddit.redditor(user.name)
        # Fetch the latest submission of the user
        for submission in redditor.submissions.new(limit=1):
            post_time = datetime.fromtimestamp(submission.created_utc)
            is_post_older = post_time < datetime.now() - timedelta(days=30)
            time.sleep(.2) # prawcore.exceptions.TooManyRequests: received 429 HTTP response
            
        # Fetch latest comment
        for comment in redditor.comments.new(limit=1):
            comment_time = datetime.fromtimestamp(comment.created_utc)
            is_comment_older = comment_time < datetime.now() - timedelta(days=30)
            time.sleep(.1) # prawcore.exceptions.TooManyRequests: received 429 HTTP response

        # print(f'post_older: {is_post_older} comment_older: {is_comment_older}')
        return is_post_older and is_comment_older

    except Exception as e:
        print(f"Error checking posts for user {user.name}: {e}")
        return False

# Function to check all moderators of a subreddit
def check_moderators(subreddit):
    # subreddit = reddit.subreddit(subreddit_name)
    moderators = subreddit.moderator()
    for moderator in moderators:
        if not is_post_older_than_one_month(moderator):
            return False    # at least one of moderator post is not older than one month
        time.sleep(.1) # prawcore.exceptions.TooManyRequests: received 429 HTTP response
    # if no moderator or any moderator has not posted for one month
    return True

def subreddit_exists(subreddit_name):
    exists = True
    try:
        time.sleep(.1) # prawcore.exceptions.TooManyRequests: received 429 HTTP response
        reddit.subreddits.search_by_name(subreddit_name, exact=True)
    except NotFound:
        exists = False
    except Exception as Ex:
        exists = False
        print(Ex)
    return exists

# Subreddits to check
subreddits = ['learnpython', 'Python', 'datascience']  # Add your subreddit names here
subreddit_list_file = open('subreddit_counts.txt','r')

count = 0
start_time = time.time()
# CSV file to store URLswhile count < 10000:

csv_file_name = "subreddits_with_inactive_moderators.csv"
with open(csv_file_name, 'a', newline='') as file:
    writer = csv.writer(file)
    # Write header only if the file is empty
    if file.tell() == 0:
        writer.writerow(['Subreddit', 'Members-Count', 'URL'])
    while count < 10400:
        # 0k-100k subreddits crawled previously, lets crawl 30,000 more.
        count += 1
        # Get subreddit fron the file
        subreddit_name = subreddit_list_file.readline().split('\t')[0] # subreddit_name
    while count < 100000:
        # Get subreddit fron the file
        subreddit_name = subreddit_list_file.readline().split('\t')[0] # subreddit_name
        
        if count%100 == 0:
            print(f'-------------------\n{count}: {subreddit_name}\n-------------------')
        count += 1
        
        
        # for subreddit_name in subreddits:
        if not subreddit_exists(subreddit_name):
            print('does not exist')
            # continue if subreddit does not exists
            continue
        try:
            '''
            subreddit: 'truefmk' exists but cant get subreddit.subscribers : banned due to a violation of Reddit's rules
            '''
            time.sleep(.1) # prawcore.exceptions.TooManyRequests: received 429 HTTP response
            subreddit = reddit.subreddit(subreddit_name)
            members_count = subreddit.subscribers
            if members_count >100:
                # Only check for subreddit with more  than 100 members
                if check_moderators(subreddit):
                    subreddit_url = f'https://www.reddit.com/r/{subreddit_name}/'
                    writer.writerow([subreddit_name, members_count, subreddit_url])
                    print(f"Added {subreddit_name} to CSV file.")
        except Exception as Ex:
            pass
        time.sleep(.15) # prawcore.exceptions.TooManyRequests: received 429 HTTP response

end_time = time.time()
print(f'time: {end_time-start_time}')