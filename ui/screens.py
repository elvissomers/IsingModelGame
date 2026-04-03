import tkinter as tk
from constants import (
    COLOR_DARK_BLUE, COLOR_LIGHT_GRAY, COLOR_BLUE, COLOR_DARK_BLUE_HOVER,
    COLOR_ORANGE, COLOR_ORANGE_HOVER, COLOR_RED, COLOR_RED_HOVER,
    COLOR_GRAY, COLOR_GRAY_HOVER, TUTORIAL_TEXT
)

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
        
        top_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        top_frame.pack(fill="x", padx=20, pady=20)
        
        quit_btn = tk.Button(top_frame, text="Quit Application", command=controller.quit_app, font=("Arial", 16), bg=COLOR_RED, fg="white", relief="flat", padx=10, pady=5)
        quit_btn.pack(side="left")
        
        back_btn = tk.Button(top_frame, text="Back to Menu", command=lambda: controller.show_frame("StartMenu"), font=("Arial", 16), bg=COLOR_GRAY, fg="white", relief="flat", padx=10, pady=5)
        back_btn.pack(side="right")
        
        title = tk.Label(self, text="Tutorial", font=("Arial", 48, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
        title.pack(pady=(50, 20))
        
        content = tk.Label(self, text=TUTORIAL_TEXT, font=("Arial", 22), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY, justify="left")
        content.pack(pady=30, padx=40)
