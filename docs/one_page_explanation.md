Approach
--------
This project uses the open-source Python library `Instaloader` to interact with Instagram. Instaloader provides both a CLI and a Python API capable of downloading stories and associated metadata. The tool supports logging in to an Instagram account (recommended for accessing stories of accounts you follow or private accounts you've access to). The CLI accepts a username or a path to a file with multiple usernames.


Dependencies
------------
- Python 3.9+
- instaloader
- Flask (optional, for web UI)
- requests, tqdm


Limitations & Constraints
-------------------------
- Instagram rate limits and anti-bot systems may restrict request frequency. Use responsibly.
- Private account stories require an Instagram account which follows them and login credentials; the tool stores session cookies (not your password) when using `--login` via Instaloader.
- This tool does not bypass paywalls, paid APIs, or circumvent Instagram security. Use only for lawful, authorized access.


How to run
----------
1. Install: `pip install -r requirements.txt`
2. CLI examples:
- Single username: `python cli.py --user nasa`
- Multiple usernames: `python cli.py --file examples/usernames.txt`
- Login (to access private/followed-only stories): `python cli.py --login your_insta_username --file examples/usernames.txt`
3. Web UI:
- `python web_app/app.py` then visit `http://127.0.0.1:5000`.


Output
------
- Files saved under `downloads/{username}/` with filenames including username, ISO timestamp and extension.