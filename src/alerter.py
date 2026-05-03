# src/alerter.py

import pygame
import os


class Alerter:
    def __init__(self):
        pygame.mixer.init()
        self.alert_playing = False
        self.sound = None
        self._generate_beep()

    def _generate_beep(self):
        """Generate a simple beep sound without needing an audio file."""
        import numpy as np
        sample_rate = 44100
        duration = 1.0
        frequency = 880

        t = np.linspace(0, duration, int(sample_rate * duration))
        wave = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)
        wave = np.column_stack([wave, wave])  # stereo

        self.sound = pygame.sndarray.make_sound(wave)

    def play(self):
        """Play alert sound if not already playing."""
        if not self.alert_playing:
            self.sound.play(-1)  # loop indefinitely
            self.alert_playing = True

    def stop(self):
        """Stop alert sound."""
        if self.alert_playing:
            self.sound.stop()
            self.alert_playing = False