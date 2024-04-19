import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from src.gui.filemanui import FileManagerUI
from src.gui.canvasmanagerui import CanvasManagerUI
from src.gui.modelmanagerui import ModelManagerUI
from src.gui.reportmanagerui import ReportManagerUI


class MainWindow(ThemedTk):
    def __init__(self):
        super().__init__(theme="arc")
        self.title("Audio File Manager")
        self.geometry("1080x720")

        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame = ttk.Labelframe(self, text="Output Frame")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.file_manager = FileManagerUI(self.left_frame)
        self.file_manager.attach(self)
        self.file_manager.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.model_manager = ModelManagerUI(self.left_frame)
        self.model_manager.attach(self)
        self.model_manager.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas_manager = CanvasManagerUI(self.left_frame, output_frame=self.main_frame)
        self.canvas_manager.set_audio_dir("audio_files")
        self.canvas_manager.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.reportmanager = ReportManagerUI(self.left_frame, "reports")
        self.reportmanager.attach(self)
        self.reportmanager.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.autoScan()

    def autoScan(self):
        self.file_manager.verify_directories()
        self.file_manager.scan_audio_files()
        self.model_manager.scan_models()

    def updateAudioFile(self, value):
        self.canvas_manager.set_file(value)
        self.canvas_manager.plot_spectrogram()
        self.model_manager.set_file("audio_files/" + value)
        self.reportmanager.setfilename(value[:-4] + ".txt")

    def updateResults(self, value):
        self.canvas_manager.set_results(value)
        self.reportmanager.set_data(value)
        
    def updateReport(self, df):
        self.reportmanager.show_report(df)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()