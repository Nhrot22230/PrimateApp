from src.classes.observer import Subject
from src.classes.modelmanager import ModelManager
import tkinter as tk
from tkinter import ttk, messagebox

class ModelManagerUI(tk.Frame, Subject):
    def __init__(self, master=None):
        super().__init__(master)
        self.model_manager = ModelManager("models")
        self.file = None
        self.model_name = tk.StringVar()
        self.model_names_list = None
        self.labelFrame = ttk.LabelFrame(self, text="Model Manager")
        self.create_widgets()
        self.labelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def detach(self):
        self.observer = None

    def attach(self, observer):
        self.observer = observer

    def notify(self, value):
        if self.observer:
            self.observer.updateResults(value)

    def set_file(self, file):
        self.file = file

    def create_widgets(self):
        # Navigation Bar
        navbar = ttk.Frame(self.labelFrame, style="Navbar.TFrame")
        navbar.pack(side=tk.TOP, fill=tk.X)

        # Configure ttk style
        style = ttk.Style()
        style.theme_use("clam")  # Use a ttk theme suitable for Material Design, 'clam' is just an example

        # Scan Models Button
        scan_models_button = ttk.Button(navbar, text="Scan Models", command=self.scan_models, style="Accent.TButton")
        scan_models_button.pack(side=tk.LEFT)

        # Load Model Button
        load_model_button = ttk.Button(navbar, text="Load Model", command=self.load_model, style="Accent.TButton")
        load_model_button.pack(side=tk.LEFT)

        # Predict Button
        predict_button = ttk.Button(navbar, text="Predict", command=self.predict, style="Accent.TButton")
        predict_button.pack(side=tk.LEFT)

        # Model Selection Radio Buttons
        self.model_selection_frame = tk.Frame(self.labelFrame)

        # Model Info Frame
        self.model_info_frame = ttk.LabelFrame(self.labelFrame, text="Model Info")


    def scan_models(self):
        self.model_names_list = self.model_manager.scan_models()
        if self.model_names_list is None:
            messagebox.showerror("Error", "No models found")
            return
        self.show_model_names()

    def show_model_names(self):
        if self.model_names_list is None:
            messagebox.showerror("Error", "No models scanned")
            return
        
        self.model_selection_frame.destroy()
        self.model_selection_frame = tk.Frame(self.labelFrame)
        self.model_selection_frame.pack(side=tk.TOP)

        for model_name in self.model_names_list:
            model_name_radio = tk.Radiobutton(self.model_selection_frame, text=model_name, variable=self.model_name, value=model_name)
            model_name_radio.pack(side=tk.TOP)
    
    def show_model_info(self):
        model_name = self.get_selected_model_name()
        model_info = self.model_manager.get_model_info(model_name)

        self.model_info_frame.destroy()
        self.model_info_frame = ttk.LabelFrame(self.labelFrame, text="Model Info")
        self.model_info_frame.pack(side=tk.TOP)

        model_info_text = tk.Text(self.model_info_frame, height=10, width=70, wrap="word")
        model_info_text.insert("1.0", model_info)
        model_info_text.pack(side=tk.TOP)


    def get_selected_model_name(self):
        return self.model_name.get()
    
    def load_model(self):
        if self.model_name.get() == "":
            messagebox.showerror("Error", "No model selected")
            return True
        
        try:
            model_name = self.get_selected_model_name()
            self.model_manager.load_model(model_name)
            messagebox.showinfo("Load Model", f"Model {model_name} loaded successfully")
            self.show_model_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {str(e)}")

    def verifyData(self):
        if self.model_name.get() == "":
            messagebox.showerror("Error", "No model selected")
            return True

        if self.model_manager.get_model(self.model_name.get()) is None:
            messagebox.showerror("Error", "Model not loaded")
            return True

        if self.file is None:
            messagebox.showerror("Error", "No file selected")
            return True
        
        return False

    def predict(self):
        if self.verifyData():
            return

        try:
            model_name = self.get_selected_model_name()
            results = self.model_manager.predict(model_name, self.file)
            self.notify(results)
            messagebox.showinfo("Predict", "Prediction results displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict: {str(e)}")

