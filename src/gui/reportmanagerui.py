from src.classes.observer import Subject
from src.classes.reportmanager import ReportManager
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

class ReportManagerUI(tk.Frame, Subject):
    def __init__(self, parent, output_dir: str):
        super().__init__(parent)
        self.report_manager = ReportManager(output_dir)
        self.labelFrame = ttk.LabelFrame(self, text="Report Manager")
        self.create_widgets()
        self.labelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.data = None

    def setfilename(self, filename: str):
        self.report_manager.set_filename(filename)

    def attach(self, observer):
        self.observer = observer

    def detach(self):
        self.observer = None

    def notify(self, df):
        if self.observer:
            self.observer.updateReport(df)

    def set_data(self, data):
        self.data = data

    def create_widgets(self):
        # Navigation Bar
        navbar = ttk.Frame(self.labelFrame, style="Navbar.TFrame")
        navbar.pack(side=tk.TOP, fill=tk.X)
        
        scan_button = ttk.Button(navbar, text="Scan Reports", command=self.scan_reports)
        scan_button.pack(side=tk.LEFT)
        
        generate_button = ttk.Button(navbar, text="Generate Report", command=self.generate_report)
        generate_button.pack(side=tk.LEFT)
        
        self.reportListBox = ttk.Combobox(self.labelFrame, state="readonly")

    def verifyErrors(self, df):
        if df.empty:
            messagebox.showerror("Error", "No data to generate report")
            return True
        return False

    def generate_report(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to generate report")
            return
        
        df, report_path = self.report_manager.generate_report(self.data)

        if self.verifyErrors(df):
            return

        messagebox.showinfo("Success", f"Report generated at {report_path}")
        self.notify(df)


    def show_report(self, df: pd.DataFrame, title=None):
        popup = tk.Toplevel()
        popup.title("Report")
        popup.geometry("400x400")
        report_frame = tk.Frame(popup)

        if title is None:
            title = self.report_manager.get_filename()

        if title is None:
            title = "Generated Report"
        else:
            title = f"{title[:-4]} Report"
        
        report_frame_title = ttk.Label(report_frame, text=title, font=("Helvetica", 16))
        report_frame_title.pack(side=tk.TOP)

        tree = ttk.Treeview(report_frame, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=20)

        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

        tree.pack(side=tk.TOP, fill=tk.X, expand=True)
        
        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(side=tk.BOTTOM)
        report_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def scan_reports(self):
        self.reportListBox.destroy()
        self.reportListBox = ttk.Combobox(self.labelFrame, state="readonly")
        self.reportListBox.pack(side=tk.LEFT)
        
        reports = self.report_manager.scan_reports()
        if not reports:
            return
        
        self.reportListBox["values"] = reports
        self.reportListBox.bind("<<ComboboxSelected>>", self.load_report)

    def load_report(self, event):
        report_name = self.reportListBox.get()
        df = pd.read_csv(f"{self.report_manager.output_dir}/{report_name}", sep="\t")
        self.show_report(df, title=report_name)