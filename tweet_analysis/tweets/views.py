from django.shortcuts import render
from .models import TweetAnalysis
from django.db.models import Count

def get_sentiment_data():
    tweets = TweetAnalysis.objects.all()
    sentiment_counts = tweets.values('sentiment').annotate(total=Count('sentiment')).order_by('sentiment')
    sentiment_data = {item['sentiment']: item['total'] for item in sentiment_counts}
    return sentiment_data

def tweet_list(request):
    sentiment = request.GET.get('sentiment')
    min_confidence = request.GET.get('min_confidence')
    keyword = request.GET.get('keyword')

    tweets = TweetAnalysis.objects.all()

    if sentiment:
        tweets = tweets.filter(sentiment=sentiment)

    if min_confidence:
        try:
            min_confidence = float(min_confidence)
            tweets = tweets.filter(confidence__gte=min_confidence)
        except ValueError:
            pass  # Ignore invalid input

    if keyword:
        tweets = tweets.filter(tweet__icontains=keyword)

    sentiment_data = get_sentiment_data()

    return render(request, 'tweets/tweet_list.html', {'tweets': tweets, 'sentiment_data': sentiment_data})

def graphs(request):
    sentiment_data = get_sentiment_data()
    return render(request, 'tweets/graphs.html', {'sentiment_data': sentiment_data})