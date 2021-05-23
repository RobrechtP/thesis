from src.pomdp import *
from src.solverAdapter import *
import numpy as np
from src.simulator import *
from src.controller import *
from src.logger import *
from src.slipGenerator import *
import time


#code to execute an experiment, should show most important functionality
def experiment():
    #indicate whether 4x4 domain (false) or 6x6 domain (true) is used
    EXTENSION = False

    #pomdp filename inside domains dir
    pomdp_file = '4x4MDP.POMDP'
    env_path = "../domains/" + pomdp_file

    #pomdp filename inside domains dir where transition function estimate can be filled in
    # (ensure same dom specs as pomdp_file)
    pomdp_est_file = '4x4MDP_est.POMDP'

    #path of .alpha file that is generated when solving the pomdp_est_file
    pol_path = "../output/4x4MDP_est.alpha"

    #P(succes): initial action succes probability in domain ( = 1-P(schuif))
    p_succ = 0.95

    #write transition function with initial p_succ to the POMDP
    write_transitions(env_path, p_succ, extension=EXTENSION)

    #solve pomdp estimate just to ensure the .alpha file exists already, this first policy does not influence expriment
    solve(pomdp_est_file)

    #set initial belief
    if EXTENSION:
        belief = np.zeros(27)
        belief[14] = 1
    else:
        belief = np.zeros(14) #todo: add to pomdp file parser
        belief[10] = 1

    #create the POMDP object and log info
    pomdp = POMDP(env_path, pol_path, belief)
    pomdp.pomdpenv.print_summary()

    #create simulation object
    sim = Simulation(env_path)

    #create transition function generator
    rain_gen = RainGenerator()

    #load pre-generated transition function data
    rain_gen.load_data("../transitions/rain3.txt")
    #or optionally generate new data instead
    #rain_gen.generate_data()

    #create logger object , defining path of excel file
    logger = Logger("../tests/adaptive400/peak10k_t097_lin150k.xlsx")

    #create one of three controllers: uniform weighted, recent weighted or similarity weighted
    #cont = Controller(pomdp, sim, 1, 1, logger, EXTENSION)
    #cont = Controller(pomdp, sim, 0.9995, 1, logger, EXTENSION)
    cont = Temporal_controller(pomdp, sim, 1, 1, logger, EXTENSION)

    #set p_succ of simulation (should be redundant with former code)
    cont.set_sim_p_succ(p_succ)


    #main loop of the experiment
    for i in range(300000):
        #execute one step in the simulation
        cont.step()

        if i%400 == 0:
            #calculate new exploration amount
            exp = exp_lin(i,150000)

            #if non-temporal controller is used: recalculate transition function estimation
            #cont.update()

            #else if no exploration is present, new data shouldnt be stored
            save = True
            if exp == 0:
                save = False
            #for temporal controller: recalculate transition function estimation with given weight and save boolean
            cont.update_alt(0.97, save)

            #recalculate policy with new estimation
            cont.update_policy(pomdp_est_file, pol_path)
            #log current information
            cont.log()
            #set new exploration value
            cont.set_exploration(exp)

        #let the generator update the transition function of the simulation
        rain_gen.step(cont, i)

        #or alternatively use a simpler form of transition function variation over time:
        #p_succ = peak_gen(cont, i, 10000, p_succ)
        #switch_gen(cont, i, 4100)
        #p_succ = switch_ran_gen(cont, 1/4000, p_succ)

    #optionally save history to be used in demo
    #cont.save_history("data_rain1.npy")


#exploration calc function
def exp_lin(i, interval):
    return max(1 - i/interval, 0)

#some simpler transition function time variatons that could be used
def peak_gen(cont, i, interval, p_succ):
    if i%(interval/100) == 0:
        if i%(2*interval) < interval:
            p_succ = p_succ + 0.002
        else:
            p_succ = p_succ - 0.002
        cont.set_sim_p_succ(p_succ)
    return p_succ

def switch_gen(cont, i, interval):
    if i%(interval*2) == 0:
        cont.set_sim_p_succ(0.85)
    if i%(interval*2) == interval:
        cont.set_sim_p_succ(0.65)

def switch_ran_gen(cont, p, p_succ):
    if np.random.random() < p:
        if p_succ == 0.75:
            p_succ = 0.8
        else:
            p_succ = 0.75
        cont.set_sim_p_succ(p_succ)
    return p_succ


def main():
    experiment()


if __name__ == "__main__":
    main()