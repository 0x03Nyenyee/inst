import os
import requests
from bs4 import BeautifulSoup
from uuid import uuid4

DOWNLOAD_FOLDER = "downloads"

def download_instagram_media(instagram_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"[🔍] Mengambil data dari: {instagram_url}")
    response = requests.get(instagram_url, headers=headers)

    if response.status_code != 200:
        print("[❌] Gagal mengakses URL.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    meta_tag = soup.find("meta", property="og:video") or soup.find("meta", property="og:image")

    if not meta_tag:
        print("[❌] Tidak menemukan media di halaman tersebut.")
        return

    media_url = meta_tag["content"]
    file_ext = ".mp4" if "video" in media_url else ".jpg"
    filename = f"{uuid4()}{file_ext}"

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    print(f"[⬇️] Mengunduh media dari: {media_url}")
    with requests.get(media_url, stream=True) as r:
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"[✅] Sukses! File disimpan di: {file_path}")

if __name__ == "__main__":
    instagram_url = input("Masukkan URL Instagram: ").strip()
    download_instagram_media(instagram_url)
