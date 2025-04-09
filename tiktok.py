import yt_dlp
import os
import google.genai
import time
from urllib.parse import urlparse


def validate_tiktok_url(url: str) -> str:
    if not url:
        raise ValueError("URL cannot be None or empty")

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL format")

    if "tiktok.com" not in parsed_url.netloc:
        raise ValueError("URL must be from tiktok.com domain")

    return url


def generate_video_id(url: str) -> str:
    if not url:
        raise ValueError("URL cannot be None or empty")
    return url.split("/")[-1]


def download_tiktok_video(url: str) -> str:
    validated_url = validate_tiktok_url(url)
    video_id = generate_video_id(validated_url)
    ydl_opts = {
        "format": "best",
        "outtmpl": f"{video_id}.mp4",
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([validated_url])
        return f"{video_id}.mp4"
    except Exception as e:
        raise e


# TODO: change this polling functionality to be event based
def upload_video_for_analysis(video_file_name: str, client: google.genai.Client):
    video_file = client.files.upload(file=video_file_name)

    while video_file.state == "PROCESSING":
        print("Waiting for video to be processed.")
        time.sleep(1)
        video_file = client.files.get(name=video_file.name)

    if video_file.state == "FAILED":
        raise ValueError(video_file.state)
    print(f"Video processing complete: " + video_file.uri)

    return video_file


def get_video_analysis(
    video_url: str, client: google.genai.Client, model_name: str, prompt: str
):
    file_name = download_tiktok_video(video_url)
    video_file = upload_video_for_analysis(file_name, client)
    response = client.models.generate_content(
        model=model_name,
        contents=[
            video_file,
            prompt,
        ],
    )
    return response.text
