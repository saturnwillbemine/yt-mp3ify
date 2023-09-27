from pytube import YouTube

video_path = './mp3ify'


def download_video(link):
    try:
        video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        stream = video.streams.get_highest_resolution()
        stream.download()

        print(video.title)
        print(f"Your video will be found at {video_path}")
    except Exception as e:
        print(f"Error at {str(e)}")


download_video("https://www.youtube.com/watch?v=-zvWBnQ0E2k")
