from tkinter import *
from moviepy.editor import *
import ttkbootstrap as tb
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
import re, os, threading


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


def convert_to_mp3(mp4_path: str, mp3_filename: str):
    """
     Converts downloaded mp4 file to a mp3 file.
    """
    file_to_convert = AudioFileClip(mp4_path)

    label2.config(text="Converting to mp3...")

    fixed_filename = ''.join(letter for letter in mp3_filename if letter.isalnum())

    file_to_convert.write_audiofile(f'./Outputs/{str(fixed_filename)}.mp3',
                                    verbose=False, logger=None)

    file_to_convert.close()
    label2.config(text="File conversion complete! Check outputs folder.")

    if os.path.exists(mp4_path):
        os.remove(mp4_path)


# entry function
# noinspection PyArgumentList
def button_press():
    if chosen_type.get() == "playlist":
        download_playlist_noauth(entry.get())

    elif chosen_type.get() == "video":

        video = download_vid_noauth(entry.get())
        convert_to_mp3(video[0], video[1])


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