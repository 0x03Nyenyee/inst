from flask import Flask, render_template, request, send_from_directory
from app.downloader import download_media
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    download_url = None
    if request.method == "POST":
        url = request.form["url"]
        download_url = download_media(url)
    return render_template("index.html", download_url=download_url)

@app.route("/downloads/<filename>")
def downloaded_file(filename):
    return send_from_directory("static/downloads", filename)

if __name__ == "__main__":
    app.run(debug=True)
