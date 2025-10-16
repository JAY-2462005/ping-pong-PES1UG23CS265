import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialize mixer safely (catch missing audio devices)
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            print("[Warning] Audio device not available. Sound disabled.")
            self.enabled = False

        self.sounds = {}

        if self.enabled:
            self.load_sounds()

    def load_sounds(self):
        """Load .wav sound files, fallback gracefully if missing."""
        base_path = os.path.join(os.path.dirname(__file__), "assets", "sounds")
        self.sounds = {
            "paddle_hit": self._load_sound(base_path, "paddle_hit.wav"),
            "wall_bounce": self._load_sound(base_path, "wall_bounce.wav"),
            "score": self._load_sound(base_path, "score.wav"),
        }

    def _load_sound(self, base_path, filename):
        path = os.path.join(base_path, filename)
        if os.path.exists(path):
            try:
                return pygame.mixer.Sound(path)
            except pygame.error:
                print(f"[Warning] Could not load sound: {filename}")
                return None
        else:
            print(f"[Info] Sound file missing: {filename}")
            return None

    def play(self, name):
        """Play a named sound effect if available."""
        if self.enabled and name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
