from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from mp3ify import convert_to_mp3
import re

root = tb.Window(themename="darkly")
root.title("YouTube MP3ify")
root.iconbitmap('ytdl.ico')
root.geometry('500x370')


def download_vid_noauth(link: str) -> tuple:
    """
            Downloads video from YouTube, with no oauth cuz gui, as a mp4 file and returns video path and title.
            """
    try:
        video = YouTube(link, use_oauth=False, allow_oauth_cache=False)

    except VideoUnavailable:
        print(f"Video at link:{link} is unavailable!")

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
        video = download_vid_noauth(url)
        convert_to_mp3(video[0], video[1])
    print("All Playlist Videos Downloaded.")


# entry function
# noinspection PyArgumentList
def button_press():
    if chosen_type.get() == "playlist":
        download_playlist_noauth(entry.get())
    elif chosen_type.get() == "video":
        video = download_vid_noauth(entry.get())
        convert_to_mp3(video[0], video[1])

    label2.config(text=f"You have selected a: {chosen_type.get()} at the link: {entry.get()}")
    download_button.config(bootstyle="success, outline", text="Downloading...")


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

label2 = tb.Label(root, text="You have selected a {} with at the link {}")
label2.pack(pady=10)

# button
download_button = tb.Button(text="Convert/Download", bootstyle="success", command=button_press)
download_button.pack(pady=20)


root.mainloop()
