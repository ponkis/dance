import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageSequence
import pyautogui, random, threading, time, pygame, sys
import os


class DanceApp:
    def __init__(self, gif_paths):
        self.gif_paths = gif_paths
        self.audio_files = []
        self.bpms = []

        self.load_audio_and_bpms()

        self.gif_path = random.choice(self.gif_paths)
        self.music_path, self.bpm = random.choice(
            list(zip(self.audio_files, self.bpms))
        )

        self.root = tk.Tk()
        self.root.attributes("-topmost", True, "-transparentcolor", "white")
        self.root.overrideredirect(True)

        self.frames = [
            ImageTk.PhotoImage(img.convert("RGBA"))
            for img in ImageSequence.Iterator(Image.open(self.gif_path))
        ]
        self.label = tk.Label(self.root, bd=0, bg="white")
        self.label.pack()

        self.frame_index = 0
        self.update_gif()
        threading.Thread(target=self.reposition_gif).start()
        threading.Thread(target=self.play_music).start()

    def load_audio_and_bpms(self):
        files = filedialog.askopenfilenames(
            title="Please choose one or more audio files",
            filetypes=[
                ("Waveform Audio File Format", "*.wav"),
                ("MP3 Audio File", "*.mp3"),
                ("OGG Audio File", "*.ogg"),
            ],
        )

        if not files:
            messagebox.showwarning("Warning", "No audio files selected!")
            sys.exit()

        for file in files:
            file_name = os.path.basename(file)
            bpm = simpledialog.askinteger(
                "BPM for the audio file/s", f"Put the BPM of:\n{file_name}", minvalue=1
            )

            if bpm is None:
                messagebox.showerror("Error", "Invalid BPM.")
                sys.exit()

            self.audio_files.append(file)
            self.bpms.append(bpm)

    def update_gif(self):
        self.label.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(100, self.update_gif)

    def reposition_gif(self):
        while True:
            screen_width, screen_height = pyautogui.size()
            x = random.randint(0, screen_width - self.frames[0].width())
            y = random.randint(0, screen_height - self.frames[0].height())
            self.root.geometry(
                f"{self.frames[0].width()}x{self.frames[0].height()}+{x}+{y}"
            )
            time.sleep(60 / self.bpm)

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(loops=-1)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gif_paths = ["assets/images/lain.gif"]
    app = DanceApp(gif_paths)
    app.run()