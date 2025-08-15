from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Tweet
from .forms import TweetForm


def tweet_list(request):
    """Display all tweets in chronological order."""
    tweets = Tweet.objects.all()
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})


def tweet_create(request):
    """Create a new tweet."""
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            # Use demo user as default author
            demo_user, created = User.objects.get_or_create(
                username='demo',
                defaults={'password': 'demo12345', 'is_active': True}
            )
            tweet.author = demo_user
            tweet.save()
            messages.success(request, 'Tweet posted successfully!')
            return redirect('tweet_list')
    else:
        form = TweetForm()
    
    return render(request, 'tweets/tweet_form.html', {'form': form}) 