import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Increase display settings for console
pd.set_option('display.max_colwidth', 50)  # Show full content of each column
pd.set_option('display.max_rows', 20)  # Show more rows

# Load tweets dataset
df = pd.read_csv('Tweets.csv', header=None, encoding='ISO-8859-1')

# Extracts head(X) number of tweets and their 6 columns
tweets = df[5].head(10).tolist()

# Preprocess tweets
def preprocess_tweet(tweet):
    tweet_words = []
    for word in tweet.split():
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    return " ".join(tweet_words)

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# Analyze sentiments
results = []
for tweet in tweets:
    tweet_proc = preprocess_tweet(tweet)
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    sentiment = labels[scores.argmax()]
    results.append((tweet, sentiment, scores.max()))

# Convert results to DataFrame for better visualization
results_df = pd.DataFrame(results, columns=['Tweet', 'Sentiment', 'Confidence'])
print(results_df)
