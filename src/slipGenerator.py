import numpy as np
from src.simulator import *
from src.controller import *
from src.pomdp import *


class RainGenerator:

    def __init__(self, dry_slip = 0.95, wet_slip = 0.65):
        self.dry_slip = dry_slip
        self.wet_slip = wet_slip

        self.data = []
        self.end_curr_show = 0
        self.end_curr_dry = 0
        self.start_next_show = 0
        self.end_next_show = 0
        self.end_next_dry = 0

    def step(self, cont, i):
        # start a shower
        if i == self.start_next_show:
            self.end_curr_show = self.end_next_show
            self.end_curr_dry = self.end_next_dry
            if len(self.data) > 2:
                self.start_next_show = self.data.pop(0)
                self.end_next_show = self.data.pop(0)
                self.end_next_dry = self.data.pop(0)
            cont.set_sim_slip(self.wet_slip)


        #if currently drying decrease slip every 100 steps
        if i%100 == 0 and self.end_curr_show < i < self.end_curr_dry:
            slip = self.wet_slip + (self.dry_slip - self.wet_slip) * (i - self.end_curr_show)/(self.end_curr_dry - self.end_curr_show)
            cont.set_sim_slip(slip)

        if i == self.end_curr_dry:
            cont.set_sim_slip(self.dry_slip)

    def generate_data(self, p_shower=1/7000, min_length_shower=1000,
                         max_length_shower=5000, min_length_drying = 3000, max_length_drying = 5000, length = 500000 ):
        data = []
        end_show = 0
        end_dry = 0

        for i in range(length):
            if end_show < i and np.random.random() < p_shower:
                end_show = np.random.randint(i + min_length_shower, i + max_length_shower)
                end_dry = np.random.randint(end_show + min_length_drying, end_show + max_length_drying)
                data = data + [i, end_show, end_dry]

        return data

    def set_data(self, data):
        self.data = data
        self.start_next_show = self.data.pop(0)
        self.end_next_show = self.data.pop(0)
        self.end_next_dry = self.data.pop(0)

    def save_data(self, data, filepath):
        file = open(filepath, 'w')
        data = [str(i) + "\n" for i in data]
        file.writelines(data)
        file.close()

    def load_data(self, filepath):
        file = open(filepath, 'r')
        lines = file.readlines()
        data = [int(i) for i in lines]
        self.set_data(data)
        return data







    #todo: optioneel methode toeveogen die een voorbeeld plot


