import os
import yt_dlp
import google


client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
import time


# def download_tiktok_video(url):
#     ydl_opts = {
#         "format": "best",
#         "outtmpl": "video.mp4",
#         "quiet": False,
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#             print("Video downloaded successfully!")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")


# if __name__ == "__main__":
#     # Example TikTok video URL
#     tiktok_url = "https://www.tiktok.com/@wearebeanz/video/7418668741380115758"
#     download_tiktok_video(tiktok_url)


def upload_video(video_file_name):
    video_file = client.files.upload(file=video_file_name)

    while video_file.state == "PROCESSING":
        print("Waiting for video to be processed.")
        time.sleep(10)
        video_file = client.files.get(name=video_file.name)

    if video_file.state == "FAILED":
        raise ValueError(video_file.state)
    print(f"Video processing complete: " + video_file.uri)

    return video_file


if __name__ == "__main__":
    # check if video exists
    if os.path.exists("video.mp4"):
        pottery_video = upload_video("video.mp4")
    else:
        print("Video does not exist")
