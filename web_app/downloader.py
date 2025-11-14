import os
import time
import requests
from datetime import datetime
from tqdm import tqdm
from instagrapi import Client
from utils import make_output_path, make_filename, LOG


# -----------------------------
# FIXED: Manual CDN downloader
# -----------------------------
def download_file(url, outfile):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.instagram.com/",
    }
    r = requests.get(url, headers=headers, stream=True)

    if r.status_code != 200:
        raise Exception(f"CDN download failed ({r.status_code}) URL: {url}")

    with open(outfile, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


# -----------------------------
# Story Downloader Class
# -----------------------------
class StoryDownloader:

    def __init__(self, sleep_between=1.0):
        self.sleep_between = sleep_between
        self.cl = Client()

        # Load saved session.json
        if os.path.exists("session.json"):
            LOG.info("Loading Instagrapi session.json")
            try:
                self.cl.load_settings("session.json")
                self.cl.get_timeline_feed()
                LOG.info("Session valid.")
            except Exception as e:
                LOG.warning(f"Session invalid: {e}")
        else:
            LOG.warning("session.json not found. Please login first.")

    # -------------------------------------------------
    # Download STORIES for a single username
    # -------------------------------------------------
    def download_stories_for(self, username):
        saved = []

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "downloads"))
        outdir = make_output_path(base=base_dir, username=username)

        LOG.info(f"Fetching stories for: {username}")

        # Get user ID
        try:
            user_id = self.cl.user_id_from_username(username)
        except Exception as e:
            LOG.error(f"Cannot get user ID for {username}: {e}")
            return saved

        # Fetch story items
        try:
            stories = self.cl.user_stories(user_id)
        except Exception as e:
            LOG.error(f"Failed to fetch stories for {username}: {e}")
            return saved

        if not stories:
            LOG.info(f"No active stories found for {username}.")
            return saved

        # Download each story
        for story in stories:
            try:
                taken_at = story.taken_at or datetime.utcnow()
                is_video = bool(story.video_url)
                ext = "mp4" if is_video else "jpg"

                # Build filename
                filename = make_filename(
                    username, taken_at, ext, shortcode=str(story.pk)
                )
                outfile = os.path.join(outdir, filename)

                # ----- FIXED: Manual CDN download -----
                media_url = story.video_url if is_video else story.thumbnail_url
                download_file(media_url, outfile)

                saved.append({
                    "username": username,
                    "timestamp": taken_at.isoformat() + "Z",
                    "file": outfile,
                    "type": ext
                })

                LOG.info(f"Saved story: {outfile}")
                time.sleep(self.sleep_between)

            except Exception as e:
                LOG.error(f"Error saving story: {e}")

        return saved

    # -------------------------------------------------
    # Download stories for multiple usernames
    # -------------------------------------------------
    def download_from_list(self, usernames):
        results = {}
        for user in tqdm(usernames, desc="users"):
            results[user] = self.download_stories_for(user)
        return results
