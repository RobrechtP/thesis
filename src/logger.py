import xlsxwriter
import numpy as np
from src.simulator import *
from src.controller import *
from src.pomdp import *
class Logger:

    def __init__(self, filepath, name):
        self.wb = xlsxwriter.Workbook(filepath)
        self.new_sheet(name)
        self.pr_succ = 1
        self.exp = 1


    def new_sheet(self, name):
        self.ws = self.wb.add_worksheet(name)
        self.row = 0
        self.col = 1
        self.ws.write(0,0,"diff_abs")
        self.ws.write(1,0,"diff_sq")
        self.ws.write(2,0,"pr_succ")
        self.ws.write(3,0,"exploration")
        self.ws.write(4,0,"reward")
        self.ws.write(5,0,"path")



    def log_t(self, real_t, estimate_t):
            sum = 0
            for a in range(len(real_t)):
                for s1 in range(len(real_t[a])):
                    for s2 in range(len(real_t[a][s1])):
                        sum += abs(real_t[a][s1][s2] - estimate_t[a][s1][s2])

            self.ws.write_number(self.row, self.col, sum)
            self.ws.write_number(self.row + 1, self.col, self.pr_succ)
            self.col += 1


    def log_all(self, sim, pomdp):
        real_t = sim.get_transition()
        estimate_t = pomdp.pomdpenv.get_transition()
        reward = sim.reward

        #indicates extensded domain (6x6) is being used
        if len(real_t[0] == 27):
            belief = np.zeros(27)
            belief[14] = 1
        else:
            belief = np.zeros(14)
            belief[10] = 1
        action, _er = pomdp.pomdppolicy.get_best_action(belief)

        sum_abs = 0
        sum_sq = 0
        for a in range(len(real_t)):
            for s1 in range(len(real_t[a])):
                for s2 in range(len(real_t[a][s1])):
                    sum_abs += abs(real_t[a][s1][s2] - estimate_t[a][s1][s2])
                    sum_sq += np.power(real_t[a][s1][s2] - estimate_t[a][s1][s2], 2)

        self.ws.write_number(self.row, self.col, sum_abs)
        self.ws.write_number(self.row + 1, self.col, sum_sq)
        self.ws.write_number(self.row + 2, self.col, self.pr_succ)
        self.ws.write_number(self.row + 3, self.col, self.exp)
        self.ws.write_number(self.row + 4, self.col, reward)
        self.ws.write_number(self.row + 5, self.col, int(action))
        self.col += 1


    def log_t_complete(self, real_t, estimate_t):
        ws2 = self.wb.add_worksheet("t_" + str(self.col))
        col = 0
        row = 0
        breadt = len(real_t[0][0])
        for a in range(len(real_t)):
            for s1 in range(len(real_t[a])):
                for s2 in range(len(real_t[a][s1])):
                    ws2.write_number(row, col, real_t[a][s1][s2])
                    ws2.write_number(row, col  + breadt + 2, estimate_t[a][s1][s2])
                    col += 1
                row += 1
                col = 0
            row += 1


    def log_pr_succ(self, pr_succ):
        self.pr_succ = pr_succ*10 #*10 for nice visual

    def log_exploration(self, exp):
        self.exp = exp*10

    def __del__(self):
        self.wb.close()

