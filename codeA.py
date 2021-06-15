import os
import re

os.chdir("E:\\Bidouillage\\Challenge Opti\\code\\data")
num = "05"

##Classes

class Intervention:

    def __init__(self, ID, name, d):
        self.ID = ID
        self.name = name
        self.d = d.copy()
        self.tf = len(self.d)
        self.daysForbidden = []

    def start(self, t0):
        self.t0 = t0

    def forbid(self, day):
        self.daysForbidden.append(day)

##Paramètres

params = open("A_"+num+"_param.csv", "r")
inputParam = params.read()
inputParam = re.split("\n", inputParam)

for i in range(len(inputParam)):
    inputParam[i] = re.split("\t", inputParam[i])

params.close()

T = int(inputParam[0][1])
I = int(inputParam[1][1])
C = int(inputParam[2][1])
S = int(inputParam[3][1])
E = int(inputParam[4][1])
tau = float(inputParam[5][1])
alpha = float(inputParam[6][1])

##Variables globales

interventions = []
ressources = [[] for i in range(C)]
workload = [[[[0 for l in range(T)] for k in range(T)] for j in range(C)] for i in range(I)]
risques = [[[[0 for l in range(S)] for k in range(T)] for j in range(T)] for i in range(I)]
exclusions = [[[] for j in range(I)] for i in range(T)]

planning = [[] for i in range(T)]
utilisationRess = [[0 for i in range(T)] for j in range(C)]

##Interventions

inter = open("A_"+num+"_interv.csv", "r")
inter.readline()
inputInt = inter.read()
inputInt = re.split("\n", inputInt)

for i in range(I):
    inputInt[i] = re.split("\t", inputInt[i])

for i in range(I):
    temp = Intervention(inputInt[i][0], inputInt[i][1], inputInt[i][2::])
    interventions.append(temp)

inter.close()

##ressources

ress = open("A_"+num+"_ressources.csv", "r")
ress.readline()
inputRess = ress.read()
inputRess = re.split("\n", inputRess)

for i in range(C):
    inputRess[i] = re.split("\t", inputRess[i])
    for j in range(T):
        ressources[i].append(float(inputRess[i][j]))

ress.close()

##Charge de travail

work = open("A_"+num+"_workload.csv", "r")
work.readline()
inputWork = work.read()
inputWork = re.split("\n", inputWork)

for i in range(len(inputWork)-1):
    line = re.split("\t", inputWork[i])
    interv_ID = int(line[0])
    ress_ID = int(line[1])
    t = int(line[2])
    t0 = int(line[3])
    val = float(line[4])
    workload[interv_ID][ress_ID][t0][t] = val

work.close()

##Scenarios

scen = open("A_"+num+"_scenarios.csv", "r")
scen.readline()
inputScen = scen.read()
inputScen = re.split("\n", inputScen)

for i in range(len(inputScen)-1):
    line = re.split("\t", inputScen[i])
    interv_ID = int(line[0])
    t = int(line[1])
    t0 = int(line[2])

    for j in range(S):
        risques[interv_ID][t][t0][j] = line[j+3]

scen.close()

##Exclusions

excl = open("A_"+num+"_exclusion.csv", "r")
excl.readline()
inputExcl = excl.read()
inputExcl = re.split("\n", inputExcl)

for i in range(len(inputExcl)-1):
    line = re.split("\t", inputScen[i])
    t = int(line[2])
    int1_ID = int(line[0])
    int2_ID = int(line[1])
    exclusions[t][int1_ID].append(int2_ID)
    exclusions[t][int2_ID].append(int1_ID)

##Calcul du planning

for i in range(I):
    t = 0
    possible = False
    while(t < T and not possible):
        if(t < interventions[i].tf):
            respecteContraintes = True
            for j in range(t, t+int(interventions[i].d[t])):                    #j = jour
                for k in range(C):                                              #k = ressource
                    if((not ressources[k][j] >= utilisationRess[k][j] + workload[i][k][t][j]) or (t in interventions[i].daysForbidden)):
                        respecteContraintes = False
            if(respecteContraintes):
                interventions[i].start(t)
                possible = True

                for j in range(t, t+int(interventions[i].d[t])):
                    for k in range(C):
                        utilisationRess[k][j] += workload[i][k][t][j]
                        planning[t].append(interventions[i])
                        for l in range(len(exclusions[t][i])):
                            tache_ID = exclusions[t][i][l]
                            interventions[tache_ID].forbid(t)

        t+=1

os.chdir("E:\\Bidouillage\\Challenge Opti\\code")

ret = open("resA"+num+".csv", "w")
ret.write("A\t"+num+"\n")

for i in range(I):
    ret.write(interventions[i].name + "\t" + str(interventions[i].t0) + "\n")

ret.close()