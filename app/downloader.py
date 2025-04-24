import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from uuid import uuid4

def download_media(instagram_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(instagram_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    meta_tag = soup.find("meta", property="og:video") or soup.find("meta", property="og:image")
    if not meta_tag:
        return None

    media_url = meta_tag["content"]
    file_ext = ".mp4" if "video" in media_url else ".jpg"
    filename = f"{uuid4()}{file_ext}"
    file_path = os.path.join("static/downloads", filename)

    with requests.get(media_url, stream=True) as r:
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return f"/downloads/{filename}"
