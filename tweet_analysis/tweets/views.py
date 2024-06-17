from django.shortcuts import render
from .models import TweetAnalysis

def tweet_list(request):
    tweets = TweetAnalysis.objects.all()
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})
