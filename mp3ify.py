from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from moviepy.editor import *
import proglog
import os
import re
import sys


# YOU MUST GO INTO cipher.py of Pytube and change line 411 to 'transform_plan_raw = js'


def download_video(link: str) -> tuple:
        """
        Downloads video from YouTube as a mp4 file and returns video path and title.
        """
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


def download_playlist(link: str):
        """
        Downloads playlist from YouTube and saves each song as a mp4 file in outputs folder.
        """
        playlist = Playlist(link)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        for url in playlist.video_urls:
                print(f"Downloading {url}")
                video = download_video(url)
                convert_to_mp3(video[0], video[1])
        print("All Playlist Videos Downloaded.")


def convert_to_mp3(mp4_path: str, mp3_filename: str):
        """
        Converts downloaded mp4 file to a mp3 file.
        """
        file_to_convert = AudioFileClip(mp4_path)

        print("Converting to mp3...")

        fixed_filename = ''.join(letter for letter in mp3_filename if letter.isalnum())

        file_to_convert.write_audiofile(f'./Outputs/{str(fixed_filename)}.mp3',
                                        verbose=False, logger=proglog.TqdmProgressBarLogger(print_messages=False))

        file_to_convert.close()
        print("File conversion complete! Check outputs folder.")

        if os.path.exists(mp4_path):
                os.remove(mp4_path)


def main():
        """
        First thing to run.
        Holds logic for video/playlist downloading and their exceptions.
        """
        try:
                link_type = sys.argv[1]

                link = sys.argv[2]

                if link_type == 'p':
                        download_playlist(link)
                elif link_type == 'v':
                        video = download_video(link)
                        convert_to_mp3(video[0], video[1])
                else:
                        print("Link type not found!")
                        sys.exit(2)

        except IndexError:

                print("No command line args found.")

                link_type = input("'p' for playlist, 'v' for video: ")

                link = input("youtube link?: ")

                try:
                        if link_type == 'p':
                                print("Downloading Playlist...")
                                download_playlist(link)
                        elif link_type == 'v':
                                print("Downloading Video...")
                                video = download_video(link)
                                convert_to_mp3(video[0], video[1])
                        else:
                                print("Link type not found!")
                                sys.exit(2)

                except KeyError:
                        print("Link is not a playlist!")
                        sys.exit(2)


if __name__ == "__main__":
        main()