from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from moviepy.editor import *
import proglog
import os
import re


# YOU MUST GO INTO cipher.py of Pytube and change line 411 to 'transform_plan_raw = js'


def download_video(link):
        try:
                video = YouTube(link, use_oauth=True, allow_oauth_cache=True)

        except VideoUnavailable:
                print(f"Video at link:{link} is unavailable!")

        else:
                stream = video.streams.get_highest_resolution()
                stream.download('./Outputs')
                print(f"{video.title} downloaded successfully!")
                video_path = f"./Outputs/{stream.default_filename}"

        return video_path, video.title


def download_playlist(link):
        playlist = Playlist(link)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        for url in playlist.video_urls:
                print(f"Downloading {url}")
                video = download_video(url)
                convert_to_mp3(video[0], video[1])
        print("All Playlist Videos Downloaded.")


def convert_to_mp3(mp4_path, mp3_filename):
        file_to_convert = AudioFileClip(mp4_path)

        print("Converting to mp3...")
        file_to_convert.write_audiofile(f'./Outputs/{mp3_filename}.mp3',
                                        verbose=False, logger=proglog.TqdmProgressBarLogger(print_messages=False))

        file_to_convert.close()
        print("File conversion complete!")

        if os.path.exists(mp4_path):
                os.remove(mp4_path)


download_playlist("https://www.youtube.com/playlist?list=PL71YAA_RLb2rxIkt0DVQqGbBVidW5hXJr")