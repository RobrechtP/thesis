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
        hist: history: list of (belief_state b, action_num a, observation_num z) todo: z wordt nooit gebruikt!
        exp: amount of exploration (1 = always random action, 0 = always best action)
        nactions: aantal actions
    """

    #set extension to true in case extended 6x6 domain is used, then pr_dry also is used
    def __init__(self, pomdp, sim, weight, exploration, logger, extension=False, pr_dry = 0.95):
        self.pomdp = pomdp
        self.sim = sim
        self.weight = weight
        self.hist = []
        self.exp = exploration
        self.nactions = len(pomdp.pomdpenv.actions) #todo: logger meegeven die gecalled wordt bij elke method call
        self.logger = logger
        self.extension = extension
        self.pr_dry = pr_dry
        logger.log_exploration(exploration)



    def step(self):
        belief = self.pomdp.belief
        if np.random.random() < self.exp:   #exploration: choose random action
            action_num = np.random.randint(self.nactions)
        else:                               #exploitation: choose best action
            action_num, expected_reward = self.pomdp.get_best_action()
        obs = self.sim.step(int(action_num))
        self.pomdp.update_belief(int(action_num), obs)
        self.hist.append((belief, int(action_num), obs))
        #todo: log

    def update(self):
        '''
        calc most likely transition function t given history
        t = nparray met elke entry: (a, s, s')
        '''
        nstates = len(self.pomdp.pomdpenv.states)
        t = np.zeros((self.nactions, nstates, nstates))
        w = 1
        b = self.pomdp.belief
        for step in reversed(self.hist):
            counts = np.outer(step[0], b) #calc outer product of b(s) and b(s') (product van elke combinatie)
            t[step[1]] += w*counts        #add these counts to the corresponding action
            b = step[0]                   #set b(s') to current for next iter
            w = w*self.weight             #decrease weight

        #normalize
        for i in range(len(t)):
            for j in range(len(t[i])):
                if t[i][j].sum() == 0: #if unseen set all to one to normalize to random
                    t[i][j] = np.ones(len(t[i][j]))
                t[i][j] = t[i][j]/t[i][j].sum()

        #set transition function in pomdp env
        self.pomdp.pomdpenv.set_transition(t)
        #self.logger.log_t(self.sim.get_transition(), t)


    def log(self):
        self.logger.log_all(self.sim, self.pomdp)

    def log_t_complete(self):
        self.logger.log_t_complete(self.sim.get_transition(), self.pomdp.pomdpenv.get_transition())

    def set_sim_slip(self, pr_succ):
        #set the transition succes probabilties of the simulation to pr_succ
        if self.extension:
            (Tn, Ts, Te, Tw) = get_transitions_extension(pr_succ, self.pr_dry)
        else:
            (Tn, Ts, Te, Tw) = get_transitions(pr_succ)
        nstates = len(self.pomdp.pomdpenv.states)
        t = np.zeros((self.nactions, nstates, nstates))
        t[0] = np.array(Tn)
        t[1] = np.array(Ts)
        t[2] = np.array(Te)
        t[3] = np.array(Tw)
        self.sim.set_transition(t)
        self.logger.log_pr_succ(pr_succ)


    def update_policy(self, mdp_path, pol_path):
        write_t(mdp_path, self.pomdp.pomdpenv.get_transition())
        solve(mdp_path)
        self.pomdp.pomdppolicy = POMDPPolicy(pol_path)



    def set_exploration(self, exp):
        self.exp = exp
        self.logger.log_exploration(exp)



    def print_summary(self):
        print("---Controller summary---")
        print("history: ", self.hist)
        print("T:", self.pomdp.pomdpenv.T)
        print("action history:", [self.pomdp.pomdpenv.actions[x[1]] for x in self.hist])
        print("------------------------")


class Temporal_controller(Controller):
    def __init__(self, pomdp, sim, weight, exploration, logger, extension=False, pr_dry = 0.9):
        super().__init__( pomdp, sim, weight, exploration, logger, extension, pr_dry)
        self.hist_c = [] #clustered history: list of (t_recent_counts, t)


    def t_sim_hellinger(self, t1, t2, sums):

        sum = 0
        for i in range(len(t1)):
            for j in range(len(t1[i])):
                hell = 1 - np.sqrt( np.power((np.sqrt(t1[i][j]) - np.sqrt(t2[i][j])), 2).sum())/np.sqrt(2) #1 - helling distance for each action-state pair
                sum = sum + sums[i][j]*hell
        #print(sum)
        return sum

    def t_sim(self, t1, t2, sums):
        sum = 0
        for i in range(len(t1)):
            for j in range(len(t1[i])):
                bc = np.sqrt(t1[i][j] * t2[i][j]).sum() #Bhattacharyya coeff for each action-state pair
                sum = sum + sums[i][j]*bc
        # print(sum)
        return sum


    def update(self):
        '''
        calc most likely transition function t given history
        t = nparray met elke entry: (a, s, s')
        '''
        nstates = len(self.pomdp.pomdpenv.states)
        t_recent_counts = np.zeros((self.nactions, nstates, nstates))

        b = self.pomdp.belief
        for step in reversed(self.hist):
            counts = np.outer(step[0], b) #calc outer product of b(s) and b(s') (product van elke combinatie)
            t_recent_counts[step[1]] += counts        #add these counts to the corresponding action
            b = step[0]                   #set b(s') to current for next iter


        sums = np.zeros((self.nactions, nstates)) #indicate for each state-action pair how many times the actions was recently taken in the states
        #normalize
        t_recent = t_recent_counts.copy()
        for i in range(len(t_recent)):
            for j in range(len(t_recent[i])):
                sum = t_recent[i][j].sum()
                sums[i][j] = sum
                if sum == 0: #if unseen set all to one to normalize to random
                    t_recent[i][j] = np.ones(len(t_recent[i][j]))
                t_recent[i][j] = t_recent[i][j]/t_recent[i][j].sum()


        t = t_recent_counts.copy()*sums.sum()


        w = 1
        for cluster in reversed(self.hist_c):
            t = t + w * self.t_sim_hellinger(t_recent,cluster[1],sums) * cluster[0]
            w = w * self.weight
        #normalize
        for i in range(len(t)):
            for j in range(len(t[i])):
                if t[i][j].sum() == 0: #if unseen set all to one to normalize to random
                    t[i][j] = np.ones(len(t[i][j]))
                t[i][j] = t[i][j]/t[i][j].sum()

        self.hist_c.append((t_recent_counts, t)) #of t als laatste param?
        self.hist = []


        #self.logger.log_t(self.sim.get_transition(), t)

        #set transition function in pomdp env and logg
        self.pomdp.pomdpenv.set_transition(t)



    #TODO: volgens mij kan er overal met genormaliseerde versie gewerkt worden!
    def update_alt(self, weight, save):
        '''
        calc most likely transition function t given history
        t = nparray met elke entry: (a, s, s')
        '''
        nstates = len(self.pomdp.pomdpenv.states)
        t_recent_counts = np.zeros((self.nactions, nstates, nstates))

        b = self.pomdp.belief
        for step in reversed(self.hist):
            counts = np.outer(step[0], b) #calc outer product of b(s) and b(s') (product van elke combinatie)
            t_recent_counts[step[1]] += counts        #add these counts to the corresponding action
            b = step[0]                   #set b(s') to current for next iter


        sums = np.zeros((self.nactions, nstates)) #indicate for each state-action pair how many times the actions was recently taken in the states
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
        for cluster in reversed(self.hist_c):
            sims.append(w * self.t_sim_hellinger(t_recent,cluster[1],sums))
            w = w * self.weight

        #flip sims since we looped in reverse
        sims = np.flip(np.array(sims))
        #get sort indices
        inds = np.argsort(sims)
        # print("at step: " + str(len(sims)))
        # print(inds)
        w = 1
        for ind in reversed(inds):
            t = t + w * self.hist_c[ind][0]
            w = w*weight
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

        if save:
            self.hist_c.append((t_recent_counts, t)) #of t als laatste param?
        self.hist = []


       # self.logger.log_t(self.sim.get_transition(), t)

        #set transition function in pomdp env and logg
        self.pomdp.pomdpenv.set_transition(t)