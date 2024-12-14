import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pyautogui, random, threading, time, pygame, sys, os

class dance:
    def __init__(self, gif_paths, music_folder, bpm_file_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.music_folder = os.path.abspath(os.path.join(base_path, music_folder))
        self.bpm_file_path = os.path.abspath(os.path.join(base_path, bpm_file_path))
        self.music_paths, self.bpms = self.load_music_and_bpms(self.music_folder, self.bpm_file_path)

        gif_path = random.choice(gif_paths)
        self.music_path, self.bpm = random.choice(list(zip(self.music_paths, self.bpms)))
        self.gif_path = os.path.join(base_path, gif_path)
        self.music_path = os.path.join(base_path, self.music_path)

        self.root = tk.Tk()
        self.root.attributes("-topmost", True, "-transparentcolor", "white")
        self.root.overrideredirect(True)

        self.frames = [ImageTk.PhotoImage(img.convert('RGBA')) for img in ImageSequence.Iterator(Image.open(self.gif_path))]
        self.label = tk.Label(self.root, bd=0, bg='white')
        self.label.pack()

        self.frame_index = 0
        self.update_gif()
        threading.Thread(target=self.reposition_gif).start()
        threading.Thread(target=self.play_music).start()

    def load_music_and_bpms(self, music_folder, bpm_file_path):
        with open(bpm_file_path, 'r') as bpm_file:
            bpms = {line.split('=')[0].strip(): int(line.split('=')[1].strip()) for line in bpm_file if '=' in line}

        music_paths = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith('.wav') and f in bpms]
        return music_paths, [bpms[os.path.basename(path)] for path in music_paths]

    def update_gif(self):
        self.label.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(100, self.update_gif)

    def reposition_gif(self):
        while True:
            screen_width, screen_height = pyautogui.size()
            x, y = random.randint(0, screen_width - self.frames[0].width()), random.randint(0, screen_height - self.frames[0].height())
            self.root.geometry(f"{self.frames[0].width()}x{self.frames[0].height()}+{x}+{y}")
            time.sleep(60 / self.bpm)

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(loops=-1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    music_folder = "../assets/audio"
    bpm_file_path = "../assets/bpm/bpm.txt"
    gif_paths = ["../assets/gif/lain.gif"]

    app = dance(gif_paths, music_folder, bpm_file_path)
    app.run()
