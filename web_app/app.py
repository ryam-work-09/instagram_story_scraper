import os
import threading
from flask import Flask, render_template, request, redirect, url_for, flash
from downloader import StoryDownloader
from utils import init_logging

app = Flask(__name__)
app.secret_key = "dev"

init_logging()

SD = StoryDownloader()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        usernames_text = request.form.get("usernames", "")
        usernames = [u.strip() for u in usernames_text.split("\n") if u.strip()]

        if not usernames:
            flash("Enter at least one username.", "warning")
            return redirect(url_for("index"))

        def task():
            SD.download_from_list(usernames)

        threading.Thread(target=task).start()
        flash("Download started. Check downloads folder.", "success")
        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
