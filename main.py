import os
import pygame
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.lang import Builder


class MusicPlayer(FloatLayout):
    current_track_label = StringProperty("No tracks available")
    music_folder = "/storage/emulated/0/Music"
    playlist = []
    current_track = 0

    def setup(self):
        """Setup the music player by loading tracks."""
        pygame.mixer.init()

        # Load the playlist
        if os.path.exists(self.music_folder):
            files = os.listdir(self.music_folder)
            for file in files:
                if file.endswith(".mp3"):  # Filter only .mp3 files
                    self.playlist.append(file)
        else:
            print("Music folder not found!")

        # Update the track label if tracks are available
        if self.playlist:
            self.current_track_label = f"Track: {self.playlist[self.current_track]}"
        else:
            self.current_track_label = "No tracks available"

    def play_music(self):
        """Play the current track."""
        if not self.playlist:
            print("No tracks to play!")
            return

        track_path = os.path.join(self.music_folder, self.playlist[self.current_track])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        print(f"Playing: {self.playlist[self.current_track]}")

    def stop_music(self):
        """Stop the current music."""
        pygame.mixer.music.stop()
        print("Music stopped.")

    def play_next(self):
        """Play the next track."""
        if self.playlist:
            self.current_track += 1
            if self.current_track >= len(self.playlist):
                self.current_track = 0  # Loop back to the first track
            self.update_track_label()
            self.play_music()

    def play_previous(self):
        """Play the previous track."""
        if self.playlist:
            self.current_track -= 1
            if self.current_track < 0:
                self.current_track = len(self.playlist) - 1  # Loop to the last track
            self.update_track_label()
            self.play_music()

    def update_track_label(self):
        """Update the track label to show the current track."""
        if self.playlist:
            self.current_track_label = f"Track: {self.playlist[self.current_track]}"
        else:
            self.current_track_label = "No tracks available"


class MusicPlayerApp(App):
    def build(self):
        player = MusicPlayer()
        player.setup()  # Set up the music player (load tracks)
        return player


# Define the layout (merged KV inside the Python file)
Builder.load_string("""
<MusicPlayer>:
    orientation: "vertical"
    padding: 20
    spacing: 10

    Label:
        text: root.current_track_label
        font_size: 18
        halign: "center"
        valign: "middle"
        size_hint: None, None
        size: 600, 50
        pos: 100, 1000  # Positioned manually

    Button:
        text: "Play"
        size_hint: None, None
        size: 300, 100
        pos: 400, 350  # Positioned manually
        on_press: root.play_music()

    Button:
        text: "Stop"
        size_hint: None, None
        size: 300, 100
        pos: 50, 350  # Positioned manually
        on_press: root.stop_music()

    Button:
        text: "Previous"
        size_hint: None, None
        size: 300, 100
        pos: 50, 100  # Positioned manually
        on_press: root.play_previous()

    Button:
        text: "Next"
        size_hint: None, None
        size: 300, 100
        pos: 400, 100  # Positioned manually
        on_press: root.play_next()
""")


if __name__ == "__main__":
    MusicPlayerApp().run()
