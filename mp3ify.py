from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from moviepy.editor import *
import proglog
import os


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
                video_path = f"./Downloads/{stream.default_filename}"

        print(f"Your video will be found at {video_path}")
        return video_path, video.title


def convert_to_mp3(mp4_path, mp3_filename):
        file_to_convert = AudioFileClip(mp4_path)

        print("Converting to mp3...")
        file_to_convert.write_audiofile(f'./mp3outputs/{mp3_filename}.mp3',
                                        verbose=False, logger=proglog.TqdmProgressBarLogger(print_messages=False))

        file_to_convert.close()
        print("File conversion complete!")

        if os.path.exists(mp4_path):
                os.remove(mp4_path)
                print("Path cleanup complete")


video = download_video('https://www.youtube.com/watch?v=AuaXmo12hAc')
convert_to_mp3(video[0], video[1])
