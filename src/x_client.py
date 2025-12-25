import os
import tweepy
import logging

# Configure logger
logger = logging.getLogger(__name__)

class XClient:
    def __init__(self):
        self.consumer_key = os.getenv("CONSUMER_KEY")
        self.consumer_secret = os.getenv("CONSUMER_SECRET")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        
        self.client = None
        self._authenticate()

    def _authenticate(self):
        """Authenticates with X API v2."""
        if not all([self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret]):
            logger.warning("API keys missing. Client will operate in dry-run mode only.")
            return

        try:
            self.client = tweepy.Client(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            logger.info("Successfully authenticated with X API.")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            self.client = None

    def post_tweet(self, text, reply_to_id=None):
        """Posts a tweet."""
        if not self.client:
            logger.info(f"[DRY RUN] Would post tweet:\n{text}")
            return True

        try:
            response = self.client.create_tweet(text=text, in_reply_to_tweet_id=reply_to_id)
            tweet_id = response.data['id']
            # Construct URL for validation
            # Note: We don't know the username dynamically without an extra API call, 
            # but 'x.com/i/web/status/<id>' works for redirection.
            logger.info(f"Tweet posted successfully! 🚀\nTweet ID: {tweet_id}\nURL: https://x.com/i/web/status/{tweet_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return False
