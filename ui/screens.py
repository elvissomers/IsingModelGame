import tkinter as tk
from constants import (
    COLOR_DARK_BLUE, COLOR_LIGHT_GRAY, COLOR_BLUE, COLOR_DARK_BLUE_HOVER,
    COLOR_ORANGE, COLOR_ORANGE_HOVER, COLOR_RED, COLOR_RED_HOVER,
    COLOR_GRAY, COLOR_GRAY_HOVER
)
import json
import os
from ui.spin_grid import SpinGridCanvas

class StartMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_DARK_BLUE)
        self.controller = controller
        
        center_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Ising Game", font=("Arial", 64, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
        title.pack(pady=(0, 50))
        
        start_btn = tk.Button(center_frame, text="Start New Game", command=lambda: controller.show_frame("LevelSelectScreen"), font=("Arial", 24), bg=COLOR_BLUE, fg="white", activebackground=COLOR_DARK_BLUE_HOVER, relief="flat", padx=20, pady=10, width=15)
        start_btn.pack(pady=15)
        
        tutorial_btn = tk.Button(center_frame, text="Tutorial", command=lambda: controller.show_frame("TutorialScreen"), font=("Arial", 24), bg=COLOR_ORANGE, fg="white", activebackground=COLOR_ORANGE_HOVER, relief="flat", padx=20, pady=10, width=15)
        tutorial_btn.pack(pady=15)
        
        quit_btn = tk.Button(center_frame, text="Quit Game", command=controller.quit_app, font=("Arial", 24), bg=COLOR_RED, fg="white", activebackground=COLOR_RED_HOVER, relief="flat", padx=20, pady=10, width=15)
        quit_btn.pack(pady=15)

class LevelSelectScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_DARK_BLUE)
        self.controller = controller
        
        center_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Select Difficulty", font=("Arial", 48, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
        title.pack(pady=(0, 40))
        
        levels = [
            ("Level 0 (1x3)", 1, 3),
            ("Level 1 (2x2)", 2, 2),
            ("Level 2 (3x2)", 3, 2),
            ("Level 3 (3x3)", 3, 3)
        ]
        
        for name, h, w in levels:
            btn = tk.Button(center_frame, text=name, 
                            command=lambda height=h, width=w: self.start_level(height, width), 
                            font=("Arial", 20), bg=COLOR_BLUE, fg="white", 
                            activebackground=COLOR_DARK_BLUE_HOVER, relief="flat", padx=20, pady=10, width=15)
            btn.pack(pady=10)
            
        back_btn = tk.Button(center_frame, text="Back", command=lambda: controller.show_frame("StartMenu"), font=("Arial", 20), bg=COLOR_GRAY, fg="white", activebackground=COLOR_GRAY_HOVER, relief="flat", padx=20, pady=10, width=15)
        back_btn.pack(pady=(30,0))
        
    def start_level(self, height, width):
        self.controller.frames["GameScreen"].set_dimensions(height, width)
        self.controller.show_frame("GameScreen")

class TutorialScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_DARK_BLUE)
        self.controller = controller
        self.current_page = 0
        
        # Load tutorial contents
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "..", "assets", "tutorial.json")
        try:
            with open(json_path, "r") as f:
                self.pages = json.load(f)
        except Exception as e:
            print(f"Error loading tutorial: {e}")
            self.pages = [{"text": "Error loading tutorial.", "grids": []}]
            
        top_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        top_frame.pack(fill="x", padx=20, pady=20)
        
        quit_btn = tk.Button(top_frame, text="Quit Application", command=controller.quit_app, font=("Arial", 16), bg=COLOR_RED, fg="white", relief="flat", padx=10, pady=5)
        quit_btn.pack(side="left")
        
        back_btn = tk.Button(top_frame, text="Back to Menu", command=lambda: controller.show_frame("StartMenu"), font=("Arial", 16), bg=COLOR_GRAY, fg="white", relief="flat", padx=10, pady=5)
        back_btn.pack(side="right")
        
        title = tk.Label(self, text="Tutorial", font=("Arial", 48, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
        title.pack(pady=(10, 10))
        
        self.content_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        nav_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        nav_frame.pack(fill="x", pady=20)
        
        self.prev_btn = tk.Button(nav_frame, text="◀ Previous", command=self.prev_page, font=("Arial", 18), bg=COLOR_BLUE, fg="white", activebackground=COLOR_DARK_BLUE_HOVER, relief="flat", padx=20, pady=10, width=12)
        self.prev_btn.pack(side="left", padx=50)
        
        self.page_label = tk.Label(nav_frame, text="", font=("Arial", 18), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
        self.page_label.pack(side="left", expand=True)
        
        self.next_btn = tk.Button(nav_frame, text="Next ▶", command=self.next_page, font=("Arial", 18), bg=COLOR_BLUE, fg="white", activebackground=COLOR_DARK_BLUE_HOVER, relief="flat", padx=20, pady=10, width=12)
        self.next_btn.pack(side="right", padx=50)
        
        self.render_page()
        
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()
            
    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.render_page()
            
    def render_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        page = self.pages[self.current_page]
        
        text_label = tk.Label(self.content_frame, text=page["text"], font=("Arial", 22), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY, justify="left", wraplength=1000)
        text_label.pack(pady=(0, 20))
        
        grids_frame = tk.Frame(self.content_frame, bg=COLOR_DARK_BLUE)
        grids_frame.pack(pady=10)
        
        for grid_data in page.get("grids", []):
            item_frame = tk.Frame(grids_frame, bg=COLOR_DARK_BLUE)
            item_frame.pack(side="left", padx=30)
            
            spin_canvas = SpinGridCanvas(
                item_frame, 
                mode=grid_data["mode"], 
                height_cells=grid_data["height"], 
                width_cells=grid_data["width"]
            )
            spin_canvas.spins = grid_data["spins"]
            spin_canvas.couplings = grid_data["couplings"]
            spin_canvas.draw_grid()
            spin_canvas.pack()
            
            if grid_data.get("label"):
                label = tk.Label(item_frame, text=grid_data["label"], font=("Arial", 16, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
                label.pack(pady=10)
                
        # Update navigation
        self.prev_btn["state"] = tk.NORMAL if self.current_page > 0 else tk.DISABLED
        self.prev_btn["bg"] = COLOR_BLUE if self.current_page > 0 else COLOR_GRAY
        
        self.next_btn["state"] = tk.NORMAL if self.current_page < len(self.pages) - 1 else tk.DISABLED
        self.next_btn["bg"] = COLOR_BLUE if self.current_page < len(self.pages) - 1 else COLOR_GRAY
        
        self.page_label["text"] = f"Page {self.current_page + 1} of {len(self.pages)}"
