import subprocess
from fractions import Fraction
from src.pomdp import *
import xlsxwriter



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


    return (Tn, Ts, Te, Tw)



def get_transitions_extension(pr_succ, pr_succ_dry):
    #chance corresponding to landing on a specific other tile because of slipping
    succ = pr_succ
    slip = float(Fraction(1 - Fraction(str(succ))) / 2)

    dsucc = pr_succ_dry
    dslip = float(Fraction(1 - Fraction(str(dsucc))) / 2)

    #create list of only 0's
    Tn = [[float(0)] * 27 for i in range(27)]
    Ts = [[float(0)] * 27 for i in range(27)]
    Te = [[float(0)] * 27 for i in range(27)]
    Tw = [[float(0)] * 27 for i in range(27)]

    Tn[0][0] = 1.0
    Tn[1][1] = 1.0
    Tn[2][14] = 1.0
    Tn[3][3] = 1.0
    Tn[4][4] = 1.0
    Tn[5][5] = 1.0

    Tn[6][0] = succ
    Tn[6][6] = slip
    Tn[6][7] = slip
    Tn[7][14] = 1.0
    Tn[8][3] = succ
    Tn[8][8] = 2*slip
    Tn[9][5] = succ
    Tn[9][9] = 2*slip

    Tn[10][6] = succ
    Tn[10][10] = slip
    Tn[10][11] = slip
    Tn[11][14] = 1.0
    Tn[12][8] = succ
    Tn[12][12] = 2*slip
    Tn[13][9] = succ
    Tn[13][13] = 2*slip

    Tn[14][10] = succ
    Tn[14][14] = slip
    Tn[14][15] = slip
    Tn[15][11] = succ
    Tn[15][14] = slip
    Tn[15][16] = slip
    Tn[16][16] = 1.0
    Tn[17][12] = dsucc
    Tn[17][17] = dslip
    Tn[17][16] = dslip
    Tn[18][13] = dsucc
    Tn[18][18] = 2*dslip

    Tn[19][14] = succ
    Tn[19][19] = 2*slip
    Tn[20][18] = dsucc
    Tn[20][20] = 2*dslip

    Tn[21][19] = succ
    Tn[21][21] = slip
    Tn[21][22] = slip
    Tn[22][22] = 1.0
    Tn[23][23] = 1.0
    Tn[24][24] = 1.0
    Tn[25][25] = 1.0
    Tn[26][20] = dsucc
    Tn[26][25] = dslip
    Tn[26][26] = dslip

    Ts[0][6] = succ
    Ts[0][0] = slip
    Ts[0][1] = slip
    Ts[1][7] = succ
    Ts[1][0] = slip
    Ts[1][2] = slip
    Ts[2][14] = 1.0
    Ts[3][8] = succ
    Ts[3][2] = slip
    Ts[3][4] = slip
    Ts[4][4] = 1.0
    Ts[5][9] = succ
    Ts[5][4] = slip
    Ts[5][5] = slip

    Ts[6][10] = succ
    Ts[6][6] = slip
    Ts[6][7] = slip
    Ts[7][14] = 1.0
    Ts[8][12] = succ
    Ts[8][8] = 2*slip
    Ts[9][13] = succ
    Ts[9][9] = 2*slip

    Ts[10][14] = succ
    Ts[10][10] = slip
    Ts[10][11] = slip
    Ts[11][14] = 1.0
    Ts[12][17] = succ
    Ts[12][12] = 2*slip
    Ts[13][18] = succ
    Ts[13][13] = 2*slip

    Ts[14][19] = succ
    Ts[14][14] = slip
    Ts[14][15] = slip
    Ts[15][15] = 1.0
    Ts[16][16] = 1.0
    Ts[17][17] = 1.0
    Ts[18][20] = dsucc
    Ts[18][18] = 2*dslip

    Ts[19][21] = succ
    Ts[19][19] = 2*slip
    Ts[20][26] = dsucc
    Ts[20][20] = 2*dslip

    Ts[21][21] = 1.0
    Ts[22][22] = 1.0
    Ts[23][23] = 1.0
    Ts[24][24] = 1.0
    Ts[25][25] = 1.0
    Ts[26][26] = 1.0

    Te[0][1] = succ
    Te[0][0] = slip
    Te[0][6] = slip
    Te[1][2] = succ
    Te[1][1] = slip
    Te[1][7] = slip
    Te[2][14] = 1.0
    Te[3][4] = succ
    Te[3][3] = slip
    Te[3][8] = slip
    Te[4][5] = succ
    Te[4][4] = 2*slip
    Te[5][5] = 1-slip
    Te[5][9] = slip

    Te[6][7] = succ
    Te[6][0] = slip
    Te[6][10] = slip
    Te[7][14] = 1.0
    Te[8][8] = 1.0
    Te[9][9] = 1.0

    Te[10][11] = succ
    Te[10][6] = slip
    Te[10][14] = slip
    Te[11][14] = 1.0
    Te[12][12] = 1.0
    Te[13][13] = 1.0

    Te[14][15] = succ
    Te[14][10] = slip
    Te[14][19] = slip
    Te[15][16] = succ
    Te[15][11] = slip
    Te[15][15] = slip
    Te[16][17] = succ
    Te[16][16] = 2*slip
    Te[17][17] = 1.0
    Te[18][18] = 1.0

    Te[19][19] = 1.0
    Te[20][20] = 1.0

    Te[21][22] = succ
    Te[21][19] = slip
    Te[21][21] = slip
    Te[22][23] = succ
    Te[22][22] = 2*slip
    Te[23][24] = succ
    Te[23][23] = 2*slip
    Te[24][25] = dsucc
    Te[24][24] = 2*dslip
    Te[25][26] = dsucc
    Te[25][25] = 2*dslip
    Te[26][26] = 1.0

    Tw[0][0] = 1.0
    Tw[1][0] = succ
    Tw[1][1] = slip
    Tw[1][7] = slip
    Tw[2][14] = 1.0
    Tw[3][2] = succ
    Tw[3][3] = slip
    Tw[3][8] = slip
    Tw[4][3] = succ
    Tw[4][4] = 2*slip
    Tw[5][4] = succ
    Tw[5][5] = slip
    Tw[5][9] = slip

    Tw[6][6] = 1.0
    Tw[7][14] = 1.0
    Tw[8][8] = 1.0
    Tw[9][9] = 1.0

    Tw[10][10] = 1.0
    Tw[11][14] = 1.0
    Tw[12][12] = 1.0
    Tw[13][13] = 1.0

    Tw[14][14] = 1.0
    Tw[15][14] = succ
    Tw[15][11] = slip
    Tw[15][15] = slip
    Tw[16][15] = succ
    Tw[16][16] = 2*slip
    Tw[17][16] = dsucc
    Tw[17][17] = dslip
    Tw[17][12] = dslip
    Tw[18][18] = 1.0

    Tw[19][19] = 1.0
    Tw[20][20] = 1.0

    Tw[21][21] = 1.0
    Tw[22][21] = succ
    Tw[22][22] = 2*slip
    Tw[23][22] = succ
    Tw[23][23] = 2*slip
    Tw[24][23] = dsucc
    Tw[24][24] = 2*dslip
    Tw[25][24] = dsucc
    Tw[25][25] = 2*dslip
    Tw[26][25] = dsucc
    Tw[26][26] = dslip
    Tw[26][20] = dslip


    return (Tn, Ts, Te, Tw)


#method used for testing to check if no typos were made in the transition generating code
def test_transitions(pr_succ):

    #Tn,Ts,Te,Tw = get_transitions(pr_succ)
    Tn,Ts,Te,Tw = get_transitions_extension(pr_succ, pr_succ)
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
    print("done")


#overwrite the transition parameters of a given correctly formatted POMDP file to match succes chance
#use extension = True in case of writing to 6x6 domain instead of 4x4 domain
def write_transitions(path, pr_succ, extension = False, pr_dry=0.95):

    if extension:
        Tn,Ts,Te,Tw = get_transitions_extension(pr_succ, pr_dry)
    else:
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


def write_t(path, t):
    #write given transition t (matrix [a][s1][s2]) to path
    #only works for domains with actions "n s e w"

    path = "../domains/" + path

    file = open(path, "r")
    lines = file.readlines()

    start = lines.index('T: n\n')
    for i in range(0, len(t[0])):
        lines[start + i + 1] = str(list(t[0][i]))[1:-1].replace(',','') + '\n'
    start = lines.index('T: s\n')
    for i in range(0, len(t[1])):
        lines[start + i + 1] = str(list(t[1][i]))[1:-1].replace(',','') + '\n'
    start = lines.index('T: e\n')
    for i in range(0, len(t[2])):
        lines[start + i + 1] = str(list(t[2][i]))[1:-1].replace(',','') + '\n'
    start = lines.index('T: w\n')
    for i in range(0, len(t[3])):
        lines[start + i + 1] = str(list(t[3][i]))[1:-1].replace(',','') + '\n'



    file = open(path, "w")
    file.writelines(lines)
    file.close()

def solvertest():

    dom = "6x6MDP"
    pr_succ = 0.8
    test_transitions(pr_succ)
    write_transitions("../domains/" + dom + ".POMDP", pr_succ, extension=True)

    solve(dom + '.POMDP')
    pol = POMDPPolicy("../output/" + dom + ".alpha")
    belief = np.zeros(27)
    belief[14] = 1
    print("BEST ACTION START:")
    print(pol.get_best_action(belief))
    belief = np.zeros(27)
    belief[15] = 1
    print("BEST ACTION TILE 15:")
    print(pol.get_best_action(belief))


def enumerate_best_action(dom = "6x6MDP", filename = "policies_6x6.xlsx", extension=True):


    pr_succs = []
    actions = []
    rewards = []
    for pr_succ in range(65,96):

        write_transitions("../domains/" + dom + ".POMDP", pr_succ/100, extension=extension)
        solve(dom + '.POMDP')

        pol = POMDPPolicy("../output/" + dom + ".alpha")
        if extension:
            belief = np.zeros(27)
            belief[14] = 1
        else:
            belief = np.zeros(14)
            belief[10] = 1
        action, reward = pol.get_best_action(belief)
        pr_succs.append(float(pr_succ/100))
        actions.append(int(action))
        rewards.append(float(reward))

    workbook = xlsxwriter.Workbook(filename)

    worksheet = workbook.add_worksheet()

    for col in range(len(pr_succs)):
        worksheet.write_number(0,col, pr_succs[col])
        worksheet.write_number(1,col, actions[col])
        worksheet.write_number(2,col, rewards[col])

    workbook.close()
