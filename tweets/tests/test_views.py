from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tweets.models import Tweet
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class TweetViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_tweet_list_view_get(self):
        """Test GET request to tweet list view returns 200 and shows tweets."""
        # Create a test tweet
        tweet = Tweet.objects.create(
            text="Test tweet for list view",
            author=self.user
        )
        
        response = self.client.get(reverse('tweet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test tweet for list view")
        self.assertContains(response, tweet.author.username)

    def test_tweet_list_view_empty(self):
        """Test tweet list view when no tweets exist."""
        response = self.client.get(reverse('tweet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tweets yet!")

    def test_tweet_create_view_get(self):
        """Test GET request to tweet create view."""
        response = self.client.get(reverse('tweet_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post a Tweet")
        self.assertContains(response, 'name="text"')

    def test_tweet_create_view_post_valid(self):
        """Test POST request to create view with valid data creates tweet and redirects."""
        tweet_data = {
            'text': 'This is a new tweet via POST'
        }
        
        response = self.client.post(reverse('tweet_create'), tweet_data, follow=True)
        
        # Should redirect to tweet list
        self.assertEqual(response.status_code, 200)
        
        # Tweet should be created
        self.assertTrue(Tweet.objects.filter(text='This is a new tweet via POST').exists())
        
        # Should show success message
        self.assertContains(response, "Tweet posted successfully!")

    def test_tweet_create_view_post_with_image(self):
        """Test creating a tweet with an image."""
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        
        uploaded_image = SimpleUploadedFile(
            "test_image.jpg",
            image_file.getvalue(),
            content_type="image/jpeg"
        )
        
        tweet_data = {
            'text': 'Tweet with image',
            'image': uploaded_image
        }
        
        response = self.client.post(reverse('tweet_create'), tweet_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        tweet = Tweet.objects.get(text='Tweet with image')
        self.assertTrue(tweet.image)

    def test_tweet_create_view_post_invalid(self):
        """Test POST request with invalid data (empty text)."""
        tweet_data = {
            'text': ''  # Empty text should be invalid
        }
        
        response = self.client.post(reverse('tweet_create'), tweet_data)
        
        # Should not redirect (stays on form page)
        self.assertEqual(response.status_code, 200)
        
        # Should not create a tweet
        self.assertEqual(Tweet.objects.count(), 0)

    def test_demo_user_creation(self):
        """Test that demo user is created when posting a tweet."""
        tweet_data = {
            'text': 'Test tweet for demo user creation'
        }
        
        # Ensure demo user doesn't exist yet
        self.assertFalse(User.objects.filter(username='demo').exists())
        
        response = self.client.post(reverse('tweet_create'), tweet_data, follow=True)
        
        # Demo user should now exist
        self.assertTrue(User.objects.filter(username='demo').exists())
        
        # Tweet should be attributed to demo user
        tweet = Tweet.objects.get(text='Test tweet for demo user creation')
        self.assertEqual(tweet.author.username, 'demo')

    def test_url_patterns(self):
        """Test that URL patterns work correctly."""
        # Test tweet list URL
        list_url = reverse('tweet_list')
        self.assertEqual(list_url, '/')
        
        # Test tweet create URL
        create_url = reverse('tweet_create')
        self.assertEqual(create_url, '/create/') 