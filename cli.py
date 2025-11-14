#!/usr/bin/env python3
import argparse
from utils import init_logging, LOG
from downloader import StoryDownloader


def parse_args():
    parser = argparse.ArgumentParser(
        description="Instagram Story Scraper — CLI Tool"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--user", "-u", help="Single username to scrape")
    group.add_argument("--file", "-f", help="File containing usernames list")

    parser.add_argument("--login", "-l", help="Instagram login username")
    parser.add_argument("--sleep", type=float, default=1.0,
                        help="Delay between downloads")

    return parser.parse_args()


def main():
    args = parse_args()
    init_logging()

    scraper = StoryDownloader(
        session_username=args.login,
        sleep_between=args.sleep
    )

    # Optional login for private accounts
    if args.login:
        scraper.login(args.login)

    # Single or multiple users
    if args.user:
        users = [args.user]
    else:
        with open(args.file, "r") as f:
            users = [line.strip() for line in f if line.strip()]

    LOG.info("Starting download for %d user(s)", len(users))
    results = scraper.download_from_list(users)
    LOG.info("Done. Story counts: %s", {k: len(v) for k, v in results.items()})


if __name__ == "__main__":
    main()
