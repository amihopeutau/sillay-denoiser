import os
import numpy as np
import noisereduce as nr
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import PhotoImage
import pygame
import threading
import sys  # Added for resource_path function

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize pygame mixer
pygame.mixer.init()

def play_silly_music(mp3_file):
    """Plays an MP3 file in the background using pygame.mixer."""
    try:
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play(-1)  # -1 means loop forever
    except Exception as e:
        print(f"Error playing music: {e}")

# Stop the music
def stop_music():
    """Stops the currently playing music."""
    pygame.mixer.music.stop()

# Denoise audio
def denoise_audio(input_path, output_path, noise_start=0, noise_end=1000):
    """Denoises an audio file and saves the result."""
    try:
        # Load audio file
        print(f"Loading: {input_path}")
        audio = AudioSegment.from_file(input_path)

        # Convert to numpy array for noisereduce
        samples = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate

        # Extract noise profile (first 1 second)
        print("Extracting noise profile...")
        noise = samples[noise_start:noise_end]

        # Perform noise reduction
        print("Denoising...")
        denoised_samples = nr.reduce_noise(
            y=samples,
            y_noise=noise,
            sr=sample_rate,
            prop_decrease=0.5,
            n_fft=1024,
            win_length=1024,
            hop_length=256
        )

        # Convert back to AudioSegment
        denoised_audio = AudioSegment(
            denoised_samples.tobytes(),
            frame_rate=sample_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )

        # Save denoised audio
        print(f"Saving denoised file: {output_path}")
        denoised_audio.export(output_path, format="wav")
        print("Done!")
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

# Process all audio clips
def process_voicebank(input_dir, output_dir):
    """Processes all audio clips in a directory."""
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    if not os.path.exists(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return False

    # Get list of .wav files
    wav_files = [f for f in os.listdir(input_dir) if f.endswith(".wav")]
    if not wav_files:
        print(f"No .wav files found in: {input_dir}")
        return False

    print(f"Found {len(wav_files)} .wav files to process.")
    for filename in wav_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        print(f"\nProcessing: {filename}")
        success = denoise_audio(input_path, output_path)
        if not success:
            return False
    return True

# GUI
class DenoiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("super sillay denoiser blublublublbubulbu")
        try:
            icon_path = resource_path("icon.ico")  # Use resource_path for the icon
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error loading icon: {e}")
        self.style = ttk.Style()
        self.style.theme_use("vista")

        # Input Directory
        self.input_label = tk.Label(root, text="Input Directory:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)
        self.input_button = tk.Button(root, text="Browse", command=self.browse_input)
        self.input_button.grid(row=0, column=2, padx=10, pady=10)

        # Output Directory
        self.output_label = tk.Label(root, text="Output Directory:")
        self.output_label.grid(row=1, column=0, padx=10, pady=10)
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        self.output_button = tk.Button(root, text="Browse", command=self.browse_output)
        self.output_button.grid(row=1, column=2, padx=10, pady=10)
        self.output_entry.insert(0, r"output")

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Start/Stop Music Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        self.start_music_button = tk.Button(self.button_frame, text="Start Music", command=self.start_music)
        self.start_music_button.pack(side="left", padx=10)

        self.stop_music_button = tk.Button(self.button_frame, text="Stop Music", command=stop_music)
        self.stop_music_button.pack(side="left", padx=10)

        # Run Button
        self.run_button = tk.Button(root, text="Denoise", command=self.run_denoiser)
        self.run_button.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

        # Start playing music
        self.mp3_file = resource_path("sillaypilled.mp3")
        self.music_thread = None
        self.start_music()

    def browse_input(self):
        """Open a dialog to select the input directory."""
        input_dir = filedialog.askdirectory()
        if input_dir:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_dir)

    def browse_output(self):
        """Open a dialog to select the output directory."""
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_dir)

    def start_music(self):
        """Start playing the silly music."""
        if os.path.exists(self.mp3_file):
            if self.music_thread is None or not self.music_thread.is_alive():
                self.music_thread = threading.Thread(target=play_silly_music, args=(self.mp3_file,), daemon=True)
                self.music_thread.start()
        else:
            print(f"MP3 file not found: {self.mp3_file}")

    def run_denoiser(self):
        """Run the denoising process."""
        input_dir = self.input_entry.get()
        output_dir = self.output_entry.get()

        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories.")
            return

        success = process_voicebank(input_dir, output_dir)
        if success:
            messagebox.showinfo("Success", "Denoising complete! Check the output folder.")
        else:
            messagebox.showerror("Error", "An error occurred during denoising. Check the console for details.")

# Run the GUI
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = DenoiseApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")