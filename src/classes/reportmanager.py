from src.utils.reportutils import generateAnnotationDataFrame
import pandas as pd
import os

class ReportManager:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.filename = "detections.txt"

    def set_filename(self, filename: str):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_output_dir(self, output_dir):
        """
        Set the output directory for saving reports.
        
        Parameters:
            output_dir (str): The output directory path.
        """
        self.output_dir = output_dir

    def generate_report(self, data):
        """
        Generate a report from the input data.
        
        Parameters:
            data (list): List of numbers.
        
        Returns:
            str: The report content.
        """
        df = generateAnnotationDataFrame(data)
        report_path = os.path.join(self.output_dir, self.filename)
        df.to_csv(report_path, index=False, sep="\t")

        return df, report_path
    
    def scan_reports(self):
        """
        Scan the output directory for reports.
        
        Returns:
            list: List of report files.
        """
        return os.listdir(self.output_dir)