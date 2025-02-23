import tkinter as tk
from tkinter import messagebox
import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageTk
import requests
import pyttsx3
import time

# Spotify credentials
SPOTIPY_CLIENT_ID = "fill it by ur id"
SPOTIPY_CLIENT_SECRET = "fill it by ur id"
SPOTIPY_REDIRECT_URI = "fill it with url"
MOOD_PLAYLISTS = {
    "happy": "happy playlist link",
    "sad": "sad playlit link",
    "neutral": "neutral playlist link",
    "angry": "angry playlist link",
    "fear":"fear playlist link",
}

class MoodifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moodify")
        self.root.geometry("600x700")  # Adjusted window width
        self.root.resizable(False, False)

        # Initialize Spotify client
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri=SPOTIPY_REDIRECT_URI,
                scope="user-modify-playback-state user-read-playback-state",
            )
        )

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Background color
        self.root.configure(bg="#FF1493")

        # Title
        self.title_label = tk.Label(
            root, text="Moodify", font=("Arial Rounded MT Bold", 28), bg="#FF1493", fg="white"
        )
        self.title_label.pack(pady=20)

        # Subtitle
        self.subtitle_label = tk.Label(
            root,
            text="Detect your mood and enjoy music 🎶",
            font=("Arial", 12),
            bg="#FF1493",
            fg="white",
        )
        self.subtitle_label.pack(pady=10)

        # Buttons
        self.start_camera_button = self.create_button("Start Camera", self.start_camera)
        self.start_camera_button.pack(pady=10)

        self.capture_button = self.create_button("Capture Image", self.capture_image)
        self.capture_button.pack(pady=10)

        self.stop_camera_button = self.create_button("Stop Camera", self.stop_camera)
        self.stop_camera_button.pack(pady=10)

        # Song info display
        self.song_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg="#FF1493",
            fg="white",
            wraplength=600,
            justify="center",  # Center text
            width=40  # Adjusted width
        )
        self.song_label.pack(pady=20)

        self.album_art_label = tk.Label(self.root, bg="#FF1493")
        self.album_art_label.pack(pady=10)

        # Footer
        self.footer_label = tk.Label(
            root,
            text="By using this app, you agree to our terms of service.",
            font=("Arial", 10),
            bg="#FF1493",
            fg="white",
        )
        self.footer_label.pack(side="bottom", fill="x", pady=10)

        self.current_mood = None
        self.current_song_name = None
        self.current_artist_name = None

    def create_button(self, text, command):
        return tk.Button(
            self.root,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#FF1493",
            activebackground="#FF69B4",
            activeforeground="white",
            bd=2,
            relief="solid",
            padx=10,
            pady=5,
        )

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.display_camera()

    def display_camera(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow("Camera", frame)
                self.root.after(10, self.display_camera)

    def capture_image(self):
        if not hasattr(self, 'cap') or not self.cap.isOpened():
            messagebox.showwarning("Camera Not Running", "Please start the camera first.")
            return

        ret, frame = self.cap.read()
        if ret:
            print("Image captured, analyzing mood...")
            mood = self.detect_mood_from_frame(frame)
            if mood:
                messagebox.showinfo("Mood Detected", f"Detected mood: {mood}")
                self.play_music(mood)
            else:
                messagebox.showerror("Error", "Mood detection failed.")
        else:
            messagebox.showerror("Error", "Failed to capture frame.")

    def detect_mood_from_frame(self, frame):
        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            if isinstance(result, list):
                result = result[0]
            self.current_mood = result.get("dominant_emotion", None)
            return self.current_mood
        except Exception as e:
            print(f"Error analyzing mood: {e}")
            return None

    def play_music(self, mood):
        playlist_uri = MOOD_PLAYLISTS.get(mood)
        if not playlist_uri:
            messagebox.showerror("Error", f"No playlist found for mood: {mood}")
            return

        try:
            # Stop any currently playing music before starting the new one
            self.sp.pause_playback()

            # Mute the playback before starting the next song
            self.sp.volume(0)

            # Start playback of the new playlist (already muted)
            self.sp.start_playback(context_uri=playlist_uri)
            time.sleep(1)  # Small delay to ensure playback starts

            self.update_song_info()  # Update song info in the UI
            self.announce_mood_and_song()  # Announce mood and song

        except spotipy.exceptions.SpotifyException as e:
            messagebox.showerror("Spotify Error", f"Error playing playlist: {e}")

    def update_song_info(self):
        try:
            current_playback = self.sp.current_playback()
            if current_playback and current_playback.get('item'):
                song_name = current_playback['item']['name']
                artist_name = current_playback['item']['artists'][0]['name']
                album_art_url = current_playback['item']['album']['images'][0]['url']

                # Update current song and artist names
                self.current_song_name = song_name
                self.current_artist_name = artist_name

                # Update GUI
                self.song_label.config(
                    text=f"Now Playing: {song_name} by {artist_name}",
                    font=("Arial", 10),
                    wraplength=600,
                    justify="center",
                )

                # Update album art
                album_art_image = Image.open(requests.get(album_art_url, stream=True).raw)
                album_art_image = album_art_image.resize((150, 150), Image.Resampling.LANCZOS)
                album_art_image_tk = ImageTk.PhotoImage(album_art_image)
                self.album_art_label.config(image=album_art_image_tk)
                self.album_art_label.image = album_art_image_tk
        except Exception as e:
            print(f"Error updating song info: {e}")
            messagebox.showerror("Error", "An error occurred while updating the song info.")

    def announce_mood_and_song(self):
        try:
            # Pause playback before starting the announcement
            self.sp.pause_playback()

            # Small delay to ensure music is paused before announcement starts
            time.sleep(0.2)  # Adjust the delay if needed

            # Announce mood first
            if self.current_mood:
                self.engine.say(f"Your current mood is {self.current_mood}.")
                self.engine.runAndWait()

            # Announce song name
            if self.current_song_name and self.current_artist_name:
                self.engine.say(f"The song playing is {self.current_song_name} by {self.current_artist_name}.")
                self.engine.runAndWait()

            # Unmute the playback and resume playback after announcement is finished
            self.sp.volume(100)  # Restore the volume to normal
            self.sp.start_playback()  # Resume playback
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def stop_camera(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MoodifyApp(root)
    root.mainloop()
