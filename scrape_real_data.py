import instaloader
import pandas as pd
import datetime
import time
import os
import random

save_dir = "real_data"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

L = instaloader.Instaloader(
    download_pictures=False,
    download_video_thumbnails=False,
    download_videos=False,
    download_geotags=False,
    download_comments=True,
    sleep=True
)

target_accounts = ['cnbcindonesia', 'katadatacoid', 'kontannews', 'bisniscom', 'idx_channel']
all_comments_data = []
max_posts_per_account = 2
max_comments_per_post = 20

print("Starting real data extraction...")

for account in target_accounts:
    print(f"\n--- Scraping @{account} ---")
    try:
        profile = instaloader.Profile.from_username(L.context, account)
        posts = profile.get_posts()
        
        post_count = 0
        for post in posts:
            if post_count >= max_posts_per_account:
                break
            post_count += 1
            
            caption = post.caption if post.caption else ""
            post_url = f"https://www.instagram.com/p/{post.shortcode}/"
            print(f"[{post_count}] Post: {post_url} | Total Comments: {post.comments}")
            
            comment_count = 0
            try:
                # Need to use post.get_comments()
                for comment in post.get_comments():
                    all_comments_data.append({
                        "post_date": post.date_utc.strftime('%Y-%m-%d'),
                        "account_username": account,
                        "comment_username": comment.owner.username,
                        "comment_text": comment.text,
                        "likes_comment": comment.likes_count,
                        "comment_time": comment.created_at_utc.strftime('%Y-%m-%d %H:%M:%S'),
                        "caption": caption,
                        "post_url": post_url,
                        "total_post_likes": post.likes,
                        "total_post_comments": post.comments
                    })
                    comment_count += 1
                    if comment_count >= max_comments_per_post:
                        break
            except Exception as e:
                print(f"Error getting comments for {post_url}: {e}")
                
            time.sleep(random.uniform(2, 5))
            
    except Exception as e:
        print(f"Critical error on {account}: {e}")

if all_comments_data:
    df = pd.DataFrame(all_comments_data)
    df.to_csv('instagram_comments_dataset_REAL_SAMPLE.csv', index=False)
    print(f"\nSUCCESS! Scraped {len(df)} real comments.")
else:
    print("\nFAILED to scrape any real comments.")
