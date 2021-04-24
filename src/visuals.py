import tkinter as tk
from PIL import Image, ImageTk
from src.pomdp import *
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.slipGenerator import *

test_policy = POMDPPolicy("../output/6x6MDP_est.alpha")
test_policy2 = POMDPPolicy("../output/6x6MDP.alpha")
slip_gen = RainGenerator()
slip_gen.load_data("../transitions/rain1.txt")
transition_data = slip_gen.get_datapoints_clustered(300000)
transition_data = [1-x for x in transition_data]


test_data = np.random.random(750)
test_data[500::] = np.zeros(250)




class BarFrame(tk.Frame):
    def __init__(self, parent, data):
        tk.Frame.__init__(self, parent)
        self.size = (10,3)
        self.data=data
        fig = Figure(figsize=self.size, dpi=100)
        ax = fig.add_axes([0.05,0.1,0.95,0.9])
        ax.plot(data, color = 'r')

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




    def set_data(self, data, position = 500):

        self.canvas.get_tk_widget().destroy()

        fig = Figure(figsize=self.size, dpi=100)

        ax = fig.add_axes([0.05,0.1,0.95,0.9])


        ax.bar(list(range(len(data))), data, color = 'b', width = 1)
        ax.axvline(x=position, color = 'r')
        ax.plot()
        ax.plot(self.data, color ='r')

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



class DemoGUI():
    def __init__(self):
        grid_size = 50
        arrow_size = 25
        path_color = (128,0,0)

        self.walls = [(1,2), (1,4),(2,2),(2,4),(3,4),(4,1),(4,2),(4,3),(4,4)]
        self.reward_tiles = [2,7,11]
        self.blank_tiles = [17,18,20,24,25,26]
        self.paths = [[14,10,6,0,1],[14,19,21,22,23,24,25,26,20,18,13,9,5,4,3],[14,15,16,17,12,8,3],[]]


        self.window = tk.Tk()
        self.window.title("Masters thesis demo")

        black = Image.new('RGB', (grid_size,grid_size))
        white = Image.new('RGB', (grid_size,grid_size), (255,255,255))
        right = Image.open("../images/arrow_right.png")
        right = right.convert('RGBA')
        right = right.resize((arrow_size,arrow_size))
        up = right.rotate(90)
        left = up.rotate(90)
        down = left.rotate(90)
        plusone = Image.open("../images/plus1.png")
        minone = Image.open("../images/min1.png")
        mintwo = Image.open("../images/min2.png")


        data = np.array(up)
        data[..., :-1][True] = path_color
        up_path = Image.fromarray(data)
        data = np.array(down)
        data[..., :-1][True] = path_color
        down_path = Image.fromarray(data)
        data = np.array(left)
        data[..., :-1][True] = path_color
        left_path = Image.fromarray(data)
        data = np.array(right)
        data[..., :-1][True] = path_color
        right_path = Image.fromarray(data)

        self.white = ImageTk.PhotoImage(white)
        self.black = ImageTk.PhotoImage(black)
        self.arrows = []
        self.arrows.append(ImageTk.PhotoImage(up))
        self.arrows.append(ImageTk.PhotoImage(down))
        self.arrows.append(ImageTk.PhotoImage(right))
        self.arrows.append(ImageTk.PhotoImage(left))
        self.arrows_path = []
        self.arrows_path.append(ImageTk.PhotoImage(up_path))
        self.arrows_path.append(ImageTk.PhotoImage(down_path))
        self.arrows_path.append(ImageTk.PhotoImage(right_path))
        self.arrows_path.append(ImageTk.PhotoImage(left_path))
        self.plusone = ImageTk.PhotoImage(plusone)
        self.minone = ImageTk.PhotoImage(minone)
        self.mintwo = ImageTk.PhotoImage(mintwo)

        self.rain_colors = ["#ffffff", "#e6e6ff", "#ccccff", "#b3b3ff", "#9999ff", "#8080ff" ]


        self.master_frames = []
        temp = []
        for i in range(2):
            frame = tk.Frame(
                master=self.window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=0, column=i)
            for i in range(2):
                frame2 = tk.Frame(
                    master=frame,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame2.grid(row=i, column=0)
                self.master_frames.append(frame2)



        dom_frame1 = tk.Frame(master=self.master_frames[0])
        dom_frame2 = tk.Frame(master=self.master_frames[1])
        dom_frames = [dom_frame1, dom_frame2]

        self.tiles = [[],[]]

        for domain in range(2):
            for i in range(6):
                for j in range(6):
                    frame = tk.Frame(
                        master=dom_frames[domain],
                        relief=tk.RAISED,
                        borderwidth=1
                    )
                    frame.grid(row=i, column=j)
                    label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}",image=self.arrows[0], width = grid_size, height = grid_size, bg="white" )

                    if i == 0 and j == 2:
                        label.config(image = self.plusone)

                    if i == 1 and j == 1:
                        label.config(image = self.minone)

                    if i == 2 and j == 1:
                        label.config(image = self.mintwo)


                    if (i,j) in self.walls:
                        label.config(image=self.black)
                    else:

                        self.tiles[domain].append(label)


                    label.pack()

        next_button = tk.Button(text="next", master=self.master_frames[3])
        next_button.bind("<Button-1>", self.next)
        button1 = tk.Button(text="uniform", master=self.master_frames[3])
        button1.bind("<Button-1>", self.set_uniform_weights)
        button2 = tk.Button(text="recent", master=self.master_frames[3])
        button2.bind("<Button-1>", self.set_recent_weights)
        button3 = tk.Button(text="similarity", master=self.master_frames[3])
        button3.bind("<Button-1>", self.next)

        self.bar_frame = BarFrame(self.master_frames[2], transition_data)

        tk.Label(master=self.master_frames[0], text="calculated policy").pack(side=tk.TOP)
        tk.Label(master=self.master_frames[1], text="optimal policy").pack()

        dom_frame1.pack(side=tk.LEFT)
        dom_frame2.pack(side=tk.RIGHT)
        self.bar_frame.pack()
        next_button.pack(side=tk.LEFT)
        button1.pack(side=tk.LEFT)
        button2.pack(side=tk.LEFT)
        button3.pack(side=tk.LEFT)

        self.set_random()
        self.set_rain_bg(0)

        self.window.mainloop()

    def next(self, event):
        print("next called")
        self.bar_frame.set_data(test_data)

        self.set_policy(test_policy)
        self.set_policy(test_policy2,1)
        self.set_rain_bg(4)


    def set_rain_bg(self, intensity):
        for dom in range(2):
            for i,tile in enumerate(self.tiles[dom]):
                if i not in self.blank_tiles + self.reward_tiles:
                    tile.config( bg = self.rain_colors[intensity])

    def set_policy(self, policy, dom = 0):
        nstates = len(self.tiles[dom])
        belief = np.zeros(nstates)
        belief[14] = 1
        action, _er = policy.get_best_action(belief)
        path = self.paths[int(action)]
        for i in range(nstates):
            if i not in self.reward_tiles:
                belief = np.zeros(nstates)
                belief[i] = 1
                action, _er = policy.get_best_action(belief)
                if i in path:
                    self.tiles[dom][i].config(image = self.arrows_path[int(action)])
                else:
                    self.tiles[dom][i].config(image = self.arrows[int(action)])

    def set_random(self, dom=0):
        for i,tile in enumerate(self.tiles[dom]):
            if i not in self.reward_tiles:
                tile.config(image=self.arrows[np.random.randint(4)])

    def set_uniform_weights(self, event):
        data = np.ones(750)
        data[500::] = np.zeros(250)
        self.bar_frame.set_data(data)

    def set_recent_weights(self, event):
        pos = 500
        data = np.zeros(750)
        val = 1
        for i in range(pos):
            data[-(750-pos)-i] = val
            val = val*0.8187
        self.bar_frame.set_data(data)

gui = DemoGUI()