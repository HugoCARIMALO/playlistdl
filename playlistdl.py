import os
import threading
from pytube import Playlist
import tkinter as tk
from tkinter import ttk

YOUTUBE_STREAM_AUDIO = '140'  # Modify the value to download a different stream

def download_and_convert(root, text_label, sub_label, progress_bar, video, path, total_videos, index):
    text_label.config(text=f"Téléchargement {index}/{total_videos} :")
    sub_label.config(text=f"{video.title}")
    
    audio_stream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
    video_filename = audio_stream.download(output_path=path)
    rename_to_mp3(video_filename, path)
    
    progress_bar["value"] = index
    root.update_idletasks()

def download_playlist(root, text_label, sub_label, progress_bar, text_entry):
    playlist_url = text_entry.get()
    playlist = Playlist(playlist_url)
    total_videos = len(playlist.videos)
    path = os.path.join(os.getcwd(), "playlist")
    os.makedirs(path, exist_ok=True)
    progress_bar["maximum"] = total_videos
    
    for index, video in enumerate(playlist.videos, start=1):
        download_and_convert(root, text_label, sub_label, progress_bar, video, path, total_videos, index)
    
    text_label.config(text="Téléchargement terminé")
    sub_label.config(text="")

def rename_to_mp3(video_filename, path):
    mp3_filename = os.path.splitext(video_filename)[0] + '.mp3'
    existing_mp3_path = os.path.join(path, mp3_filename)
    if os.path.exists(existing_mp3_path):
        os.remove(existing_mp3_path)
    os.rename(video_filename, existing_mp3_path)

def create_ui():
    root = tk.Tk()
    root.title("Téléchargement de Playlist YouTube ~ Hugo UwU")
    root.geometry("600x250")

    style = ttk.Style()
    style.configure("TButton", padding=5, relief="flat", background="#007acc", foreground="white")
    style.map("TButton", background=[("active", "#005fbf")])

    label = ttk.Label(root, text="URL de la playlist YouTube:")
    label.pack(pady=10)

    text_entry = ttk.Entry(root, font=("Tahoma", 12), width=50)
    text_entry.pack(pady=5)
    text_entry.insert(0, 'https://www.youtube.com/playlist?list=PLZHRfekrKz7hf33uNDh_0wAud1BYidNmc')

    button = ttk.Button(root, text="Télécharger la playlist", command=lambda: threading.Thread(target=download_playlist, args=(root, text_label, sub_label, progress_bar, text_entry)).start())
    button.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=10)

    text_label = ttk.Label(root, text="", font=("Tahoma", 12))
    text_label.pack(pady=5)

    sub_label = ttk.Label(root, text="", font=("Tahoma", 12), wraplength=580)
    sub_label.pack(pady=5)

    return root, progress_bar, text_label, sub_label

if __name__ == "__main__":
    root, progress_bar, text_label, sub_label = create_ui()
    root.mainloop()
