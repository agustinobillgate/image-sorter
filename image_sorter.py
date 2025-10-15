import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil

class ImageSorter:
  def __init__(self, root):
    self.root = root
    self.root.title("Image Sorter")
    self.root.geometry("1500x1000")
    self.root.configure(bg="black")
    self.image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.ico')
    self.source_folder = ""
    self.image_files = []
    self.current_index = 0
    self.current_image = None
    self.photo = None
    self.poor_folder = ""
    self.good_folder = ""
    self.best_folder = ""
    self.setup_ui()
    self.root.update_idletasks()
    
  def setup_ui(self):
    top_frame = tk.Frame(self.root, pady=10, bg="black")
    top_frame.pack(fill=tk.X)
    select_btn = tk.Button(top_frame, text="Select Folder", command=self.select_folder, font=("Arial", 10), padx=20, pady=5, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    select_btn.pack()
    self.counter_label = tk.Label(self.root, text="0", font=("Arial", 15), pady=10, bg="black", fg="white")
    self.counter_label.pack()
    self.image_frame = tk.Frame(self.root, bg="black", width=900, height=500, highlightbackground="white", highlightthickness=2)
    self.image_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    self.image_frame.pack_propagate(False)
    self.image_label = tk.Label(self.image_frame, bg="black")
    self.image_label.pack(expand=True)
    nav_frame = tk.Frame(self.root, pady=10, bg="black")
    nav_frame.pack()
    self.prev_btn = tk.Button(nav_frame, text="← Prev", command=self.prev_image, font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.prev_btn.grid(row=0, column=0, padx=10)
    self.next_btn = tk.Button(nav_frame, text="Next →", command=self.next_image, font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.next_btn.grid(row=0, column=1, padx=10)
    sort_frame = tk.Frame(self.root, pady=20, bg="black")
    sort_frame.pack()
    self.poor_btn = tk.Button(sort_frame, text="Poor", command=lambda: self.sort_image("poor"), font=("Arial", 15), padx=30, pady=10, state=tk.DISABLED, bg="white", fg="black", highlightbackground="black", highlightthickness=2)
    self.poor_btn.grid(row=0, column=0, padx=15)
    self.good_btn = tk.Button(sort_frame, text="Good", command=lambda: self.sort_image("good"), font=("Arial", 15), padx=30, pady=10, state=tk.DISABLED, bg="white", fg="black", highlightbackground="black", highlightthickness=2)
    self.good_btn.grid(row=0, column=1, padx=15)
    self.best_btn = tk.Button(sort_frame, text="Best", command=lambda: self.sort_image("best"), font=("Arial", 15), padx=30, pady=10, state=tk.DISABLED, bg="white", fg="black", highlightbackground="black", highlightthickness=2)
    self.best_btn.grid(row=0, column=2, padx=15)
    self.root.bind('<KP_1>', lambda e: self.sort_image("poor"))
    self.root.bind('<KP_2>', lambda e: self.sort_image("good"))
    self.root.bind('<KP_3>', lambda e: self.sort_image("best"))
    self.root.bind('<KP_4>', lambda e: self.prev_image())
    self.root.bind('<KP_6>', lambda e: self.next_image())
    self.root.bind('<KP_5>', lambda e: self.open_folder())
  
  def select_folder(self):
    folder = filedialog.askdirectory(title="Select Folder with Images")
    if folder:
      self.source_folder = folder
      self.load_images()
      
  def load_images(self):
    self.image_files = [f for f in os.listdir(self.source_folder) if f.lower().endswith(self.image_extensions)]
    if not self.image_files:
      messagebox.showwarning("No Images", "No supported images found in the selected folder!")
      return
        
    self.image_files.sort()
    self.current_index = 0
    self.poor_folder = os.path.join(self.source_folder, "poor")
    self.good_folder = os.path.join(self.source_folder, "good")
    self.best_folder = os.path.join(self.source_folder, "best")
    os.makedirs(self.poor_folder, exist_ok=True)
    os.makedirs(self.good_folder, exist_ok=True)
    os.makedirs(self.best_folder, exist_ok=True)
    self.prev_btn.config(state=tk.NORMAL)
    self.next_btn.config(state=tk.NORMAL)
    self.poor_btn.config(state=tk.NORMAL)
    self.good_btn.config(state=tk.NORMAL)
    self.best_btn.config(state=tk.NORMAL)
    self.display_image()
    
  def display_image(self):
    if not self.image_files:
      self.counter_label.config(text="All images sorted!")
      self.image_label.config(image="", text="All Done! ✓", font=("Arial", 24), fg="white")
      self.disable_buttons()
      return
    
    self.counter_label.config(text=f"{self.current_index + 1} of {len(self.image_files)}")
    image_path = os.path.join(self.source_folder, self.image_files[self.current_index])
    
    try:
      img = Image.open(image_path)
      self.image_frame.update_idletasks()
      frame_width = self.image_frame.winfo_width() - 20
      frame_height = self.image_frame.winfo_height() - 20
      if frame_width <= 20 or frame_height <= 20:
        frame_width = 880
        frame_height = 480
      
      img.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)
      self.photo = ImageTk.PhotoImage(img)
      self.image_label.config(image=self.photo, text="")
      
    except Exception as e:
      messagebox.showerror("Error", f"Could not load image: {str(e)}")
      
  def sort_image(self, category):
    if not self.image_files:
      return
    
    if category == "poor":
      dest_folder = self.poor_folder
    elif category == "good":
      dest_folder = self.good_folder
    else:
      dest_folder = self.best_folder

    current_file = self.image_files[self.current_index]
    source_path = os.path.join(self.source_folder, current_file)
    dest_path = os.path.join(dest_folder, current_file)
    
    try:
      shutil.move(source_path, dest_path)
      self.image_files.pop(self.current_index)
      if self.current_index >= len(self.image_files) and self.current_index > 0:
        self.current_index -= 1
      
      self.display_image()  
    except Exception as e:
      messagebox.showerror("Error", f"Could not move image: {str(e)}")
      
  def prev_image(self):
    if self.image_files and self.current_index > 0:
      self.current_index -= 1
      self.display_image()
      
  def next_image(self):
    if self.image_files and self.current_index < len(self.image_files) - 1:
      self.current_index += 1
      self.display_image()
  
  def open_folder(self):
    if self.source_folder:
      import subprocess
      import platform
      
      if platform.system() == "Windows":
        os.startfile(self.source_folder)
      elif platform.system() == "Darwin":
        subprocess.Popen(["open", self.source_folder])
      else:
        subprocess.Popen(["xdg-open", self.source_folder])
      
  def disable_buttons(self):
    self.prev_btn.config(state=tk.DISABLED)
    self.next_btn.config(state=tk.DISABLED)
    self.poor_btn.config(state=tk.DISABLED)
    self.good_btn.config(state=tk.DISABLED)
    self.best_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorter(root)
    root.mainloop()