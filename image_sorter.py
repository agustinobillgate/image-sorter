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
    self.photo = None
    self.poor_folder = ""
    self.good_folder = ""
    self.best_folder = ""
    self.undo_stack = []
    self.current_sort = "name"
    self.sort_ascending = True
    self.setup_ui()
    self.root.update_idletasks()

  def setup_ui(self):
    top_frame = tk.Frame(self.root, pady=10, bg="black")
    top_frame.pack(fill=tk.X)
    select_btn = tk.Button(top_frame, text="Select Folder", command=self.select_folder, font=("Arial", 10), padx=20, pady=5, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    select_btn.pack()
    sort_control_frame = tk.Frame(self.root, pady=10, bg="black")
    sort_control_frame.pack()
    self.sort_name_btn = tk.Button(sort_control_frame, text="Name", command=lambda: self.sort_images("name"), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.sort_name_btn.grid(row=0, column=1, padx=10)
    self.sort_type_btn = tk.Button(sort_control_frame, text="Type", command=lambda: self.sort_images("type"), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.sort_type_btn.grid(row=0, column=2, padx=10)
    self.sort_date_btn = tk.Button(sort_control_frame, text="Date", command=lambda: self.sort_images("date"), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.sort_date_btn.grid(row=0, column=3, padx=10)
    self.sort_asc_btn = tk.Button(sort_control_frame, text="↑ Asc", command=lambda: self.set_sort_order(True), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="lightgray", fg="black", highlightbackground="white", highlightthickness=2)
    self.sort_asc_btn.grid(row=0, column=5, padx=10)
    self.sort_desc_btn = tk.Button(sort_control_frame, text="Dsc ↓", command=lambda: self.set_sort_order(False), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.sort_desc_btn.grid(row=0, column=6, padx=10)
    self.counter_label = tk.Label(self.root, text="0", font=("Arial", 10), pady=5, bg="black", fg="white")
    self.counter_label.pack()
    self.filename_label = tk.Label(self.root, text="", font=("Arial", 10), pady=5, bg="black", fg="white")
    self.filename_label.pack()
    self.image_frame = tk.Frame(self.root, bg="black", width=1000, height=500, highlightbackground="white", highlightthickness=2)
    self.image_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    self.image_frame.pack_propagate(False)
    self.image_label = tk.Label(self.image_frame, bg="black")
    self.image_label.pack(expand=True)
    nav_frame = tk.Frame(self.root, pady=10, bg="black")
    nav_frame.pack()
    self.prev_btn = tk.Button(nav_frame, text="Prev", command=self.prev_image, font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.prev_btn.grid(row=0, column=0, padx=10)
    self.undo_btn = tk.Button(nav_frame, text="Undo", command=self.undo_image, font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.undo_btn.grid(row=0, column=1, padx=10)
    self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_image, font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="white", highlightthickness=2)
    self.next_btn.grid(row=0, column=2, padx=10)
    sort_frame = tk.Frame(self.root, pady=10, bg="black")
    sort_frame.pack()
    self.poor_btn = tk.Button(sort_frame, text="Poor", command=lambda: self.sort_image("poor"), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="black", highlightthickness=2)
    self.poor_btn.grid(row=0, column=0, padx=10)
    self.good_btn = tk.Button(sort_frame, text="Good", command=lambda: self.sort_image("good"), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="black", highlightthickness=2)
    self.good_btn.grid(row=0, column=1, padx=10)
    self.best_btn = tk.Button(sort_frame, text="Best", command=lambda: self.sort_image("best"), font=("Arial", 10), padx=20, pady=5, state=tk.DISABLED, bg="white", fg="black", highlightbackground="black", highlightthickness=2)
    self.best_btn.grid(row=0, column=2, padx=10)
    self.root.bind('<Left>', lambda e: self.prev_image())
    self.root.bind('<Right>', lambda e: self.next_image())
    self.root.bind('1', lambda e: self.sort_image("poor"))
    self.root.bind('2', lambda e: self.sort_image("good"))
    self.root.bind('3', lambda e: self.sort_image("best"))
    self.root.bind('u', lambda e: self.undo_image())

    try:
      self.root.bind('<KP_1>', lambda e: self.sort_image("poor"))
      self.root.bind('<KP_2>', lambda e: self.sort_image("good"))
      self.root.bind('<KP_3>', lambda e: self.sort_image("best"))
      self.root.bind('<KP_4>', lambda e: self.prev_image())
      self.root.bind('<KP_6>', lambda e: self.next_image())
      self.root.bind('<KP_5>', lambda e: self.open_folder())
    except:
      pass

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

    self.apply_current_sort()
    self.current_index = 0
    self.undo_stack = []
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
    self.sort_name_btn.config(state=tk.NORMAL)
    self.sort_type_btn.config(state=tk.NORMAL)
    self.sort_date_btn.config(state=tk.NORMAL)
    self.sort_asc_btn.config(state=tk.NORMAL)
    self.sort_desc_btn.config(state=tk.NORMAL)
    self.update_sort_button_highlight()
    self.display_image()

  def sort_images(self, sort_by):
    if not self.image_files:
      return
    
    self.current_sort = sort_by
    self.apply_current_sort()
    self.current_index = 0
    self.update_sort_button_highlight()
    self.display_image()

  def set_sort_order(self, ascending):
    if not self.image_files:
      return
    
    self.sort_ascending = ascending
    self.apply_current_sort()
    self.current_index = 0
    self.update_sort_order_buttons()
    self.display_image()

  def apply_current_sort(self):
    if self.current_sort == "name":
      self.image_files.sort(reverse=not self.sort_ascending)
    elif self.current_sort == "type":
      self.image_files.sort(key=lambda x: (os.path.splitext(x)[1].lower(), x.lower()), reverse=not self.sort_ascending)
    elif self.current_sort == "date":
      self.image_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.source_folder, x)), reverse=not self.sort_ascending)

  def update_sort_button_highlight(self):
    # Reset all sort buttons
    self.sort_name_btn.config(bg="white", highlightbackground="white")
    self.sort_type_btn.config(bg="white", highlightbackground="white")
    self.sort_date_btn.config(bg="white", highlightbackground="white")
    
    if self.current_sort == "name":
      self.sort_name_btn.config(bg="lightgray", highlightbackground="lightgray")
    elif self.current_sort == "type":
      self.sort_type_btn.config(bg="lightgray", highlightbackground="lightgray")
    elif self.current_sort == "date":
      self.sort_date_btn.config(bg="lightgray", highlightbackground="lightgray")
    
    self.update_sort_order_buttons()

  def update_sort_order_buttons(self):
    if self.sort_ascending:
      self.sort_asc_btn.config(bg="lightgray", highlightbackground="lightgray")
      self.sort_desc_btn.config(bg="white", highlightbackground="white")
    else:
      self.sort_asc_btn.config(bg="white", highlightbackground="white")
      self.sort_desc_btn.config(bg="lightgray", highlightbackground="lightgray")

  def display_image(self):
    if not self.image_files:
      self.counter_label.config(text="All images sorted!")
      self.filename_label.config(text="")
      self.image_label.config(image="", text="All Done! ✓", font=("Arial", 24), fg="white")
      self.disable_buttons()
      return

    current_file = self.image_files[self.current_index]
    self.counter_label.config(text=f"{self.current_index + 1} of {len(self.image_files)}")
    self.filename_label.config(text=f"{current_file}")
    image_path = os.path.join(self.source_folder, current_file)
    
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
      self.undo_stack.append({
        'file': current_file,
        'from': self.source_folder,
        'to': dest_folder,
        'index': self.current_index
      })
      self.undo_btn.config(state=tk.NORMAL)
      self.image_files.pop(self.current_index)
      if self.current_index >= len(self.image_files) and self.current_index > 0:
        self.current_index -= 1
      
      self.display_image()
    except Exception as e:
      messagebox.showerror("Error", f"Could not move image: {str(e)}")

  def undo_image(self):
    if not self.undo_stack:
      return
    
    last_action = self.undo_stack.pop()
    
    try:
      source_path = os.path.join(last_action['to'], last_action['file'])
      dest_path = os.path.join(last_action['from'], last_action['file'])
      shutil.move(source_path, dest_path)
      self.image_files.insert(last_action['index'], last_action['file'])
      self.current_index = last_action['index']
      if not self.undo_stack:
        self.undo_btn.config(state=tk.DISABLED)
      
      self.display_image()
      
    except Exception as e:
      messagebox.showerror("Error", f"Could not undo: {str(e)}")

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
    self.undo_btn.config(state=tk.DISABLED)
    self.poor_btn.config(state=tk.DISABLED)
    self.good_btn.config(state=tk.DISABLED)
    self.best_btn.config(state=tk.DISABLED)
    self.sort_name_btn.config(state=tk.DISABLED)
    self.sort_type_btn.config(state=tk.DISABLED)
    self.sort_date_btn.config(state=tk.DISABLED)
    self.sort_asc_btn.config(state=tk.DISABLED)
    self.sort_desc_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorter(root)
    root.mainloop()

# pyinstaller --onefile --noconsole --name ImageSorter image_sorter.py --icon=cross.ico