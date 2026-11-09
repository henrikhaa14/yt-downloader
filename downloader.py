"""Download YouTube videos or audio with yt-dlp."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any

import yt_dlp


def download_options(media_type: str, destination: Path) -> dict[str, Any]:
    """Build quiet yt-dlp options for the selected media type."""
    options: dict[str, Any] = {
        "outtmpl": str(destination / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    if media_type == "audio":
        options["format"] = "bestaudio/best"
    elif shutil.which("ffmpeg"):
        # Separate streams provide higher resolutions when FFmpeg can merge them.
        options["format"] = "bestvideo*+bestaudio/best"
    else:
        options["format"] = "best"

    return options

def download(url: str, media_type: str, destination: Path) -> Path:
    """Download the best available stream to the destination directory."""
    destination.mkdir(parents=True, exist_ok=True)

    with yt_dlp.YoutubeDL(download_options(media_type, destination)) as downloader:
        info = downloader.extract_info(url, download=True)
        filename = downloader.prepare_filename(info)

    return Path(filename)

def prompt_media_type() -> str:
    """Ask repeatedly until the user selects audio or video."""
    while True:
        choice = input("Download audio or video? [audio/video]: ").strip().lower()
        if choice in ("audio", "video"):
            return choice
        print("Please enter 'audio' or 'video'.")

def prompt_destination() -> Path:
    """Ask for a destination directory, defaulting to the current directory."""
    while True:
        current = Path.cwd()
        answer = input(f"Output directory [{current}]: ").strip()
        destination = Path(answer).expanduser() if answer else current
        if destination.exists() and not destination.is_dir():
            print(f"Not a directory: {destination}")
            continue
        return destination

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the best available YouTube video or audio stream."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-t", "--type", choices=("video", "audio"),
        help="media type (prompted if omitted)",
    )
    parser.add_argument(
        "-o", "--output", type=Path, metavar="DIR",
        help="destination directory (prompted if omitted)",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    media_type = args.type or prompt_media_type()
    destination = args.output or prompt_destination()

    try:
        path = download(args.url, media_type, destination)
    except (yt_dlp.DownloadError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Downloaded to: {path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
