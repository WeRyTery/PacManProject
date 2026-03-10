import pygame as pg
import os

from ..core.constants import SOUND_DIR


class Sound_Manager:
    def __init__(self):
        pg.mixer.init()
        self.sounds = {}
        self.load_all_sounds()

    def load_all_sounds(self):
        if not os.path.exists(SOUND_DIR):
            print(f"Папка {SOUND_DIR} не найдена!")
            return

        valid_extensions = (".wav", ".mp3", ".ogg")
        for file in os.listdir(SOUND_DIR):
            if file.lower().endswith(valid_extensions):
                name = os.path.splitext(file)[0]  # removes file extension
                try:
                    self.sounds[name] = pg.mixer.Sound(os.path.join(SOUND_DIR, file))
                    print(f"Загружен звук: {name}")
                except Exception as e:
                    print(f"Ошибка загрузки {file}: {e}")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Sound {name} was not found!")

    def set_volume(self, volume_percent):
        volume_float = volume_percent / 100.0
        for sound in self.sounds.values():
            sound.set_volume(volume_float)
