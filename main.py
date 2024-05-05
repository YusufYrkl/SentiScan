import pandas as pd
import sqlite3
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Increase display settings for console
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.max_rows', 20)

# Connect and prepare database
conn = sqlite3.connect('tweets_analysis.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS tweet_analysis (
    id INTEGER PRIMARY KEY,
    tweet TEXT,
    sentiment TEXT,
    confidence REAL
)
''')
conn.commit()

# Load tweets dataset
df = pd.read_csv('Tweets.csv', header=None, encoding='ISO-8859-1')
tweets = df[5].head(50).tolist() #


# Preprocess and analyze tweets
def preprocess_tweet(tweet):
    tweet_words = []
    for word in tweet.split():
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    return " ".join(tweet_words)


roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']
results = []

for tweet in tweets:
    tweet_proc = preprocess_tweet(tweet)
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    sentiment = labels[scores.argmax()]
    confidence = round(scores.max() * 100, 2)  # Convert to percentage
    results.append((tweet, sentiment, confidence))
    c.execute('INSERT INTO tweet_analysis (tweet, sentiment, confidence) VALUES (?, ?, ?)',
              (tweet, sentiment, confidence))

conn.commit()
conn.close()

results_df = pd.DataFrame(results, columns=['Tweet', 'Sentiment', 'Confidence'])
print(results_df)
