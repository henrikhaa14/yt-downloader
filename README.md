# YouTube downloader

A small Python command-line downloader using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Setup

```sh
python -m pip install -r requirements.txt
```

## Usage

Run the downloader and answer its prompts to choose audio or video and an
output directory. Press Enter at the directory prompt to use the current
directory:

```sh
python downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

You can also provide either choice as an option to skip that prompt:

```sh
python downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --type audio --output ./downloads
```

Use `--help` to see all options. Audio is saved in the best format provided by
YouTube; it is not converted to MP3. For video, yt-dlp selects the best video
and audio streams and merges them when FFmpeg is installed. Without FFmpeg, it
falls back to the best single stream containing both audio and video.
