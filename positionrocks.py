import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import os

class Rock:
    def __init__(self, image_path, canvas):
        self.original_image = Image.open(image_path).convert("RGBA")
        self.angle = 0
        self.x, self.y = 100, 100
        self.canvas = canvas
        self.tk_image = None
        self.image_id = None
        self.slider = None
        self.resized_image = self.original_image

    def resize(self, factor):
        w, h = self.original_image.size
        new_size = (max(1, int(w * factor)), max(1, int(h * factor)))
        self.resized_image = self.original_image.resize(new_size, Image.LANCZOS)

    def draw(self):
        rotated = self.resized_image.rotate(self.angle, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated)
        if self.image_id:
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    def rotate(self, angle):
        self.angle = angle
        self.draw()


class RockComposer:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Composer")

        self.canvas_width = 1000
        self.canvas_height = 800
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rock_list = []
        self.selected_rock = None

        self.toolbar = tk.Frame(root)
        self.toolbar.pack()

        tk.Button(self.toolbar, text="Add Rock", command=self.add_rock).pack(side=tk.LEFT, padx=5)
        tk.Button(self.toolbar, text="Export PNG", command=self.export_image).pack(side=tk.LEFT, padx=5)

        self.canvas.bind("<Button-1>", self.select_rock)
        self.canvas.bind("<B1-Motion>", self.drag_rock)

    def add_rock(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if not path:
            return

        rock = Rock(path, self.canvas)
        self.rock_list.append(rock)

        # Compute scale factor: shrink as more rocks are added
        n = len(self.rock_list)
        factor = max(0.2, 1.0 - 0.08 * (n - 1))

        # Resize and redraw all rocks with new scale
        for r in self.rock_list:
            r.resize(factor)
            r.draw()

        # Add a rotation slider for this rock
        slider = tk.Scale(self.toolbar, from_=0, to=360, orient=tk.HORIZONTAL,
                          label=f"Rotate Rock {n}",
                          command=lambda val, r=rock: r.rotate(int(val)))
        slider.pack(side=tk.LEFT, padx=5)
        rock.slider = slider

    def select_rock(self, event):
        for rock in reversed(self.rock_list):  # topmost rock first
            bbox = self.canvas.bbox(rock.image_id)
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.selected_rock = rock
                self.last_x = event.x
                self.last_y = event.y
                break

    def drag_rock(self, event):
        if self.selected_rock:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.selected_rock.move(dx, dy)
            self.last_x = event.x
            self.last_y = event.y

    def export_image(self):
        final = Image.new("RGBA", (self.canvas_width, self.canvas_height), (255, 255, 255, 0))
        for rock in self.rock_list:
            rotated = rock.resized_image.rotate(rock.angle, expand=True)
            final.paste(rotated, (rock.x, rock.y), rotated)
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if save_path:
            final.save(save_path)
            print(f"✅ Saved composition to {save_path}")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = RockComposer(root)
    root.mainloop()
