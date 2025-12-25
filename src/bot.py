
import argparse
import logging
import sys
from dotenv import load_dotenv
from content_manager import ContentManager
from reply_engine import ReplyEngine
from x_client import XClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="X Vocabulary Bot")
    parser.add_argument("--mode", choices=["post", "reply"], required=True, help="Mode of operation: 'post' for scheduled words, 'reply' for contextual replies")
    parser.add_argument("--text", help="Text to analyze for reply mode (simulating a tweet)")
    parser.add_argument("--dry-run", action="store_true", help="Run without actually posting to X")
    
    args = parser.parse_args()

    # Load env vars
    load_dotenv()

    # Initialize components
    cm = ContentManager()
    reply_engine = ReplyEngine()
    client = XClient()

    if args.mode == "post":
        logger.info("Starting Curated Word Post job...")
        word_data = cm.get_next_word()
        
        if not word_data:
            logger.error("Failed to generate word data. Check Groq API key and logs.")
            # Exit with code 1 so GitHub Actions shows a Failure Red X
            sys.exit(1)

        post_content = cm.generate_post_text(word_data)
        
        if args.dry_run:
            logger.info(f"[DRY RUN] Content to post:\n{post_content}")
            # In dry run we don't mark as used to preserve data for real run
        else:
            success = client.post_tweet(post_content)
            if success:
                cm.mark_as_used(word_data['word'])
                logger.info(f"Posted and marked '{word_data['word']}' as used.")
            else:
                logger.error("Failed to post tweet.")

    elif args.mode == "reply":
        logger.info("Starting Contextual Reply job...")
        if not args.text:
            logger.error("Reply mode requires --text argument to analyze.")
            sys.exit(1)

        analysis = reply_engine.analyze_text(args.text)
        if analysis:
            found_word, suggestion = analysis
            reply_content = reply_engine.generate_reply(found_word, suggestion)
            
            if args.dry_run:
                logger.info(f"[DRY RUN] Would reply: '{reply_content}'")
            else:
                # In a real scenario, we would need the tweet ID to reply to.
                # Since this is a restricted implementation (Write-only), we assume this might be triggered manually 
                # or via a future distinct hook that provides tweet_id.
                # For now, we just post it as a standalone tweet or log it.
                logger.info(f"Generated reply: {reply_content}")
                # client.post_tweet(reply_content) # Uncomment if we had a target ID
        else:
            logger.info("No trigger words found in the text.")

if __name__ == "__main__":
    main()
