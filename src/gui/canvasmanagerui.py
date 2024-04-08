import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from src.classes.canvasmanager import MatplotlibCanvasManager
from src.utils.plotutils import createSpectrogram, createPredictionPlot

class CanvasManagerUI(ttk.Frame):
    def __init__(self, master, output_frame=None):
        super().__init__(master)
        self.master = master
        self.canvas_manager = MatplotlibCanvasManager(output_frame)
        self.file = None
        self.audio_dir = None
        self.results = None
        self.labelFrame = ttk.LabelFrame(self, text="Canvas Manager")
        self.create_widgets()
        self.labelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

    def set_file(self, file):
        self.file = file

    def set_audio_dir(self, audio_dir):
        self.audio_dir = audio_dir

    def set_results(self, results):
        self.results = results

    def create_widgets(self):
        self.create_buttons()

    def create_buttons(self):
        # Navigation Bar
        navbar = ttk.Frame(self.labelFrame, style="Navbar.TFrame")
        navbar.pack(side=tk.TOP, fill=tk.X)

        style = ttk.Style()
        style.theme_use("clam")  # Choose a ttk theme that suits material design, 'clam' is one example

        spectrogram_button = ttk.Button(navbar, text="Plot Spectrogram", command=self.plot_spectrogram, style="Accent.TButton")
        spectrogram_button.pack(side=tk.LEFT)

        prediction_button = ttk.Button(navbar, text="Plot Prediction", command=self.plot_prediction, style="Accent.TButton")
        prediction_button.pack(side=tk.LEFT)

    def plot_spectrogram(self):
        if self.file is None:
            messagebox.showerror("Error", "No file selected")
            return
        if self.audio_dir is None:
            messagebox.showerror("Error", "No audio directory selected")
            return
        
        if self.canvas_manager.get_plot("spectrogram") is not None:
            self.canvas_manager.remove_plot("spectrogram")
        
        self.canvas_manager.add_plot("spectrogram", createSpectrogram, self.file, self.audio_dir)

    def plot_prediction(self):
        if self.results is None:
            messagebox.showerror("Error", "No prediction results")
            return
        if self.file is None:
            messagebox.showerror("Error", "No file selected")
            return
        
        if self.canvas_manager.get_plot("prediction") is not None:
            self.canvas_manager.remove_plot("prediction")
        
        self.canvas_manager.add_plot("prediction", createPredictionPlot, self.results, self.file)
    
    