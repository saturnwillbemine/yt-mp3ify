# YTMP3ify

A simple python YouTube-to-MP3 converter.


## To run locally


### Using .exe file

Running `YTMP3ify.exe` is an windowed application where you can use a graphical user interface to convert videos.

The graphical interface currently doesn't support age restricted videos, use CLI to download them.

The output folder is created where ever the file was ran.

### Using command line

```bash
  git clone https://github.com/saturnwillbemine/yt-mp3ify
```

Go to the project directory

```bash
  cd yt-mp3ify
```

Install dependencies

```bash
  pip install pytube
  pip install moviepy
  pip install proglog
```

Available `link_types`
- `v` to download a single video.
- `p` to download a playlist.


`video_link` is either a YouTube playlist or video link, depending on `link_type` chosen..

```bash
  python mp3ify.py link_type video_link
```

You can also just use 

```bash
  python mp3ify.py
```
It will still run, it will ask for inputs during runtime.

## Authors

- [@saturnwillbemine](https://www.github.com/saturnwwillbemine)

Shoutout [pytube](https://github.com/pytube/pytube) and [moviepy](https://github.com/Zulko/moviepy)
## Screenshots

![App Screenshot](https://i.ibb.co/k9LCSF0/image-2023-10-09-163942239.png)

