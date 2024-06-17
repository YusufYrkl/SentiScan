import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Twitter API Bearer Token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJKbtgEAAAAA%2Filk9FSWW%2BtZdkXw5cUgP%2BMupeo%3D9p3dqIK7S65lfAZVhfWEulzX3PRN9KPNJ6X9ZuIzN2Xy3QxXa7'

def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

def get_tweet(tweet_id):
    headers = create_headers(bearer_token)
    tweet_fields = "tweet.fields=text,author_id,created_at,lang"
    url = f"https://api.twitter.com/2/tweets/{tweet_id}?{tweet_fields}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    return response.json()

tweet_id = '1787166855108419947'
tweet_data = get_tweet(tweet_id)
tweet = tweet_data['data']['text']

# Load pre-trained model and tokenizer from Hugging Face's Transformers
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# Encode and analyze the tweet
encoded_tweet = tokenizer(tweet, return_tensors='pt')
output = model(**encoded_tweet)

# Convert model output to probabilities using softmax
scores = softmax(output.logits.detach().numpy()[0])
labels = ['Negative', 'Neutral', 'Positive']
sentiment = labels[scores.argmax()]
confidence = scores.max()

# Print the results
print(f"Tweet: {tweet}")
print(f"Sentiment: {sentiment}, Confidence: {confidence:.2f}")
