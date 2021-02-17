from src.pomdp import *
from src.solverAdapter import *
import numpy as np
from src.simulator import *
from src.controller import *
from src.logger import *


def main():
    mdp_path = '4x4MDP.POMDP'
    pol_path = "../output/4x4MDP.alpha"

    env_path = "../domains/" + mdp_path

    slip = 0.6
    write_transitions(env_path, slip)
    #solve(mdp_path)

    belief = np.zeros(14) #todo: add to pomdp file parser
    belief[10] = 1
    #belief = np.array([0.111111, 0.111111, 0.111111, 0.0, 0.111111, 0.111111, 0.0, 0.111112, 0.111111, 0.111111, 0.111111])
    pomdp = POMDP(env_path, pol_path, belief)
    pomdp.pomdpenv.print_summary()

    sim = Simulation(env_path)

    logger = Logger("../tests/explore/peak10k_alt01_trunc40k.xlsx", "main") #hellinger is on

    #cont = Controller(pomdp, sim, 0.9995, 1, logger)
    cont = Temporal_controller(pomdp, sim, 1, 1, logger)

    cont.set_sim_slip(slip)
    cont.print_summary()

    for i in range(60000):
        cont.step()
        if i%200 == 0:
            #cont.update()
            cont.update_alt(0.1)
#            cont.update_policy(mdp_path, pol_path)
        if i == 40000:
            cont.exp = 0
          #  cont.weight = 1
        slip = peak_gen(cont, i, 10000, slip)
        #switch_gen(cont, i, 2000)



     #   if i%2000 == 0:
     #       cont.log_t_complete()
#
    #cont.print_summary()


    for i in range(0):
        step(pomdp, sim)

def peak_gen(cont, i, interval, slip):
    if i%(interval/100) == 0:
        if i%(2*interval) < interval:
            slip = slip + 0.002
        else:
            slip = slip - 0.002
        cont.set_sim_slip(slip)
    return slip



def switch_gen(cont, i, interval):
    if i%(interval*2) == 0:
        cont.set_sim_slip(0.8)
    if i%(interval*2) == interval:
        cont.set_sim_slip(0.6)

def step(pomdp, sim):
    print("start step")
    best_action_num, expected_reward = pomdp.get_best_action()
    best_action_str = pomdp.get_action_str(int(best_action_num))
    print ('\t- action:         ', best_action_str)
    print ('\t- expected reward:', expected_reward)
    obs = sim.step(int(best_action_num))
    pomdp.update_belief(int(best_action_num), obs)
    print ('\t- belief:         ', np.round(pomdp.belief.flatten(), 3))
    print ('\t- state:          ', sim.state)
    print ('\t- reward:         ', sim.reward)






if __name__ == "__main__":
    main()