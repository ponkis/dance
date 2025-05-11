import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageSequence
import pyautogui
import random
import threading
import time
import pygame
import sys
import os


class DanceApp:
    DEFAULT_GIF_FRAME_DURATION_MS = 100
    MIN_GIF_DELAY_MS = 20
    MAX_GIF_DELAY_MS = 500
    BPM_NORMALIZATION_TARGET = 120
    BPM_SENSITIVITY_FACTOR = 200.0

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.selected_gif_paths = []
        self.audio_files = []
        self.bpms = []

        self.current_gif_path = None
        self.current_music_path = None
        self.current_bpm = self.BPM_NORMALIZATION_TARGET

        self.frames_data = []
        self.frame_index = 0
        self.gif_update_id = None

        self.reposition_thread_stop_event = threading.Event()
        self.app_running = True

        try:
            pygame.mixer.init()
        except pygame.error as e:
            messagebox.showerror(
                "Pygame Error", f"Failed to initialize audio mixer: {e}"
            )
            self.root.destroy()
            sys.exit(1)

        if not self.load_media_files_dialogs():
            messagebox.showerror("Setup Error", "No media files loaded. Exiting.")
            self.cleanup_and_exit()
            return

        if not self.select_initial_media_and_load_gif():
            messagebox.showerror(
                "Setup Error", "Failed to select or load initial media. Exiting."
            )
            self.cleanup_and_exit()
            return

        self.setup_ui()
        self.root.deiconify()

    def load_media_files_dialogs(self):
        gif_files = filedialog.askopenfilenames(
            parent=self.root,
            title="Please choose one or more GIF files",
            filetypes=[("GIF files", "*.gif")],
        )
        if not gif_files:
            messagebox.showwarning("Warning", "No GIF files selected!")
            return False
        self.selected_gif_paths = list(gif_files)

        audio_dialog_files = filedialog.askopenfilenames(
            parent=self.root,
            title="Please choose one or more audio files",
            filetypes=[
                ("Waveform Audio File Format", "*.wav"),
                ("MP3 Audio File", "*.mp3"),
                ("OGG Audio File", "*.ogg"),
            ],
        )
        if not audio_dialog_files:
            messagebox.showwarning("Warning", "No audio files selected!")
            return False

        for file_path in audio_dialog_files:
            file_name = os.path.basename(file_path)
            bpm = simpledialog.askinteger(
                "BPM Input",
                f"Enter BPM for:\n{file_name}",
                parent=self.root,
                minvalue=1,
                maxvalue=500,
            )
            if bpm is None:
                messagebox.showinfo(
                    "Info", f"Skipping audio file '{file_name}' due to no BPM provided."
                )
                continue
            self.audio_files.append(file_path)
            self.bpms.append(bpm)

        if not self.audio_files:
            messagebox.showwarning("Warning", "No audio files with BPMs were loaded!")
            return False
        return True

    def select_initial_media_and_load_gif(self):
        if not self.selected_gif_paths or not self.audio_files:
            return False

        self.current_gif_path = random.choice(self.selected_gif_paths)

        combined_audio_bpm = list(zip(self.audio_files, self.bpms))
        if not combined_audio_bpm:
            return False
        self.current_music_path, self.current_bpm = random.choice(combined_audio_bpm)

        return self.load_gif_frames(self.current_gif_path)

    def load_gif_frames(self, gif_path):
        self.frames_data = []
        try:
            with Image.open(gif_path) as img_gif:
                for frame in ImageSequence.Iterator(img_gif):
                    duration = frame.info.get(
                        "duration", self.DEFAULT_GIF_FRAME_DURATION_MS
                    )
                    if duration < self.MIN_GIF_DELAY_MS / 2:
                        duration = self.DEFAULT_GIF_FRAME_DURATION_MS

                    rgba_frame = frame.convert("RGBA")
                    photo_image = ImageTk.PhotoImage(rgba_frame)
                    self.frames_data.append(
                        {"image": photo_image, "duration": duration}
                    )
        except FileNotFoundError:
            messagebox.showerror("Error", f"GIF file not found: {gif_path}")
            return False
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load GIF '{os.path.basename(gif_path)}': {e}"
            )
            return False

        if not self.frames_data:
            messagebox.showerror(
                "Error", f"No frames loaded from GIF: {os.path.basename(gif_path)}"
            )
            return False
        return True

    def setup_ui(self):
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self.root.overrideredirect(True)

        if not self.frames_data:
            messagebox.showerror("UI Error", "Cannot setup UI without GIF frames.")
            self.cleanup_and_exit()
            return

        self.label = tk.Label(self.root, bd=0, bg="white")
        self.label.pack()

        img_width = self.frames_data[0]["image"].width()
        img_height = self.frames_data[0]["image"].height()
        screen_width, screen_height = pyautogui.size()
        x = (screen_width - img_width) // 2
        y = (screen_height - img_height) // 2
        self.root.geometry(f"{img_width}x{img_height}+{x}+{y}")

        self.root.bind("<Escape>", lambda event: self.on_close())

    def update_gif(self):
        if not self.app_running or not self.frames_data:
            return

        current_frame_data = self.frames_data[self.frame_index]
        self.label.config(image=current_frame_data["image"])
        self.frame_index = (self.frame_index + 1) % len(self.frames_data)

        original_delay = current_frame_data["duration"]

        bpm_factor = 1.0 - (
            (self.current_bpm - self.BPM_NORMALIZATION_TARGET)
            / self.BPM_SENSITIVITY_FACTOR
        )
        bpm_factor = max(0.5, min(1.5, bpm_factor))

        adjusted_delay = int(original_delay * bpm_factor)
        adjusted_delay = max(
            self.MIN_GIF_DELAY_MS, min(self.MAX_GIF_DELAY_MS, adjusted_delay)
        )

        self.gif_update_id = self.root.after(adjusted_delay, self.update_gif)

    def reposition_gif(self):
        while not self.reposition_thread_stop_event.is_set():
            if not self.app_running or not self.frames_data:
                self.reposition_thread_stop_event.wait(0.1)
                continue

            try:
                frame_width = self.frames_data[0]["image"].width()
                frame_height = self.frames_data[0]["image"].height()
                screen_width, screen_height = pyautogui.size()

                max_x = screen_width - frame_width
                max_y = screen_height - frame_height

                x = random.randint(0, max(0, max_x))
                y = random.randint(0, max(0, max_y))

                self.root.after(
                    0,
                    lambda: self.root.geometry(f"{frame_width}x{frame_height}+{x}+{y}"),
                )
            except tk.TclError:
                break
            except Exception as e:
                print(f"Error in reposition_gif: {e}")
                self.reposition_thread_stop_event.wait(1)
                continue

            sleep_duration = 60.0 / max(1, self.current_bpm)
            self.reposition_thread_stop_event.wait(sleep_duration)

    def play_music(self):
        if not self.current_music_path or not self.app_running:
            return
        try:
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            messagebox.showerror(
                "Music Error",
                f"Could not load or play music '{os.path.basename(self.current_music_path)}': {e}",
            )

    def on_close(self):
        if not self.app_running:
            return
        print("Closing application...")
        self.app_running = False

        if self.gif_update_id:
            self.root.after_cancel(self.gif_update_id)
            self.gif_update_id = None

        self.reposition_thread_stop_event.set()

        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except pygame.error as e:
            print(f"Pygame error during music stop/unload: {e}")

        self.cleanup_and_exit()

    def cleanup_and_exit(self):
        if self.root:
            try:
                self.root.destroy()
            except tk.TclError:
                pass
            self.root = None

        pygame.quit()
        sys.exit(0)

    def run(self):
        if not self.app_running:
            return

        self.update_gif()

        self.reposition_thread = threading.Thread(
            target=self.reposition_gif, daemon=True
        )
        self.reposition_thread.start()

        self.music_thread = threading.Thread(target=self.play_music, daemon=True)
        self.music_thread.start()

        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected, closing.")
        finally:
            self.on_close()


if __name__ == "__main__":
    try:
        pyautogui.size()
    except Exception as e:
        print(f"Error: PyAutoGUI could not get screen dimensions: {e}")
        print(
            "This program requires a graphical environment where screen size can be determined."
        )
        sys.exit(1)

    app = DanceApp()
    if hasattr(app, "app_running") and app.app_running:
        app.run()
    else:
        print("Application did not initialize correctly.")