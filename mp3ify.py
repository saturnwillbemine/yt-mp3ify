from pytube import YouTube, Playlist
from pytube.exceptions import *
from moviepy.editor import *
import proglog, os, re, sys, time

# YOU MUST GO INTO cipher.py of Pytube and change line 411 to 'transform_plan_raw = js'

# YOU MUST ALSO change lines 272 and 273 in cipher.py of Pytube to:
#  r'a.[a-zA-Z]\s*&&\s*([a-z]\s*=\sa.get("n"))\s&&.?||\s([a-z]+)',
#  r'([a-z]\s*=\s*([a-zA-Z0-9$]+)([\d+])?([a-z])', ]


def download_video(link: str) -> tuple:
        """
        Downloads video from YouTube as a mp4 file and returns video path and title.
        """
        try:
                video = YouTube(link, use_oauth=True, allow_oauth_cache=True)

        except (VideoUnavailable, RegexMatchError, UnboundLocalError):
                print(f"Video is unavailable/Incorrect link type!")

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
        video_num = 1
        try:
                playlist = Playlist(link)
                playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        except KeyError:
                print(f"Playlist is unavailable/Incorrect link type!")
        for url in playlist.video_urls:
                print(f"Downloading {video_num}/{len(playlist.video_urls)}")
                try:
                        video = download_video(url)
                except AgeRestrictedError:
                        print("Age restricted video.. skipping. Download it using 'v'")
                        video_num += 1
                        time.sleep(2)
                        continue
                convert_to_mp3(video[0], video[1])
                video_num += 1
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

                try:
                        if link_type == 'p':
                                print("Downloading Playlist...")
                                download_playlist(link)
                        elif link_type == 'v':
                                print("Downloading Video...")
                                try:
                                        video = download_video(link)
                                except (VideoUnavailable, RegexMatchError, UnboundLocalError):
                                        main()
                                convert_to_mp3(video[0], video[1])
                        else:
                                print("Link type not found!")
                                main()

                except KeyError:
                        print("Link is not a playlist!")
                        main()

        except IndexError:

                link_type = input("'p' for playlist, 'v' for video: ")

                link = input("youtube link?: ")

                try:
                        if link_type == 'p':
                                print("Downloading Playlist...")
                                download_playlist(link)
                        elif link_type == 'v':
                                print("Downloading Video...")
                                try:
                                        video = download_video(link)
                                except (VideoUnavailable, RegexMatchError, UnboundLocalError):
                                        main()
                                convert_to_mp3(video[0], video[1])
                        else:
                                print("Link type not found!")
                                main()

                except KeyError:
                        print("Link is not a playlist!")
                        main()

                main()


if __name__ == "__main__":
        main()
