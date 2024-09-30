import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import json
import time
import re

class GalleryDLGUI:
    def __init__(self, master):
        self.master = master
        master.title("Erome Downloader")
        master.geometry("700x600")
        master.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Main frame
        main_frame = ttk.Frame(master, padding="20 20 20 20", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = ttk.Frame(main_frame, style="Card.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # URL input
        url_frame = ttk.Frame(input_frame)
        url_frame.pack(fill=tk.X, pady=(10, 5), padx=10)
        self.url_label = ttk.Label(url_frame, text="Enter erome.com URL(s):", style="Card.TLabel")
        self.url_label.pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50, style="TEntry")
        self.url_entry.pack(side=tk.LEFT, padx=(10, 0), expand=True, fill=tk.X)

        # Directory selection
        dir_frame = ttk.Frame(input_frame)
        dir_frame.pack(fill=tk.X, pady=(5, 10), padx=10)
        self.dir_button = ttk.Button(dir_frame, text="Select Download Directory", command=self.select_directory, style="TButton")
        self.dir_button.pack(side=tk.LEFT)
        self.dir_label = ttk.Label(dir_frame, text="No directory selected", style="Card.TLabel")
        self.dir_label.pack(side=tk.LEFT, padx=(10, 0))

        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # Download button
        self.download_button = ttk.Button(button_frame, text="⬇ Download", command=self.start_download, style="Action.TButton")
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))

        # Stop button (initially disabled)
        self.stop_button = ttk.Button(button_frame, text="⏹ Stop", command=self.stop_download, style="TButton", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

        # History button
        self.history_button = ttk.Button(button_frame, text="🕒 Download History", command=self.show_history, style="TButton")
        self.history_button.pack(side=tk.LEFT)

        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 20))

        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=200, mode="determinate", style="TProgressbar")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="", style="TLabel")
        self.progress_label.pack(side=tk.LEFT, padx=(10, 0))

        # Output frame
        output_frame = ttk.Frame(main_frame, style="Card.TFrame")
        output_frame.pack(fill=tk.BOTH, expand=True)

        # Output area
        self.output_text = tk.Text(output_frame, height=10, width=50, font=("Roboto", 9), wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output_text.config(bg="#ffffff", fg="#333333")

        # Scrollbar for output area
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=scrollbar.set)

        self.download_dir = ""
        self.history_file = "download_history.json"
        self.load_history()

        self.create_tooltips()

        self.download_process = None
        self.stop_flag = threading.Event()

    def configure_styles(self):
        self.style.configure("TButton", padding=10, font=("Roboto", 10))
        self.style.configure("Action.TButton", background="#4CAF50", foreground="white")
        self.style.map("Action.TButton", background=[('active', '#45a049')])
        self.style.configure("TLabel", font=("Roboto", 10))
        self.style.configure("TEntry", font=("Roboto", 10))
        self.style.configure("Card.TFrame", background="#ffffff", relief="raised", borderwidth=1)
        self.style.configure("Card.TLabel", background="#ffffff")
        self.style.configure("Main.TFrame", background="#f0f0f0")
        self.style.configure("TProgressbar", thickness=6)

    def create_tooltips(self):
        self.create_tooltip(self.download_button, "Start downloading the entered URL(s)")
        self.create_tooltip(self.history_button, "View download history")
        self.create_tooltip(self.dir_button, "Choose where to save downloaded files")

    def create_tooltip(self, widget, text):
        def enter(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip

        def leave(event):
            widget.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def select_directory(self):
        self.download_dir = filedialog.askdirectory()
        self.dir_label.config(text=self.download_dir if self.download_dir else "No directory selected")

    def start_download(self):
        urls = [url.strip() for url in self.url_entry.get().split(',')]
        if not urls or not self.download_dir:
            messagebox.showerror("Error", "Please enter URL(s) and select a download directory")
            return

        self.download_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Starting download...\n")
        self.progress_bar["value"] = 0
        self.progress_label.config(text="")
        self.stop_flag.clear()

        thread = threading.Thread(target=self.run_gallery_dl, args=(urls,))
        thread.start()

    def stop_download(self):
        if self.download_process:
            self.stop_flag.set()
            self.download_process.terminate()
            self.output_text.insert(tk.END, "Download stopped by user.\n")
            self.download_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def run_gallery_dl(self, urls):
        try:
            for url in urls:
                if self.stop_flag.is_set():
                    break

                self.output_text.insert(tk.END, f"Downloading: {url}\n")
                self.download_process = subprocess.Popen(
                    ["gallery-dl", "-d", self.download_dir, url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                start_time = time.time()
                total_files = 0
                downloaded_files = 0

                for line in self.download_process.stdout:
                    if self.stop_flag.is_set():
                        break

                    self.output_text.insert(tk.END, line)
                    self.output_text.see(tk.END)

                    if "Downloading" in line:
                        total_files += 1
                    elif "Finished" in line:
                        downloaded_files += 1
                        self.update_progress(downloaded_files, total_files, start_time)

                self.download_process.wait()
                
                if self.download_process.returncode == 0 and not self.stop_flag.is_set():
                    self.output_text.insert(tk.END, f"Download completed successfully for {url}\n")
                    self.add_to_history(url)
                elif not self.stop_flag.is_set():
                    self.output_text.insert(tk.END, f"Download failed for {url} with error code {self.download_process.returncode}\n")
            
            if not self.stop_flag.is_set():
                self.output_text.insert(tk.END, "All downloads completed.\n")
                self.show_open_directory_button()
        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred: {str(e)}\n")
        finally:
            self.download_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress_bar["value"] = 0
            self.progress_label.config(text="")
            self.download_process = None

    def update_progress(self, downloaded, total, start_time):
        if total > 0:
            progress = (downloaded / total) * 100
            self.progress_bar["value"] = progress

            elapsed_time = time.time() - start_time
            if downloaded > 0:
                estimated_total_time = (elapsed_time / downloaded) * total
                remaining_time = estimated_total_time - elapsed_time
                
                self.progress_label.config(text=f"{downloaded}/{total} - {progress:.1f}% - ETA: {self.format_time(remaining_time)}")
            else:
                self.progress_label.config(text=f"{downloaded}/{total} - {progress:.1f}%")

    def format_time(self, seconds):
        minutes, secs = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    def show_open_directory_button(self):
        open_button = ttk.Button(self.master, text="Open Download Directory", command=self.open_download_directory)
        open_button.pack(pady=(10, 0))

    def open_download_directory(self):
        os.startfile(self.download_dir)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def add_to_history(self, url):
        if url not in self.history:
            self.history.append(url)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f)

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Download History")
        history_window.geometry("400x300")

        history_list = tk.Listbox(history_window, width=50)
        history_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for url in self.history:
            history_list.insert(tk.END, url)

        redownload_button = ttk.Button(history_window, text="Re-download Selected", command=lambda: self.redownload(history_list.get(tk.ACTIVE)))
        redownload_button.pack(pady=(0, 10))

    def redownload(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.start_download()

root = tk.Tk()
app = GalleryDLGUI(root)
root.mainloop()