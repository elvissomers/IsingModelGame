import tkinter as tk
import random
from constants import COLOR_YELLOW, COLOR_RED, COLOR_PURPLE, COLOR_BLUE, COLOR_GREEN, COLOR_WHITE

class FireworksAnimation(tk.Canvas):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.particles = []
        self.is_running = True
        
        # After a tiny delay to ensure window is laid out, blast off
        self.after(50, lambda: self.create_explosion(self.winfo_width() / 2, self.winfo_height() / 2))
        self.update_animation()
        
        self.after(3000, self.stop_animation)
        
    def create_explosion(self, center_x, center_y):
        colors = [COLOR_YELLOW, COLOR_RED, COLOR_PURPLE, COLOR_BLUE, COLOR_GREEN, COLOR_WHITE]
        canvas_width = max(self.winfo_width(), 800)
        canvas_height = max(self.winfo_height(), 600)
        
        num_fireworks = 6
        particles_per_firework = 35
        
        for _ in range(num_fireworks):
            explosion_x = random.randint(int(canvas_width*0.2), int(canvas_width*0.8))
            explosion_y = random.randint(int(canvas_height*0.2), int(canvas_height*0.8))
            
            for _ in range(particles_per_firework):
                speed = random.uniform(3, 14)
                size = random.uniform(4, 9)
                color = random.choice(colors)
                
                dx = speed * random.uniform(-1, 1)
                dy = speed * random.uniform(-1, 1)
                
                particle_id = self.create_oval(explosion_x, explosion_y, explosion_x+size, explosion_y+size, fill=color, outline="")
                self.particles.append({"id": particle_id, "dx": dx, "dy": dy, "life": 100})
                
    def update_animation(self):
        if not self.is_running:
            return
            
        to_remove = []
        for p in self.particles:
            pid = p["id"]
            self.move(pid, p["dx"], p["dy"])
            p["dy"] += 0.25 # Gravity
            p["life"] -= 2
            
            if p["life"] <= 0:
                self.delete(pid)
                to_remove.append(p)
                
        for p in to_remove:
            self.particles.remove(p)
            
        if self.is_running:
            self.after(30, self.update_animation)
            
    def stop_animation(self):
        if not self.is_running:
            return
        self.is_running = False
        self.delete("all")
        self.destroy() 
        self.callback()
