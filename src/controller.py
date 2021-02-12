from src.pomdp import *
from src.solverAdapter import *
from src.simulator import *


import numpy as np


class Controller:
    """
    attributes:
        pomdp: POMDP instance (containing current transition function estimate T)
        sim: simulation
        weight: constant used for weighting recent action-observations
        hist: history: list of (belief_state b, action_num a, observation_num z)
        exp: amount of exploration (1 = always random action, 0 = always best action)
        nactions: aantal actions
    """

    def __init__(self, pomdp, sim, weight, exploration):
        self.pomdp = pomdp
        self.sim = sim
        self.weight = weight
        self.hist = []
        self.exp = exploration
        self.nactions = len(pomdp.pomdpenv.actions) #todo: logger meegeven die gecalled wordt bij elke method call

    def step(self):
        belief = self.pomdp.belief
        if np.random.random() < self.exp:   #exploration: choose random action
            action_num = np.random.randint(self.nactions)
        else:                               #exploitation: choose best action
            action_num, expected_reward = self.pomdp.get_best_action()
        obs = self.sim.step(int(action_num))
        self.pomdp.update_belief(int(action_num), obs)
        self.hist.append((belief, int(action_num), obs))

    def update(self):
        #calc most likely transition function given history
        print("todo update")

    def print_summary(self):
        print("---Controller summary---")
        print("history: ", self.hist)
        print("T:", self.pomdp.pomdpenv.T)
        print("action history:", [self.pomdp.pomdpenv.actions[x[1]] for x in self.hist])
        print("------------------------")





