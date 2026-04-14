import tkinter as tk
from tkinter import messagebox
from ui.screens import StartMenu, LevelSelectScreen, TutorialScreen
from ui.game_screen import GameScreen
from ui.fireworks import FireworksAnimation
from constants import COLOR_DARK_BLUE

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ising Game UI")
        # Enforce fullscreen requirement
        self.attributes('-fullscreen', True)
        self.configure(bg=COLOR_DARK_BLUE)
        
        self.container = tk.Frame(self, bg=COLOR_DARK_BLUE)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        # Initializing the screens
        for F in (StartMenu, LevelSelectScreen, TutorialScreen, GameScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_frame("StartMenu")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        
        if page_name == "GameScreen":
            frame.start_new_game()
            
        frame.tkraise()
        
    def trigger_fireworks(self):
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        fireworks_canvas = FireworksAnimation(self, callback=self.on_win_complete, width=canvas_width, height=canvas_height, bg=COLOR_DARK_BLUE, highlightthickness=0)
        fireworks_canvas.place(x=0, y=0)
        
    def on_win_complete(self):
        messagebox.showinfo("Winner", "Congratulations, you successfully mapped the couplings!")
        
    def quit_app(self):
        self.destroy()

def start_gui():
    app = App()
    app.mainloop()
