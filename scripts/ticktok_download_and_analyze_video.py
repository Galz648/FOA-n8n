import os
import yt_dlp
import google.genai
import time




# better to use gemini-2.5-pro-exp-03-25 but it is not allways working
model_name = "gemini-2.0-flash" #["gemini-1.5-flash-latest","gemini-2.0-flash-lite","gemini-2.0-flash","gemini-2.5-pro-exp-03-25"] {"allow-input":true, isTemplate: true}
client = google.genai.Client(api_key="AIzaSyDa0oufrgbKRHD6dU4dzSuZOgbUaVOdS4U")


def download_tiktok_video(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "video.mp4",
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("Video downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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
    # Example TikTok video URL
    tiktok_url = "https://www.tiktok.com/@wearebeanz/video/7418668741380115758"
    download_tiktok_video(tiktok_url)

    video = upload_video("video.mp4")
    prompt = "sumeries this video and tell if it is antisemitic or not"  
            
    response = client.models.generate_content(
        model=model_name,
        contents=[
            video,
            prompt,
        ]
    )

    print(response.text)

    
