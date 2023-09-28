from pytube import YouTube
from pytube.exceptions import VideoUnavailable


# YOU MUST GO INTO cipher.py of Pytube and change line 411 to 'transform_plan_raw = js'


def download_video(link):
        try:
                video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        except VideoUnavailable:
                print(f"Video at link:{link} is unavailable!")
        else:
                stream = video.streams.get_highest_resolution()
                stream.download('./Downloads')
                print(f"{video.title} downloaded successfully!")

        print(f"Your video will be found at ../yt-mp3ify/Downloads")


download_video('https://www.youtube.com/watch?v=AuaXmo12hAc')
