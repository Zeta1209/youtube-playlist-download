import time
import os
import json
from googleapiclient.discovery import build
import yt_dlp
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import re
import tempfile

API_KEY = 'YOURAPIKEY'
PLAYLIST_ID = 'THE PLAYLIST ID OF YOUR PLAYLIST'
DOWNLOAD_DIR = './music'
DOWNLOAD_HISTORY_FILE = 'downloaded_videos.json'

# Function to fetch the videos in a playlist
def fetch_playlist_videos(api_key, playlist_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.playlistItems().list(
        part='contentDetails',
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    return [item['contentDetails']['videoId'] for item in response['items']]

def sanitize_filename(title):
    # Replace invalid characters with underscores or remove them
    return re.sub(r'[\/:*?"<>|]', '_', title).strip()

# Function to download video as mp3
def download_audio(video_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),  # Use video ID for temporary filename
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)  # Get the title of the video

        # Sanitize the filename to avoid invalid characters
        sanitized_title = sanitize_filename(video_title)
        temp_file_path = os.path.join(output_dir, f"{info_dict['id']}.mp3")  # Use temporary filename

        # Rename the file to use the sanitized title
        final_file_path = os.path.join(output_dir, f"{sanitized_title}.mp3")
        if os.path.exists(temp_file_path):
            os.rename(temp_file_path, final_file_path)

        return final_file_path

# Function to load downloaded video IDs from file
def load_downloaded_videos(file_path):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        # If the file doesn't exist or is empty, return an empty list
        return []
    else:
        with open(file_path, 'r') as f:
            return json.load(f)

# Function to save downloaded video IDs to file
def save_downloaded_videos(file_path, video_ids):
    with open(file_path, 'w') as f:
        json.dump(video_ids, f, indent=4)

# Function to crop silent parts of the audio
def crop_silence(file_path):
    print(f"Attempting to crop silence for file: {file_path}")  # Debugging line
    audio = AudioSegment.from_mp3(file_path)
    non_silent_ranges = detect_nonsilent(audio, min_silence_len=500, silence_thresh=-40)
    
    if non_silent_ranges:
        start_trim = non_silent_ranges[0][0]
        end_trim = non_silent_ranges[-1][1]
        cropped_audio = audio[start_trim:end_trim]
        cropped_audio.export(file_path, format="mp3")

# Main function to download new videos and process them
def main():
    downloaded_videos = load_downloaded_videos(DOWNLOAD_HISTORY_FILE)

    while True:
        video_ids = fetch_playlist_videos(API_KEY, PLAYLIST_ID)
        new_videos = [vid for vid in video_ids if vid not in downloaded_videos]

        if new_videos:
            for video_id in new_videos:
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                
                # Download the video and get the output path (file path with video title)
                output_path = download_audio(video_url, DOWNLOAD_DIR)
                
                # Crop silence
                crop_silence(output_path)

                # Update downloaded videos
                downloaded_videos.append(video_id)
                save_downloaded_videos(DOWNLOAD_HISTORY_FILE, downloaded_videos)

            print("All new videos processed successfully.")
        else:
            print("No new videos to download. Waiting for new videos...")

        # Wait before checking again (e.g., 30 sec)
        time.sleep(30)

if __name__ == '__main__':
    main()
