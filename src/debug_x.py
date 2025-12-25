
import os
import tweepy
import logging
import sys
from datetime import datetime

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_x_post():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Check for missing keys
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        logger.error("❌ MISSING API KEYS! Check your GitHub Secrets.")
        return

    # Authenticate
    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        logger.info("✅ Authentication Object Created.")
    except Exception as e:
        logger.error(f"❌ Authentication Failed: {e}")
        return

    # Try to post
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"Hello World! Debugging Deployment at {timestamp} 🚀"
        logger.info(f"Attempting to post: '{text}'")
        
        response = client.create_tweet(text=text)
        
        logger.info(f"✅ SUCCESS! Tweet posted.")
        logger.info(f"Tweet ID: {response.data['id']}")
        logger.info(f"URL: https://x.com/i/web/status/{response.data['id']}")
        
    except tweepy.Errors.Forbidden as e:
        logger.error("❌ 403 FORBIDDEN ERROR")
        logger.error("This means your Access Tokens are READ-ONLY.")
        logger.error("FIX: Go to X Developer Portal -> User Auth Settings -> Select 'Read and Write' -> Save.")
        logger.error("THEN: Go to Keys and Tokens -> REGENERATE Access Token & Secret -> Update GitHub Secrets.")
        logger.error(f"Full Error: {e}")
    except Exception as e:
        logger.error(f"❌ UNKNOWN ERROR: {e}")

if __name__ == "__main__":
    debug_x_post()
