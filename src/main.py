from src.pomdp import *
from src.solverAdapter import *
import numpy as np
from src.simulator import *
from src.controller import *
from src.logger import *
from src.slipGenerator import *
import time


def main():
    time1 = time.time()
    mdp_path = '4x4_test.POMDP'
    mdp_est_path = '4x4_test_est.POMDP'
    pol_path = "../output/4x4_test_est.alpha"

    env_path = "../domains/" + mdp_path

    slip = 0.95
    write_transitions(env_path, slip)
    solve(mdp_est_path)

    belief = np.zeros(14) #todo: add to pomdp file parser
    belief[10] = 1
    #belief = np.array([0.111111, 0.111111, 0.111111, 0.0, 0.111111, 0.111111, 0.0, 0.111112, 0.111111, 0.111111, 0.111111])
    pomdp = POMDP(env_path, pol_path, belief)
    pomdp.pomdpenv.print_summary()

    sim = Simulation(env_path)
    rain_gen = RainGenerator()
    rain_gen.load_data("../transitions/rain2.txt")

    logger = Logger("../tests/pomdp_adaptive/rain2_09995_lin150k_pomdp.xlsx", "main") #hswitch is on

    cont = Controller(pomdp, sim, 0.9995, 1, logger)
    #cont = Temporal_controller(pomdp, sim, 1, 1, logger)

    cont.set_sim_slip(slip)
    #cont.print_summary()


    for i in range(300000):
        cont.step()
        if i%400 == 0:

            exp = exp_lin(i,150000)
            save = True
            if exp == 0:
                save = False

            cont.update()
            #cont.update_alt(0.97, save)
            cont.update_policy(mdp_est_path, pol_path)
            cont.log()
            cont.set_exploration(exp)
        #slip = peak_gen(cont, i, 10000, slip)
        rain_gen.step(cont, i)
        #switch_gen(cont, i, 2000)

        #slip = peak_gen(cont, i, 15000, slip)


        #slip = switch_ran_gen(cont, 1/2000, slip)

        #if i==100000:
       #     cont.set_exploration(0)
        #    cont.set_sim_slip(0.75)


     #   if i%2000 == 0:
     #       cont.log_t_complete()
#
    #cont.print_summary()
    time2 = time.time()
    print("runtime: " + str(time2-time1))



def exp_lin(i, interval):
    return max(1 - i/interval, 0)

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
        cont.set_sim_slip(0.95)
    if i%(interval*2) == interval:
        cont.set_sim_slip(0.6)

def switch_ran_gen(cont, p, slip):
    if np.random.random() < p:
        if slip == 0.6:
            slip = 0.8
        else:
            slip = 0.6
        cont.set_sim_slip(slip)
    return slip


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