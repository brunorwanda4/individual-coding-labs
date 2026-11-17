import csv
import sys
import os


def load_raw_data(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    raw_tweets = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                raw_tweets.append(row)
    except Exception as error:
        print(f"Error reading '{filename}': {error}")
        sys.exit(1)
    return raw_tweets


def get_field(tweet, names):
    for name in names:
        if name in tweet:
            return tweet[name]
    lower_names = {str(key).lower(): key for key in tweet}
    for name in names:
        key = lower_names.get(name.lower())
        if key is not None:
            return tweet[key]
    return ""


def set_field(tweet, names, value):
    for name in names:
        if name in tweet:
            tweet[name] = value
            return


def clean_data(tweets):
    clean_tweets = []
    bad_rows = 0
    fixed_rows = 0

    for tweet in tweets:
        text = get_field(tweet, ("Text", "text"))
        if text is None or str(text).strip() == "":
            bad_rows += 1
            continue

        likes = get_field(tweet, ("Likes", "likes"))
        retweets = get_field(tweet, ("Retweets", "retweets"))

        if likes is None or str(likes).strip() == "":
            set_field(tweet, ("Likes", "likes"), "0")
            fixed_rows += 1
        if retweets is None or str(retweets).strip() == "":
            set_field(tweet, ("Retweets", "retweets"), "0")
            fixed_rows += 1

        clean_tweets.append(tweet)

    print(f"Data audit: removed {bad_rows} row(s) with missing text.")
    print(f"Data audit: fixed {fixed_rows} blank Likes/Retweets field(s).")
    return clean_tweets


def tweet_likes(tweet):
    value = get_field(tweet, ("Likes", "likes"))
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def find_viral_tweet(tweets):
    if not tweets:
        print("No valid tweets to analyze.")
        return None

    viral = tweets[0]
    highest_likes = tweet_likes(viral)
    for tweet in tweets[1:]:
        likes = tweet_likes(tweet)
        if likes > highest_likes:
            highest_likes = likes
            viral = tweet

    username = get_field(viral, ("Username", "username"))
    text = get_field(viral, ("Text", "text"))
    print("Viral tweet:")
    print(f"Username: {username}")
    print(f"Likes: {highest_likes}")
    print(f"Text: {text}")
    return viral


def custom_sort_by_likes(tweets):
    sorted_tweets = list(tweets)
    for i in range(len(sorted_tweets)):
        highest_index = i
        for j in range(i + 1, len(sorted_tweets)):
            if tweet_likes(sorted_tweets[j]) > tweet_likes(sorted_tweets[highest_index]):
                highest_index = j
        if highest_index != i:
            temporary = sorted_tweets[i]
            sorted_tweets[i] = sorted_tweets[highest_index]
            sorted_tweets[highest_index] = temporary
    return sorted_tweets


def search_tweets(tweets, keyword):
    matches = []
    keyword = keyword.lower()
    for tweet in tweets:
        text = str(get_field(tweet, ("Text", "text"))).lower()
        if keyword in text:
            matches.append(tweet)
    return matches


if __name__ == "__main__":
    dataset = load_raw_data("twitter_dataset.csv")
    clean_dataset = clean_data(dataset)

    viral_tweet = find_viral_tweet(clean_dataset)

    sorted_tweets = custom_sort_by_likes(clean_dataset)
    print("\nTop 10 most liked tweets:")
    for index, tweet in enumerate(sorted_tweets[:10], start=1):
        print(
            f"{index}. "
            f"{get_field(tweet, ('Username', 'username'))} "
            f"({tweet_likes(tweet)} Likes): "
            f"{get_field(tweet, ('Text', 'text'))}"
        )

    keyword = input("\nEnter a search word: ").strip()
    if keyword:
        matches = search_tweets(clean_dataset, keyword)
        print(f"{len(matches)} tweets matched '{keyword}'.")
        for tweet in matches:
            print(
                f"{get_field(tweet, ('Username', 'username'))}: "
                f"{get_field(tweet, ('Text', 'text'))}"
            )
    else:
        print("Search cancelled: no keyword was entered.")
