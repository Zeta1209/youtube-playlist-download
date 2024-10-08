# YouTube Playlist MP3 Downloader

This Python script allows you to download all videos from a YouTube playlist, convert them to MP3 format and remove silent parts.

## Features

- Downloads videos from a YouTube playlist as MP3 files.
- Automatically trims silence from the start and end of the audio.
- Keeps track of downloaded videos to avoid duplicates.

## Requirements

- Python 3.x
- FFmpeg (required for audio conversion)
- YouTube Data API v3

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install the required Python libraries:**

    Run the run.bat file or run the command below:
    
    ```bash
    pip install -r requirements.txt
    ```

3. **Install FFmpeg:**

    - For Windows: [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system's PATH.
    - For macOS: Install via Homebrew:

      ```bash
      brew install ffmpeg
      ```

    - For Linux (Debian-based):

      ```bash
      sudo apt update
      sudo apt install ffmpeg
      ```

## Setup

1. **Get a YouTube Data API Key:**

    - Go to the [Google Cloud Console](https://console.developers.google.com/).
    - Create a new project or use an existing one.
    - Enable the "YouTube Data API v3" for the project.
    - Go to **Credentials** and create an API key.
    - Copy the generated API key.

2. **Find the YouTube Playlist ID:**

    - Go to the YouTube playlist you want to download.
    - The playlist ID is the part of the URL after `list=`. For example, in the URL:

      ```
      https://www.youtube.com/playlist?list=PLJNsKqGTcYkZw43XxNkyM_RRrh1uEBvZ6
      ```

      The playlist ID is `PLJNsKqGTcYkZw43XxNkyM_RRrh1uEBvZ6`.

3. **Add your API Key and Playlist ID to the Script:**

    Open the Python script (`MusicDL.py`) and update the following variables with your API key and playlist ID:

    ```python
    API_KEY = 'YOUR_API_KEY'
    PLAYLIST_ID = 'YOUR_PLAYLIST_ID'
    ```

## Usage

1. **Run the script:**

    After you have set up everything, run the run.bat file or run the script using the following command:

    ```bash
    python MusicDL.py
    ```

    The script will start downloading videos, converting them to MP3 and trimming silence.

2. **Wait for new videos:**

    The script checks for new videos in the playlist every 30 seconds. If it finds new videos, it downloads and processes them automatically.

