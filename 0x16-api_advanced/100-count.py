#!/usr/bin/python3
""" raddit api"""
import praw
import re

def count_words(subreddit, word_list, results={}):
    reddit = praw.Reddit(user_agent='myBot/0.0.1')
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        for submission in subreddit_obj.hot(limit=10):  # Limit to 10 to avoid hitting Reddit API rate limits
            title = submission.title.lower()
            for word in word_list:
                word = word.lower()
                if re.search(rf"\b{word}\b", title):  # Use regex to match whole words only
                    if word in results:
                        results[word] += 1
                    else:
                        results[word] = 1
        if not results:
            return  # No matching keywords found, exit
        sorted_results = sorted(results.items(), key=lambda x: (-x[1], x[0]))  # Sort by count descending, then word ascending
        for word, count in sorted_results:
            print(f"{word}: {count}")
    except praw.exceptions.NotFound:
        return  # Invalid subreddit, exit

