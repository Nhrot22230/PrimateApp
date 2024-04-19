from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

class MatplotlibCanvasManager:
    def __init__(self, master):
        self.master = master
        self.canvas = {}

    def add_plot(self, fig_id, plot_func, *args):
        fig, ax = plot_func(*args)
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X)
        self.canvas[fig_id] = (fig, canvas)
        return canvas

    def get_plot(self, fig_id):
        try:
            self.canvas[fig_id]
            return self.canvas[fig_id]
        except KeyError:
            return None

    def clear_plots(self):
        for fig, canvas in self.canvas.values():
            canvas.get_tk_widget().destroy()
            plt.close(fig)
        self.canvas = {}

    def remove_plot(self, fig_id):
        fig, canvas = self.canvas.pop(fig_id)
        canvas.get_tk_widget().destroy()
        plt.close(fig)