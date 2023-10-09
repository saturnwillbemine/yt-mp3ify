from tkinter import *
from moviepy.editor import *
import ttkbootstrap as tb
from pytube import YouTube, Playlist
from pytube.exceptions import *
import re, os, threading


root = tb.Window(themename="darkly")
root.title("YouTube MP3ify")
root.geometry('500x370')


def download_vid_noauth(link: str) -> tuple:
    """
            Downloads video from YouTube, with no oauth cuz gui, as a mp4 file and returns video path and title.
            """
    try:
        video = YouTube(link, use_oauth=False, allow_oauth_cache=False)  # no oauth because login shows up in cmdl

    except (VideoUnavailable, RegexMatchError, UnboundLocalError) as error:
        # RegexMatchError is playlist links in single video downloader
        # UnboundLocalError comes after RegexMatchError
        print(f"Video at link:{link} is unavailable!")
        print(error)
        label2.config(text=f"Incorrect link type!/Video unavailable")


    else:
        stream = video.streams.get_highest_resolution()
        stream.download('./Outputs')
        print(f"{video.title} downloaded successfully!")
        video_path = f"./Outputs/{stream.default_filename}"

    return video_path, video.title


def download_playlist_noauth(link: str):
    """
    Downloads playlist from YouTube and saves each song as a mp4 file in outputs folder.
    """
    playlist = Playlist(link)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    for url in playlist.video_urls:
        print(f"Downloading {url}")
        try:
            video = download_vid_noauth(url)
        except AgeRestrictedError:
            label2.config(text=f"Age restricted video, skipping... use CLI version to login")
            continue
        convert_to_mp3(video[0], video[1])
    print("All Playlist Videos Downloaded.")


def convert_to_mp3(mp4_path: str, mp3_filename: str):
    """
     Converts downloaded mp4 file to a mp3 file.
    """
    file_to_convert = AudioFileClip(mp4_path)

    label2.config(text=f"Converting {mp3_filename} to mp3...")

    fixed_filename = ''.join(letter for letter in mp3_filename if letter.isalnum())

    file_to_convert.write_audiofile(f'./Outputs/{str(fixed_filename)}.mp3',
                                    verbose=False, logger=None)

    file_to_convert.close()
    label2.config(text="File converted! Check outputs folder.")

    if os.path.exists(mp4_path):
        os.remove(mp4_path)


def download_video_thread():
    link = entry.get()
    video = download_vid_noauth(link)
    convert_to_mp3(video[0], video[1])



def download_playlist_thread():
    link = entry.get()
    download_playlist_noauth(link)
    label2.config(text=f"All playlist videos downloaded")



# entry function
# noinspection PyArgumentList
def button_press():
    if chosen_type.get() == "playlist":
        playlist_thread = threading.Thread(target=download_playlist_thread)
        playlist_thread.start()
    elif chosen_type.get() == "video":
        video_thread = threading.Thread(target=download_video_thread)
        video_thread.start()

# noinspection PyArgumentList
# label
label = tb.Label(text="YTMP3ify", font=("Helvetica", 28), bootstyle="default")
label.pack(pady=25)


# entry
entry = tb.Entry(root)
entry.pack(pady=15)

# radio buttons
link_types = ["playlist", "video"]
chosen_type = StringVar()


for link_type in link_types:

    (tb.Radiobutton(root, bootstyle="info, outline, toolbutton", variable=chosen_type, text=link_type, value=link_type)
     .pack(pady=10, padx=20))

label2 = tb.Label(root, text=" ")
label2.pack(pady=10)

# button
download_button = tb.Button(text="Convert", bootstyle="success", command=button_press)
download_button.pack(pady=20)


root.mainloop()