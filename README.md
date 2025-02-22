# Moodify 🎶🎭

Moodify is a Python-based application that detects your mood using facial recognition and plays music accordingly via Spotify.

## Features 🚀
- Uses **DeepFace** to analyze emotions from your webcam.
- Connects to **Spotify** to play music based on detected mood.
- Provides a **GUI interface** built with **Tkinter**.
- Displays **album art** and song details.

## Installation 🛠
### Prerequisites
Ensure you have **Python 3.7+** installed.

### Clone the Repository
bash
git clone https://github.com/Sabarish0605/moodify.git
cd moodify


### Install Dependencies
Use `pip` to install required libraries:
bash
pip install opencv-python deepface spotipy pillow pyttsx3 requests


## Usage 🎥🎼
1. Run the application:
   bash
   python d2.py
   ```
2. Click *Start Camera* to enable the webcam.
3. Capture an image using *Capture Image*.
4. The app will analyze your mood and play a corresponding Spotify playlist.

## Configuration 🎧
Update SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI with your *Spotify API credentials*.

## Mood-Based Playlists 🎵
- *Happy* 😊 → Upbeat playlist
- *Sad* 😢 → Slow and emotional playlist
- *Neutral* 😐 → Chill music
- *Angry* 😡 → High-energy music

## Issues & Contributions 🤝
Feel free to *open issues* or *contribute* by submitting pull requests!

---
