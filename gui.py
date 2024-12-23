import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from false_position import FalsePosition

class FalsePositionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("False Position Method Calculator")
        
        # Initialize solver
        self.solver = FalsePosition()
        
        # Create main frames
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.output_frame = ttk.Frame(root, padding="10")
        self.output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_input_widgets()
        self.create_output_widgets()
        
        # Initialize plot
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        
        
     
    def create_input_widgets(self):
        # Expression input
        ttk.Label(self.input_frame, text="Expression (use 'x' as variable):").grid(row=0, column=0, sticky=tk.W)
        self.expr_var = tk.StringVar()
        self.expr_entry = ttk.Entry(self.input_frame, textvariable=self.expr_var, width=30)
        self.expr_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Interval inputs
        ttk.Label(self.input_frame, text="Lower bound:").grid(row=1, column=0, sticky=tk.W)
        self.lower_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.lower_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Upper bound:").grid(row=2, column=0, sticky=tk.W)
        self.upper_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.upper_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Calculate button
        ttk.Button(self.input_frame, text="Calculate", command=self.calculate).grid(row=3, column=0, pady=10)
        
    def create_output_widgets(self):
        self.output_text = tk.Text(self.output_frame, height=15, width=50)
        self.output_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.output_text['yscrollcommand'] = scrollbar.set
        
    def iteration_callback(self, iteration, c, fc):
        """Callback function to receive iteration updates"""
        self.output_text.insert(tk.END, f"Iteration {iteration}:\n")
        self.output_text.insert(tk.END, f"c = {c:.{self.solver.PRECISION}f}\n")
        self.output_text.insert(tk.END, f"f(c) = {fc:.{self.solver.PRECISION}f}\n\n")
        
    def plot_function(self, a, b, root=None):
        self.ax.clear()
        
        try:
            x, y = self.solver.get_plot_points(a, b)
            self.ax.plot(x, y, 'b-', label='f(x)')
            self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            self.ax.grid(True, alpha=0.3)
            
            if root is not None:
                self.ax.plot([root], [0], 'ro', label='Root')
                
            self.ax.legend()
            self.ax.set_title('Function Plot')
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Error plotting function: {str(e)}")
        
    def calculate(self):
        try:
            # Clear previous output
            self.output_text.delete(1.0, tk.END)
            
            # Set expression
            self.solver.set_expression(self.expr_var.get())
            
            # Get input values
            a = float(self.lower_var.get())
            b = float(self.upper_var.get())
            
            # Check if workable
            workability = self.solver.is_workable(a, b)
            
            self.output_text.insert(tk.END, "Checking if function is workable...\n")
            self.output_text.insert(tk.END, f"Continuous: {workability['continuous']}\n")
            self.output_text.insert(tk.END, f"Unequal signs: {workability['unequal_signs']}\n")
            self.output_text.insert(tk.END, f"Number of roots: {workability['num_roots']}\n\n")
            
            if not workability['workable']:
                self.output_text.insert(tk.END, "Function is not workable for false position method.\n")
                return
                
            # Solve using false position method
            self.output_text.insert(tk.END, "Starting False Position Method...\n")
            result = self.solver.solve(a, b, callback=self.iteration_callback)
            
            # Display results
            self.output_text.insert(tk.END, "\nResults:\n")
            self.output_text.insert(tk.END, f"Root = {result['root']:.{self.solver.PRECISION}f}\n")
            self.output_text.insert(tk.END, f"f(root) = {result['f_root']:.{self.solver.PRECISION}f}\n")
            self.output_text.insert(tk.END, f"Number of iterations: {result['iterations']}\n")
            
            # Plot the function
            self.plot_function(a, b, result['root'])
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FalsePositionGUI(root)
    root.mainloop()
