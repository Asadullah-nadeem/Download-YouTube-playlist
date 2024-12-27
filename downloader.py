import os
from yt_dlp import YoutubeDL
from logger import CustomLogger


def download_media(playlist_url, output_folder, download_type, resolution, log_callback, stop_flag):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': f"bestvideo[height<={resolution}]+bestaudio/best" if download_type == 'video' else 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4' if download_type == 'video' else None,
        'logger': CustomLogger(log_callback),
        'progress_hooks': [lambda d: check_stop_and_log(d)],
    }

    def check_stop_and_log(data):
        if stop_flag.is_set():
            raise Exception("Download stopped by user.")
        log_callback(f"Status: {data.get('status')} | Downloading: {data.get('filename', 'Unknown')}")

    if download_type == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
        except Exception as e:
            log_callback(f"Error: {e}")
