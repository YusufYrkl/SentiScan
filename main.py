import pandas as pd
import sqlite3
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Set display options for better console readability
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.max_rows', 20)

# Connect to the SQLite database
conn = sqlite3.connect('tweets_analysis.db')
c = conn.cursor()

# Create a table with a unique constraint on the 'tweet' column
c.execute('''
CREATE TABLE IF NOT EXISTS tweet_analysis (
    id INTEGER PRIMARY KEY,
    tweet TEXT UNIQUE,
    sentiment TEXT,
    confidence REAL
)
''')
conn.commit()

# Load tweets dataset
df = pd.read_csv('Tweets.csv', header=None, encoding='ISO-8859-1')
tweets = df[5].head(100).tolist()  # Process only the first 50 tweets for this example

# Function to preprocess tweets
def preprocess_tweet(tweet):
    tweet_words = []
    for word in tweet.split():
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    return " ".join(tweet_words)

# Load the pre-trained model and tokenizer from Hugging Face's Transformers
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

# Labels for sentiment classification
labels = ['Negative', 'Neutral', 'Positive']
results = []

# Process each tweet
for tweet in tweets:
    tweet_proc = preprocess_tweet(tweet)
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    sentiment = labels[scores.argmax()]
    confidence = round(scores.max() * 100, 2)  # Convert to percentage

    # Try to insert each tweet into the database, skip duplicates
    try:
        c.execute('INSERT INTO tweet_analysis (tweet, sentiment, confidence) VALUES (?, ?, ?)',
                  (tweet, sentiment, confidence))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Duplicate tweet was not added.")

# Close the database connection
conn.close()

# Convert the results to a DataFrame and print
results_df = pd.DataFrame(results, columns=['Tweet', 'Sentiment', 'Confidence'])
print(results_df)