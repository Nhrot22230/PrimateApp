from src.classes.filemanager import FileManager
from src.classes.observer import Subject
import tkinter as tk
from tkinter import ttk, messagebox


class FileManagerUI(tk.Frame, Subject):
    def __init__(self, master=None):
        super().__init__(master)
        self.needed_directories = ["audio_files", "models", "reports", "fixed_audio_files"]
        self.audio_files = []
        self.file_manager = FileManager()
        self.observer = None # Observer - Subject pattern
        self.labelFrame = ttk.LabelFrame(self, text="File Manager")
        self.create_widgets()
        self.labelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

    def attach(self, observer):
        self.observer = observer

    def detach(self):
        self.observer = None

    def notify(self, value):
        if self.observer:
            self.observer.updateAudioFile(value)

    def create_widgets(self):
        # Navigation Bar
        navbar = ttk.Frame(self.labelFrame, style="Navbar.TFrame")
        navbar.pack(side=tk.TOP, fill=tk.X)

        style = ttk.Style()
        style.theme_use("clam")  # Choose a ttk theme that suits material design, 'clam' is one example
        # Verify Directories Button
        verify_button = ttk.Button(navbar, text="Verify Directories", command=self.verify_directories, style="Accent.TButton")
        verify_button.pack(side=tk.LEFT)

        # Scan Audio Files Button
        scan_button = ttk.Button(navbar, text="Scan Audio Files", command=self.scan_audio_files, style="Accent.TButton")
        scan_button.pack(side=tk.LEFT)

        # Show Audio Files Button
        show_button = ttk.Button(navbar, text="Show Audio Files", command=self.show_audio_files, style="Accent.TButton")
        show_button.pack(side=tk.LEFT)

        # Audio Files List Box
        self.audio_files_frame = ttk.Frame(self.labelFrame)
        self.audio_files_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def verify_directories(self):
        if self.file_manager.check_directories(self.needed_directories):
            messagebox.showinfo("Verify Directories", "Directories verified successfully")
        else:
            self.file_manager.restore_directories(self.needed_directories)
            messagebox.showinfo("Verify Directories", "Directories restored successfully")

    def scan_audio_files(self):
        self.audio_files.clear()
        temp = self.file_manager.get_files_in_directory("audio_files")
        temp2 = self.file_manager.filter_files_by_extension(temp, ".wav")
        temp2 += self.file_manager.filter_files_by_extension(temp, ".WAV")

        for elem in temp2:
            self.audio_files.append((elem, tk.BooleanVar(value=True)))

        self.update_files_listbox()

    def show_audio_files(self):
        popup_dim = (300, 300)
        popup = tk.Toplevel()
        popup.geometry(f"{popup_dim[0]}x{popup_dim[1]}")
        popup.title("Audio Files")

        for (file, checked) in self.audio_files:
            checkbox = ttk.Checkbutton(popup, text=file, variable=checked)
            checkbox.pack(side=tk.TOP, fill=tk.X, expand=True)

        checkbox_frame = ttk.Frame(popup)
        checkbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        ok_button = ttk.Button(popup, text="OK", command= lambda : {
            self.update_files_listbox(),
            popup.destroy()
            })
        ok_button.pack(side=tk.TOP, fill=tk.X, expand=True)

    def get_selected_audio_files(self):
        return [file for (file, checked) in self.audio_files if checked.get()]
    
    def update_files_listbox(self):
        self.audio_files_frame.destroy()
        self.audio_files_frame = ttk.Frame(self.labelFrame)
        self.audio_files_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(self.audio_files_frame, selectmode=tk.SINGLE)
        listbox.bind("<<ListboxSelect>>", self.onClickListBox)

        for file in self.get_selected_audio_files():
            listbox.insert(tk.END, file)
        listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def onClickListBox(self, event):
        w = event.widget
        if not w.curselection():
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        self.notify(value)
    


