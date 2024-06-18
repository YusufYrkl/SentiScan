from django.shortcuts import render
from .models import TweetAnalysis

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

    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})
