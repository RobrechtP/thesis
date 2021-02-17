import subprocess
from fractions import Fraction
from src.pomdp import *



def solve(path = '4x4MDP.POMDP'):
    subprocess.run(['java', '-cp', '../lib/SolvePOMDP.jar;../lib/*', 'program.SolvePOMDP', path ], shell=True)

#-cp SolvePOMDP.jar;../lib/*'

#get the transition matrices Tn, Ts, Te, Tw of the 4x4 grid given pr_success
def get_transitions(pr_succ):
    #chance corresponding to landing on a specific other tile because of slipping
    succ = pr_succ
    slip = float(Fraction(1 - Fraction(str(succ))) / 2)

    #create list of only 0's
    Tn = [[float(0)] * 14 for i in range(14)]
    Ts = [[float(0)] * 14 for i in range(14)]
    Te = [[float(0)] * 14 for i in range(14)]
    Tw = [[float(0)] * 14 for i in range(14)]

    Tn[0][0] = 1-slip
    Tn[0][1] = slip
    Tn[1][1] = succ
    Tn[1][0] = slip
    Tn[1][2] = slip
    Tn[2][2] = succ
    Tn[2][1] = slip
    Tn[2][3] = slip
    Tn[3][3] = 1-slip
    Tn[3][2] = slip
    Tn[4][0] = succ
    Tn[4][4] = 2*slip
    Tn[5][2] = succ
    Tn[5][5] = slip
    Tn[5][6] = slip
    Tn[6][10] = 1.0
    Tn[7][4] = succ
    Tn[7][7] = 2*slip
    Tn[8][5] = succ
    Tn[8][8] = slip
    Tn[8][9] = slip
    Tn[9][10] = 1.0
    Tn[10][7] = succ
    Tn[10][10] = slip
    Tn[10][11] = slip
    Tn[11][11] = succ
    Tn[11][10] = slip
    Tn[11][12] =slip
    Tn[12][8] = succ
    Tn[12][11] = slip
    Tn[12][13] = slip
    Tn[13][13] = slip
    Tn[13][9] = succ
    Tn[13][12] = slip

    Ts[0][0] = slip
    Ts[0][4] = succ
    Ts[0][1] = slip
    Ts[1][1] = succ
    Ts[1][0] = slip
    Ts[1][2] = slip
    Ts[2][5] = succ
    Ts[2][1] = slip
    Ts[2][3] = slip
    Ts[3][3] = slip
    Ts[3][6] = succ
    Ts[3][2] = slip
    Ts[4][4] = 2*slip
    Ts[4][7] = succ
    Ts[5][8] = succ
    Ts[5][5] = slip
    Ts[5][6] = slip
    Ts[6][10] = 1.0
    Ts[7][7] = 2*slip
    Ts[7][10] = succ
    Ts[8][12] = succ
    Ts[8][8] = slip
    Ts[8][9] = slip
    Ts[9][10] = 1.0
    Ts[10][10] = 1-slip
    Ts[10][11] = slip
    Ts[11][11] = succ
    Ts[11][10] = slip
    Ts[11][12] = slip
    Ts[12][12] = succ
    Ts[12][11] = slip
    Ts[12][13] = slip
    Ts[13][13] = 1 - slip
    Ts[13][12] = slip

    Te[0][0] = slip
    Te[0][1] = succ
    Te[0][4] = slip
    Te[1][1] = 2*slip
    Te[1][2] = succ
    Te[2][3] = succ
    Te[2][2] = slip
    Te[2][5] = slip
    Te[3][3] = 1-slip
    Te[3][6] = slip
    Te[4][4] = succ
    Te[4][0] = slip
    Te[4][7] = slip
    Te[5][6] = succ
    Te[5][2] = slip
    Te[5][8] = slip
    Te[6][10] = 1.0
    Te[7][7] = succ
    Te[7][4] = slip
    Te[7][10] = slip
    Te[8][9] = succ
    Te[8][5] = slip
    Te[8][12] = slip
    Te[9][10] = 1.0
    Te[10][11] = succ
    Te[10][10] = slip
    Te[10][7] = slip
    Te[11][11] = 2*slip
    Te[11][12] = succ
    Te[12][13] = succ
    Te[12][12] = slip
    Te[12][8] = slip
    Te[13][13] = 1-slip
    Te[13][9] = slip

    Tw[0][0] = 1-slip
    Tw[0][4] = slip
    Tw[1][0] = succ
    Tw[1][1] = 2*slip
    Tw[2][1] = succ
    Tw[2][2] = slip
    Tw[2][5] = slip
    Tw[3][2] = succ
    Tw[3][3] = slip
    Tw[3][6] = slip
    Tw[4][4] = succ
    Tw[4][0] = slip
    Tw[4][7] = slip
    Tw[5][5] = succ
    Tw[5][2] = slip
    Tw[5][8] = slip
    Tw[6][10] = 1.0
    Tw[7][7] = succ
    Tw[7][4] = slip
    Tw[7][10] = slip
    Tw[8][8] = succ
    Tw[8][5] = slip
    Tw[8][12] = slip
    Tw[9][10] = 1.0
    Tw[10][7] = slip
    Tw[10][10] = 1-slip
    Tw[11][10] = succ
    Tw[11][11] = 2*slip
    Tw[12][11] = succ
    Tw[12][12] = slip
    Tw[12][8] = slip
    Tw[13][12] = succ
    Tw[13][13] = slip
    Tw[13][9] = slip

    #TEST: print if somewhere sum is not equal to 1 (error)
    for n in Tn:
        if sum(n) != 1:
            print("transition calc ERROR: (n)" + str(n))
    for s in Ts:
        if sum(s) != 1:
            print("transition calc ERROR: (s) " + str(s))
    for e in Te:
        if sum(e) != 1:
            print("transition calc ERROR (e): " + str(e))
    for w in Tw:
        if sum(w) != 1:
            print("transition calc ERROR (w): " + str(w))


    return (Tn, Ts, Te, Tw)

#overwrite the transition parameters of a given correctly formatted POMDP file to match succes chance
def write_transitions(path, pr_succ):

    Tn,Ts,Te,Tw = get_transitions(pr_succ)
    file = open(path, "r")
    lines = file.readlines()

    start = lines.index('T: n\n')
    for i in range(0, len(Tn)):
        lines[start + i + 1] = str(Tn[i])[1:-1].replace(',','') + '\n'
    start = lines.index('T: s\n')
    for i in range(0, len(Ts)):
        lines[start + i + 1] = str(Ts[i])[1:-1].replace(',','') + '\n'
    start = lines.index('T: e\n')
    for i in range(0, len(Te)):
        lines[start + i + 1] = str(Te[i])[1:-1].replace(',','') + '\n'
    start = lines.index('T: w\n')
    for i in range(0, len(Tw)):
        lines[start + i + 1] = str(Tw[i])[1:-1].replace(',','') + '\n'



    file = open(path, "w")
    file.writelines(lines)
    file.close()

#write_transitions("../domains/4x4MDP.POMDP", 0.8)
#solve('4x4_test.POMDP')
#print("done")