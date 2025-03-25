import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResourceAllocationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphical Simulator for Resource Allocation")
        self.root.geometry("1400x800")
        self.root.configure(bg="#2c3e50")

        self.processes = set()
        self.resources = {}
        self.edges = set()
        self.deadlock_nodes = set()
        self.deadlock_edges = set() 

        heading_label = tk.Label(root, text="Graphical Simulator for Resource Allocation", font=("Arial", 18, "bold"),
                                 fg="white", bg="#34495e", padx=10, pady=10)
        heading_label.pack(fill=tk.X)

        self.graph_frame = tk.Frame(root, bg="#ecf0f1", bd=2, relief=tk.RIDGE)
        self.graph_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(root, bg="#bdc3c7", bd=2, relief=tk.RIDGE)
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

        self.figure, self.ax = plt.subplots(figsize=(8, 6))  # Was (6, 5)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Expand canvas fully



        self.create_controls()

    def create_controls(self):
        ttk.Label(self.control_frame, text="Process Name:", font=("Arial", 14, "bold"), background="#bdc3c7").grid(row=0, column=0, sticky="w", pady=5)
        self.process_entry = ttk.Entry(self.control_frame, width=20)
        self.process_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.control_frame, text="Resource Name:", font=("Arial", 14, "bold"), background="#bdc3c7").grid(row=1, column=0, sticky="w", pady=5)
        self.resource_entry = ttk.Entry(self.control_frame, width=20)
        self.resource_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self.control_frame, text="Instances:", font=("Arial", 14, "bold"), background="#bdc3c7").grid(row=2, column=0, sticky="w", pady=5)
        self.instance_entry = ttk.Entry(self.control_frame, width=10)
        self.instance_entry.grid(row=2, column=1, pady=5, padx=5)
        self.instance_entry.insert(0, "1")  # Default value

        # Frame to Hold Process & Resource Details
        self.details_frame = tk.Frame(root, bg="#ecf0f1", bd=2, relief=tk.RIDGE)
        self.details_frame.pack(fill=tk.X, padx=20, pady=10)

        # Processes List (Stacked First)
        ttk.Label(self.details_frame, text="Processes:", font=("Arial", 12, "bold"), background="#ecf0f1").pack(anchor="w", padx=10, pady=(5, 0))
        self.process_listbox = tk.Listbox(self.details_frame, height=5, width=80)
        self.process_listbox.pack(fill=tk.X, padx=10, pady=5)

        # Resources List (Stacked Below)
        ttk.Label(self.details_frame, text="Resources (Instances):", font=("Arial", 12, "bold"), background="#ecf0f1").pack(anchor="w", padx=10, pady=(10, 0))
        self.resource_listbox = tk.Listbox(self.details_frame, height=5, width=80)
        self.resource_listbox.pack(fill=tk.X, padx=10, pady=5)


        buttons = [
            ("Add Process", self.add_process),
            ("Add Resource", self.add_resource),
            ("Request Resource", self.request_resource),
            ("Allocate Resource", self.allocate_resource),
            ("Detect Deadlock", self.detect_deadlock),
            ("Reset Graph", self.reset_graph)
        ]

        for i, (text, command) in enumerate(buttons, start=2):
            btn = ttk.Button(self.control_frame, text=text, command=command, style="TButton")
            btn.grid(row=i + 2, column=0, columnspan=2, pady=10, padx=10, ipadx=10, ipady=5)
        # Deadlock Example Buttons Section
        
        
        # Frame to Hold Deadlock Example Buttons (Placed Below Details)
        self.example_frame = tk.Frame(root, bg="#ecf0f1", bd=2, relief=tk.RIDGE)
        self.example_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(self.example_frame, text="Load Examples:", font=("Arial", 14, "bold"), background="#ecf0f1").pack(anchor="w", padx=10, pady=5)

        example_buttons = [
            ("Deadlock 1", self.load_deadlock_1),
            ("Deadlock 2", self.load_deadlock_2),
            ("Deadlock 3", self.load_deadlock_3),
        ]

        for text, command in example_buttons:
            btn = ttk.Button(self.example_frame, text=text, command=command, style="TButton")
            btn.pack(fill=tk.X, padx=10, pady=5)



        self.style_buttons()

    def load_deadlock_1(self):
        self.reset_graph()
    
        # Processes & Resources
        self.processes = {"P1", "P2"}
        self.resources = {"R1": 1, "R2": 1}
        
        # Update Listboxes
        self.process_listbox.delete(0, tk.END)
        self.resource_listbox.delete(0, tk.END)
        for p in self.processes:
            self.process_listbox.insert(tk.END, p)
        for r, i in self.resources.items():
            self.resource_listbox.insert(tk.END, f"{r} ({i})")
        
        # Requests & Allocations to Form Deadlock
        self.edges = {("P1", "R1"), ("P2", "R2"), ("R1", "P2"), ("R2", "P1")}
        
        self.update_graph()
        messagebox.showinfo("Example Loaded", "Deadlock Example 1 Loaded!")

    def load_deadlock_2(self):
        self.reset_graph()
        
        # Processes & Resources
        self.processes = {"P1", "P2", "P3"}
        self.resources = {"R1": 1, "R2": 1, "R3": 1}
        
        # Update Listboxes
        self.process_listbox.delete(0, tk.END)
        self.resource_listbox.delete(0, tk.END)
        for p in self.processes:
            self.process_listbox.insert(tk.END, p)
        for r, i in self.resources.items():
            self.resource_listbox.insert(tk.END, f"{r} ({i})")
        
        # Requests & Allocations to Form Deadlock
        self.edges = {("P1", "R1"), ("P2", "R2"), ("P3", "R3"), ("R1", "P2"), ("R2", "P3"), ("R3", "P1")}
        
        self.update_graph()
        messagebox.showinfo("Example Loaded", "Deadlock Example 2 Loaded!")

    def load_deadlock_3(self):
        self.reset_graph()
        
        # Processes & Resources (Multiple Instances)
        self.processes = {"P1", "P2", "P3", "P4"}
        self.resources = {"R1": 2, "R2": 2, "R3": 1, "R4": 1}  # ✅ Multiple instances for R1 & R2
        
        # Update Listboxes
        self.process_listbox.delete(0, tk.END)
        self.resource_listbox.delete(0, tk.END)
        for p in self.processes:
            self.process_listbox.insert(tk.END, p)
        for r, i in self.resources.items():
            self.resource_listbox.insert(tk.END, f"{r} ({i})")
        
        # Requests & Allocations (Deadlock Formed)
        self.edges = {("P1", "R1"), ("P2", "R2"), ("P3", "R3"), ("P4", "R4"),
                    ("R1", "P2"), ("R2", "P3"), ("R3", "P4"), ("R4", "P1")}  # Circular wait

        self.update_graph()
        messagebox.showinfo("Example Loaded", "Deadlock Example 3 (Multiple Instances) Loaded!")


    def style_buttons(self):
        style = ttk.Style()
        style.configure("TButton",
                        font=("Arial", 12, "bold"),  # Bigger font
                        padding=10,
                        background="#3498db",  # Default blue color
                        foreground="black",
                        borderwidth=2)

        style.map("TButton",
                background=[("active", "#2980b9"), ("disabled", "#bdc3c7")],  # Darker on hover
                foreground=[("disabled", "#7f8c8d")])


    # def update_status(self, message):
    #     self.status_label.config(text=f"Status: {message}")

    def add_process(self):
        process = self.process_entry.get().strip()
        if process and process not in self.processes:
            self.processes.add(process)
            self.process_listbox.insert(tk.END, process)  # ✅ Update listbox
            self.update_graph()
            # self.update_status(f"Added process {process}")
        self.process_entry.delete(0, tk.END)


    def add_resource(self):
        resource = self.resource_entry.get().strip()
        instances = self.instance_entry.get().strip()

        if resource and resource not in self.resources:
            try:
                instances = max(1, int(instances))  # Ensure at least 1 instance
                self.resources[resource] = instances  
                self.resource_listbox.insert(tk.END, f"{resource} ({instances})")  # ✅ Update listbox
                self.update_graph()
                # self.update_status(f"Added resource {resource} with {instances} instances")
            except ValueError:
                messagebox.showerror("Invalid Input", "Instances must be a number.")
        
        self.resource_entry.delete(0, tk.END)
        self.instance_entry.delete(0, tk.END)
        self.instance_entry.insert(0, "1")  # Reset to default



    def request_resource(self):
        process = self.process_entry.get().strip()
        resource = self.resource_entry.get().strip()
        instances_input = self.instance_entry.get().strip()

        if not process or not resource:
            messagebox.showwarning("Invalid Input", "Please enter both a process and a resource.")
            return

        # Automatically add process if it doesn't exist
        if process not in self.processes:
            self.processes.add(process)
            self.process_listbox.insert(tk.END, process)

        # Automatically add resource if it doesn't exist, using instance entry
        if resource not in self.resources:
            try:
                instances = max(1, int(instances_input))  # Ensure at least 1 instance
            except ValueError:
                instances = 1  # Default to 1 if invalid or empty
            self.resources[resource] = instances
            self.resource_listbox.insert(tk.END, f"{resource} ({instances})")

        # Add the request edge
        self.edges.add((process, resource))
        self.update_graph()

        # Clear entries (but keep instance default at 1)
        self.process_entry.delete(0, tk.END)
        self.resource_entry.delete(0, tk.END)
        # Reset instance entry to default value
        self.instance_entry.delete(0, tk.END)
        self.instance_entry.insert(0, "1")

    def allocate_resource(self):
        process = self.process_entry.get().strip()
        resource = self.resource_entry.get().strip()
        instances_input = self.instance_entry.get().strip()

        if not process or not resource:
            messagebox.showwarning("Invalid Input", "Please enter both a process and a resource.")
            return

        # Automatically add process if it doesn't exist
        if process not in self.processes:
            self.processes.add(process)
            self.process_listbox.insert(tk.END, process)

        # Automatically add resource if it doesn't exist, using instance entry
        if resource not in self.resources:
            try:
                instances = max(1, int(instances_input))  # Ensure at least 1 instance
            except ValueError:
                instances = 1  # Default to 1 if invalid or empty
            self.resources[resource] = instances
            self.resource_listbox.insert(tk.END, f"{resource} ({instances})")

        # Add the allocation edge
        self.edges.add((resource, process))
        self.update_graph()

        # Clear entries (but keep instance default at 1)
        self.process_entry.delete(0, tk.END)
        self.resource_entry.delete(0, tk.END)
        # Reset instance entry to default value
        self.instance_entry.delete(0, tk.END)
        self.instance_entry.insert(0, "1")

    def detect_deadlock(self):
        graph = nx.DiGraph()
        graph.add_edges_from(self.edges)

        try:
            cycle = nx.find_cycle(graph, orientation='original')
            self.deadlock_nodes = {node for edge in cycle for node in edge}
            self.deadlock_edges = set((u, v) for u, v, _ in cycle)  # Store edges without orientation
            self.update_graph()

            # Build the cycle as an ordered sequence of nodes
            cycle_path = [edge[0] for edge in cycle] + [cycle[-1][1]]  # Start nodes + final target
            cycle_nodes = " → ".join(cycle_path)
            messagebox.showwarning("Deadlock Detected", f"Cycle Found: {cycle_nodes}")
        except nx.NetworkXNoCycle:
            self.deadlock_nodes.clear()
            self.deadlock_edges.clear()
            messagebox.showinfo("No Deadlock", "No deadlock detected!")




    def reset_graph(self):
        self.processes.clear()
        self.resources.clear()
        self.edges.clear()
        self.deadlock_nodes.clear()

        self.process_listbox.delete(0, tk.END)
        self.resource_listbox.delete(0, tk.END)

        self.update_graph()
        # self.update_status("Graph reset")

    def update_graph(self):
        self.ax.clear()
        G = nx.DiGraph()
        G.add_edges_from(self.edges)

        pos = {}  # Position dictionary for nodes
        process_x, resource_x = -1.5, 1.5
        process_y, resource_y = 1.0, 1.0
        spacing_y = 1.0  # More spacing to prevent overlap

        # Assign positions for processes (stacked vertically)
        for i, process in enumerate(self.processes):
            pos[process] = (process_x, process_y - i * spacing_y)

        # Assign positions for resources (stacked vertically)
        for i, resource in enumerate(self.resources):
            pos[resource] = (resource_x, resource_y - i * spacing_y)

        # Draw nodes with deadlock indication
        for node in G.nodes:
            x, y = pos[node]
            color = "#e74c3c" if node in self.deadlock_nodes else ("blue" if node in self.processes else "green")
            edge_color = "black" if node not in self.deadlock_nodes else "red"

            if node in self.processes:
                self.ax.scatter(x, y, s=900, c=color, edgecolors=edge_color)
                self.ax.text(x, y, node, fontsize=14, fontweight="bold", ha='center', va='center', color="white")
            elif node in self.resources:
                instances = self.resources[node]
                
                rect_width = 0.3 + (0.07 * instances)
                rect_height = 0.2
                rect = plt.Rectangle((x - rect_width / 2, y - rect_height / 2), rect_width, rect_height, fc=color, edgecolor=edge_color, lw=2)

                self.ax.add_patch(rect)

                for i in range(instances):
                    self.ax.scatter(x - (rect_width / 2) + (i * (rect_width / instances)) + 0.06, y, s=70, c="white", edgecolors="black")

                self.ax.text(x, y + 0.15, node, fontsize=14, fontweight="bold", ha='center', va='bottom', color="black")

        # Draw edges (Highlight Deadlock Edges)
        for edge in G.edges:
            start, end = edge
            color = "red" if edge in self.deadlock_edges else "black"
            lw = 3 if edge in self.deadlock_edges else 2

            self.ax.annotate("", xy=pos[end], xytext=pos[start],
                            arrowprops=dict(arrowstyle="->", color=color, lw=lw))

        # Set axes limits with padding to avoid clipping
        if pos:  # Only set limits if there are nodes
            x_coords = [p[0] for p in pos.values()]
            y_coords = [p[1] for p in pos.values()]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            # Add padding (adjust based on circle size; 0.5 is roughly half the circle diameter in data units)
            padding = 0.5
            self.ax.set_xlim(x_min - padding, x_max + padding)
            self.ax.set_ylim(y_min - padding, y_max + padding)

        # Keep equal aspect ratio
        self.ax.set_aspect('equal')

        # Remove axis
        self.ax.set_frame_on(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.axis("off")

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceAllocationSimulator(root)
    root.mainloop()
