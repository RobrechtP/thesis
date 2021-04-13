import tkinter as tk
from PIL import Image, ImageTk


class DemoGUI():
    def __init__(self):
        grid_size = 100
        self.window = tk.Tk()

        black = Image.new('RGB', (grid_size,grid_size))
        white = Image.new('RGB', (grid_size,grid_size), (255,255,255))
        right = Image.open("../images/arrow_right.png")
        right = right.convert('RGBA')
        right = right.resize((50,50))
        up = right.rotate(90)
        left = up.rotate(90)
        down = left.rotate(90)

        self.white = ImageTk.PhotoImage(white)
        self.black = ImageTk.PhotoImage(black)
        self.arrows = []
        self.arrows.append(ImageTk.PhotoImage(up))
        self.arrows.append(ImageTk.PhotoImage(down))
        self.arrows.append(ImageTk.PhotoImage(right))
        self.arrows.append(ImageTk.PhotoImage(left))


        self.rain_colors = ["#ffffff", "#e6e6ff", "#ccccff", "#b3b3ff", "#9999ff", "#8080ff" ]


        dom_frame = tk.Frame()
        self.tiles = []
        for i in range(4):
            for j in range(4):
                frame = tk.Frame(
                    master=dom_frame,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j)
                label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}", image=self.arrows[0], width = grid_size, height = grid_size, bg="white" )

                if j == 1 and (i == 1 or i == 2):
                    label.config(image=self.black)
                else:
                    self.tiles.append(label)
                label.pack()

        next_button = tk.Button(text="next")
        next_button.bind("<Button-1>", self.next)


        dom_frame.pack()
        next_button.pack()

        self.window.mainloop()

    def next(self, event):
        print("next called")
        self.tiles[0].config(image = self.arrows[1])

        self.set_rain_bg(4)

    def set_rain_bg(self, intensity):
        for tile in self.tiles:
            tile.config( bg = self.rain_colors[intensity])


gui = DemoGUI()