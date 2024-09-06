<h2 align="center">🪩 dance 🪩</h2>

---

### 🚀 Description
This project plays a random dancing GIF that moves in sync with the BPM of a randomly selected music track. It uses **Tkinter** for the GUI, **Pillow** for GIF handling, and **Pygame** for music.

---

### 🎵 Adding Songs
To add a song, list its filename (e.g., **909.mp3**) and BPM (e.g., **127**) in **BPM.txt** in the **bpm** folder:
```
909.mp3 = 127
```

---

### 🎨 Features
- 🎶 Plays a random GIF synchronized with the BPM of a music track.
- 🖼️ Moves the GIF randomly across the screen at intervals matching the BPM.
- 🔁 Looping music and GIF for a continuous experience.

---

### 🛠️ Technologies Used
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Tkinter](https://img.shields.io/badge/-Tkinter-FF4500?style=for-the-badge)
![Pillow](https://img.shields.io/badge/-Pillow-FFD700?logo=pillow&style=for-the-badge)
![Pygame](https://img.shields.io/badge/-Pygame-00FF00?logo=pygame&style=for-the-badge)

---

### 🔧 Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dance-gif-player.git
   ```
2. Navigate to the project directory:
   ```bash
   cd dance-gif-player
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

### 📂 Project Structure
```
.
├── assets
│   ├── audio           # Folder containing music files (MP3)
│   ├── bpm             # Folder containing BPM configuration file
│   └── gif             # Folder containing the GIF file
├── main.py             # Main script to run the application
├── requirements.txt    # Python dependencies file
└── README.md           # Project documentation
```

---

### 📝 To-Do List
- 🔄 Add more music tracks lol.
- 🎶 Support for more audio formats? Maybe.
- 🕹️ A CLOSE BUTTON LMAO.

---

### 🤝 Contributions
Feel free to fork this repository, open issues, or submit pull requests!