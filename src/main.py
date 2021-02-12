from src.pomdp import *
from src.solverAdapter import *
import numpy as np
from src.simulator import *
from src.controller import *


def main():
    mdp = "4x4MDP.POMDP"
    pol_path = "../output/4x4MDP.alpha"

    env_path = "../domains/" + mdp

    write_transitions(env_path, 0.7)
#    solve(mdp)

    belief = np.zeros(14)
    belief[10] = 1
    pomdp = POMDP(env_path, pol_path, belief)
    pomdp.pomdpenv.print_summary()

    sim = Simulation(env_path)

    cont = Controller(pomdp, sim, 0.95, 0.1)
    cont.print_summary()
    for i in range(20):
        cont.step()
    cont.print_summary()


    for i in range(0):
        step(pomdp, sim)




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