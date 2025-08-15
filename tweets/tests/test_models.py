from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tweets.models import Tweet


class TweetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_tweet_creation_with_text_only(self):
        """Test creating a tweet with text only."""
        tweet = Tweet.objects.create(
            text="This is a test tweet",
            author=self.user
        )
        self.assertEqual(tweet.text, "This is a test tweet")
        self.assertEqual(tweet.author, self.user)
        self.assertIsNotNone(tweet.created_at)
        self.assertIsNone(tweet.image.name if not tweet.image else None)

    def test_tweet_creation_with_max_length_text(self):
        """Test creating a tweet with maximum allowed length."""
        max_text = "x" * 280
        tweet = Tweet.objects.create(
            text=max_text,
            author=self.user
        )
        self.assertEqual(len(tweet.text), 280)
        self.assertEqual(tweet.text, max_text)

    def test_tweet_text_max_length_validation(self):
        """Test that text field respects max_length constraint."""
        # Create a text longer than 280 characters
        long_text = "x" * 281
        tweet = Tweet(text=long_text, author=self.user)
        
        # This should raise a validation error when full_clean is called
        with self.assertRaises(ValidationError):
            tweet.full_clean()

    def test_tweet_string_representation(self):
        """Test the string representation of a tweet."""
        tweet = Tweet.objects.create(
            text="Test tweet for string representation",
            author=self.user
        )
        expected_str = f"{self.user.username}: Test tweet for string representation..."
        self.assertEqual(str(tweet), expected_str)

    def test_tweet_ordering(self):
        """Test that tweets are ordered by created_at descending."""
        tweet1 = Tweet.objects.create(text="First tweet", author=self.user)
        tweet2 = Tweet.objects.create(text="Second tweet", author=self.user)
        
        tweets = Tweet.objects.all()
        self.assertEqual(tweets.first(), tweet2)  # Most recent first
        self.assertEqual(tweets.last(), tweet1)

    def test_tweet_without_author(self):
        """Test creating a tweet without an author."""
        tweet = Tweet.objects.create(text="Anonymous tweet")
        self.assertIsNone(tweet.author)
        self.assertTrue("Anonymous" in str(tweet)) 