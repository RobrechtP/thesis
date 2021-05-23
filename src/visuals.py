import tkinter as tk
from PIL import Image, ImageTk
from src.pomdp import *
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.slipGenerator import *
from src.solverAdapter import *


#The demo!



test_policy = POMDPPolicy("../output/6x6MDP_est.alpha")
test_policy2 = POMDPPolicy("../output/6x6MDP.alpha")
slip_gen = RainGenerator()
slip_gen.load_data("../transitions/rain1.txt")
transition_data = slip_gen.get_datapoints_clustered(300000)
transition_data = [1-x for x in transition_data]






def t_sim_hellinger( t1, t2, sums):

    sum = 0
    for i in range(len(t1)):
        for j in range(len(t1[i])):
            hell = 1 - np.sqrt( np.power((np.sqrt(t1[i][j]) - np.sqrt(t2[i][j])), 2).sum())/np.sqrt(2) #1 - helling distance for each action-state pair
            sum = sum + sums[i][j]*hell
    #print(sum)
    return sum

def calculate_t(hist, weights):
    t = np.zeros((4, 27, 27))
    for i in range(len(hist)):
        t  = t + weights[i]*hist[i]

    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j].sum() == 0: #if unseen set all to one to normalize to random
                t[i][j] = np.ones(len(t[i][j]))
            t[i][j] = t[i][j]/t[i][j].sum()
    return t



def calculate_sim(history, weight):
    '''
    calc most likely transition function t given history
    t = nparray met elke entry: (a, s, s')
    '''
    nstates = 27
    t_recent_counts = history[0][-1].copy()


    sums = np.zeros((4, nstates)) #indicate for each state-action pair how many times the actions was recently taken in the states
    #normalize
    t_recent = t_recent_counts.copy()
    for i in range(len(t_recent)):
        for j in range(len(t_recent[i])):
            sum = t_recent[i][j].sum()
            sums[i][j] = sum
            if sum == 0: #if unseen set all to one to normalize to random
                t_recent[i][j] = np.ones(len(t_recent[i][j]))
            t_recent[i][j] = t_recent[i][j]/t_recent[i][j].sum()


    t = t_recent_counts.copy()

    #alternative impl: first get al sims and reorder on similarity to weight them
    w = 1
    sims = []
    for cluster in history[1][:-1]:
        sims.append(w * t_sim_hellinger(t_recent,cluster,sums))


    #flip sims since we looped in reverse
    sims = np.flip(np.array(sims))
    #get sort indices
    inds = np.argsort(sims)
    # print("at step: " + str(len(sims)))
    # print(inds)
    weights = np.zeros(len(history[0])-1)
    w = 1
    for ind in reversed(inds):
        weights[ind]=w
        t = t + w * history[0][ind]
        w = w*weight

    weights = np.flip(weights)

    #BASELINE CODE:
    #   for cluster in reversed(self.hist_c):
    #       t = t + w * cluster[0]
    #       w = w*weight

    #normalize
    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j].sum() == 0: #if unseen set all to one to normalize to random
                t[i][j] = np.ones(len(t[i][j]))
            t[i][j] = t[i][j]/t[i][j].sum()


    return weights, t






demo_data = np.load("data_rain1.npy")
hist_test = [demo_data[0][:374] + demo_data[0][500], demo_data[1][:374] + demo_data[1][500]]
w, _t = calculate_sim(hist_test, 0.97)

test_data = w




class BarFrame(tk.Frame):
    def __init__(self, parent, data):
        tk.Frame.__init__(self, parent)
        self.size = (10,3)
        self.data=data
        fig = Figure(figsize=self.size, dpi=100)
        ax = fig.add_axes([0.05,0.1,0.95,0.9])
        ax.set_ylim(0,1.05)
        ax.plot([0,377],[1,0], color = 'k',label='exploration')
        ax.plot(data, color = 'r', label='P(slip)')
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




    def set_data(self, data, position = 500):

        self.canvas.get_tk_widget().destroy()

        fig = Figure(figsize=self.size, dpi=100)

        ax = fig.add_axes([0.05,0.1,0.95,0.9])
        ax.set_ylim(0,1.05)

        if len(data) > 0:
            ax.bar(list(range(len(data))), data, color = 'b', width = 1, label='Weights')
        ax.axvline(x=position, color = 'r')
        ax.plot([0,377],[1,0], color = 'k', label='Exploration')
        ax.plot(self.data, color ='r',label='P(slip)')
        ax.legend()


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
        white = Image.new('RGB', (0,0), (255,255,255,0))
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

        self.rain_colors = ["#ffffff", "#e6e6ff", "#ccccff", "#b3b3ff", "#9999ff", "#8080ff", "#6666ff" ]


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
                    label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}",image=self.white, width = grid_size, height = grid_size, bg="white" )

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

        next_button = tk.Button(text="Enter", master=self.master_frames[3])
        next_button.bind("<Button-1>", self.set_position)
        self.button1 = tk.Button(text="uniform", master=self.master_frames[3])
        self.button1.bind("<Button-1>", self.set_uniform_weights)
        self.button2 = tk.Button(text="recent", master=self.master_frames[3])
        self.button2.bind("<Button-1>", self.set_recent_weights)
        self.button3 = tk.Button(text="similarity", master=self.master_frames[3])
        self.button3.bind("<Button-1>", self.set_sim_weights)

        self.button_color = self.button1.cget("background")
        self.toggle_color = 'grey'

        self.pos_input = tk.Entry(master=self.master_frames[3])



        self.bar_frame = BarFrame(self.master_frames[2], transition_data)

        tk.Label(master=self.master_frames[0], text="calculated policy").pack(side=tk.TOP)
        tk.Label(master=self.master_frames[1], text="optimal policy").pack()

        dom_frame1.pack(side=tk.LEFT)
        dom_frame2.pack(side=tk.RIGHT)
        self.bar_frame.pack()
        self.pos_input.pack(side=tk.LEFT)
        next_button.pack(side=tk.LEFT)
        self.button1.pack(side=tk.LEFT)
        self.button2.pack(side=tk.LEFT)
        self.button3.pack(side=tk.LEFT)


        self.set_rain_bg(0.05)
        self.pos = 500
        self.window.mainloop()





    def set_rain_bg(self, slip):
        intensity = int(slip*20 - 1)
        for dom in range(2):
            for i,tile in enumerate(self.tiles[dom]):
                if i not in self.blank_tiles + self.reward_tiles:
                    tile.config( bg = self.rain_colors[intensity])

    def set_empty(self, dom = 0):
        nstates = 27
        for i in range(nstates):
            if i not in self.reward_tiles:
                self.tiles[dom][i].config(image = self.white)

    def set_policy(self, policy, dom = 0):
        nstates = 27
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
        self.button1.config(background=self.toggle_color)
        self.button2.config(background=self.button_color)
        self.button3.config(background=self.button_color)

        w = np.ones(750)
        w[self.pos::] = np.zeros(750-self.pos)

        t = calculate_t(demo_data[0],w)
        self.bar_frame.set_data(w, self.pos)
        self.set_transition(t)

    def set_recent_weights(self, event):
        self.button1.config(background=self.button_color)
        self.button2.config(background=self.toggle_color)
        self.button3.config(background=self.button_color)
        pos = self.pos
        w = np.zeros(750)
        val = 1
        for i in range(pos):
            w[-(750-pos)-i] = val
            val = val*0.8187

        t = calculate_t(demo_data[0],w)
        self.bar_frame.set_data(w, pos)
        self.set_transition(t)

    def set_sim_weights(self, event):
        self.button1.config(background=self.button_color)
        self.button2.config(background=self.button_color)
        self.button3.config(background=self.toggle_color)

        pos = self.pos
        print(pos)
        hist = [np.concatenate((demo_data[0][:min(375,pos)], [demo_data[0][pos]])), (demo_data[1][:min(375,pos)])]
        print(len(hist[0]))
        w, t = calculate_sim(hist, 0.97)
        t = demo_data[1][pos] #use exisiting data because of bug in calc_sim
        self.bar_frame.set_data(w,pos)
        self.set_transition(t)


    def set_position(self, event):
        self.button1.config(background=self.button_color)
        self.button2.config(background=self.button_color)
        self.button3.config(background=self.button_color)
        pos = int(self.pos_input.get())
        self.pos = pos
        self.bar_frame.set_data([], pos)
        slip = transition_data[pos]
        self.set_rain_bg(slip)
        self.set_slip(slip)
        self.set_empty(0)

    def set_slip(self, slip):
        dom = "6x6MDP"
        write_transitions("../domains/" + dom + ".POMDP", 1-slip, extension=True)
        solve(dom + '.POMDP')
        pol = POMDPPolicy("../output/" + dom + ".alpha")
        self.set_policy(pol,1)

    def set_transition(self, t):
        dom = "6x6MDP_est"
        write_t(dom + ".POMDP", t)
        solve(dom + '.POMDP')
        pol = POMDPPolicy("../output/" + dom + ".alpha")
        self.set_policy(pol,0)




gui = DemoGUI()