import globvar as GV
import numpy as np
import random
from math import *
import csv
from time import clock as ck
import cLSOutilities as CU

dateprice   =[]
netdateprice=[]
revenue     =[]
netrevenue  =[]
interval    =[]

class Annealing: # popsize must be multiple of 4
    def __init__(Anand, obj, dim, ngen):
        Anand.EPSILON = 1
        Anand.INFINITY = 10e16
        Anand.obj = obj
        Anand.dim = dim
        Anand.ngen = ngen
        Anand.RIGID = 0
        Anand.state = np.array(Anand.dim, dtype=int)
        Anand.energy = 0
        Anand.lowb = np.array(Anand.dim, dtype=int)  #[0 for i in range(Anand.dim)]  #
        Anand.highb = np.array(Anand.dim, dtype=int)  #[1 for i in range(Anand.dim)]  #
        Anand.genTime = np.zeros(ngen)
        Anand.bestmemyet = np.zeros(Anand.dim)  # [0 for i in range(Anand.dim)]  #
        Anand.bestsofar = -np.inf
        Anand.currentbest = -np.inf
        Anand.worstmemyet = np.zeros(Anand.dim)  # [0 for i in range(Anand.dim)]  #
        Anand.worstsofar = np.inf
        Anand.currentworst = np.inf
        #Anand.pop_init()

    def setbounds(Anand, lows, highs):
        Anand.lowb = lows[:]
        Anand.highb = highs[:]
        return

    def pop_init(Anand):
        # Anand.pop.append([])
        Anand.state = Anand.lowb[:]
        Anand.energy = Anand.eval_pop()
        # print("Initial")
        # print(Anand.state, Anand.energy)

    def eval_pop(Anand):
        # irp_dates = []
        # for j in range(Anand.dim):
        #     irp_dates.append(GV.volume_dates[Anand.state[j]])
        # Anand.state = [2, 9, 13, 10, 2, 13, 2, 9, 5, 7, 15, 19, 4, 4, 12, 10, 9, 9, 3, 2, 13, 12, 5, 6, 3, 11, 1, 13, 1, 13, 21, 22, 11, 7, 6, 17, 11, 28, 28, 3, 8, 6, 16, 15, 10, 1, 39, 21, 30, 15, 2, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1]
        tmp = np.array(GV.volume_dates)
        # GV.volume_pickup_dates = tmp[Anand.state[:]]
        for c in range(GV.num_of_contries):
            # if c== 32:
            #     print("Here")
            GV.pricevol[c] = tmp[Anand.state[c]]
            for d in range(len(GV.datediff[c])):
                if GV.datediff[c][0] < 0:
                    GV.dossier_submission_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][0])
                else:
                    GV.dossier_submission_date[c] = CU.Datesum(GV.pricevol[c], GV.datediff[c][0])

                if GV.datediff[c][1] < 0:
                    GV.price_approval_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][1])
                else:
                    GV.price_approval_date[c] = CU.Datesum(GV.pricevol[c], GV.datediff[c][1])

                if GV.datediff[c][2] < 0:
                    GV.price_publication_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][2])
                else:
                    GV.price_publication_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][2])

                if GV.datediff[c][3] < 0:
                    GV.reimbursement_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][3])
                else:
                    GV.reimbursement_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][3])

                if GV.datediff[c][4] < 0:
                    GV.volume_pickup_dates[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][4])
                else:
                    GV.volume_pickup_dates[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][4])

        results = Anand.obj()
        # print(results[-4])
        return results[-4]

    def run(Anand, run, seed):
        fname = 'Output/Simulated/Simulated_Results_' + str(run) + '.csv'
        ofile = csv.writer(open(fname, "w+"), delimiter=',')
        # toPrint = np.column_stack((np.array(Anand.pop), np.array(Anand.fits)))
        # for row in toPrint:
        #     ofile.writerow(row)
        # ofile.writerow('\r')
        ##### Generate initial population
        random.seed(seed)
        Anand.pop_init()
        prevState = Anand.state[:]
        prevEnergy = Anand.energy
        # print("Prevstate", Anand.state)
        # print("Prevenergy", Anand.energy)
        epochs = steps = (run+1)*Anand.ngen
        accepts, improves = 0, 0
        ##### Starts perturbation
        step = 0
        starttime = ck()
        for gen in range(epochs):
            # print("Generation ", gen)
            if not(step < steps):
                break

            Anand.move()

            T = 0.0
            while T == 0.0:
                step += 1
                # st = ck()
                Anand.move()
                # e = ck()-st
                T = abs(Anand.energy - prevEnergy)

            dE = Anand.energy - prevEnergy
            if dE < 0.0 and exp(-dE / T) > random.random():
                Anand.state = prevState[:]
                Anand.energy = prevEnergy
            else:
                accepts += 1
                if dE > 0.0:
                    improves += 1
                # prevState = copy.deepcopy(state)
                prevState = Anand.state[:]
                prevEnergy = Anand.energy

        total_time = ck() - starttime
        ofile.writerow((run, steps, total_time, total_time/steps, prevEnergy, improves, float(improves)/step))
        # irp_dates = []
        # for j in range(len(prevState)):
        #     irp_dates.append(GV.volume_dates[prevState[j]])
        tmp = np.array(GV.volume_dates)
        irp_dates = tmp[prevState[:]]
        ofile.writerow((prevState))
        ofile.writerow((irp_dates))
        # ofile.writerows(Anand.genTime)
        return Anand.state, Anand.energy, accepts, improves, step, float(accepts)/step, float(improves)/step

    def move(Anand):
        a = random.randint(0, len(Anand.state) - 1)
        b = random.randint(0, len(Anand.state) - 1)
        #####Swap two random components
        temp = max(Anand.lowb[a], min(Anand.state[b], Anand.highb[a]))
        Anand.state[b] = max(Anand.lowb[b], min(Anand.state[a], Anand.highb[b]))
        Anand.state[a] = temp
        #####Compute the energy
        Anand.energy = Anand.eval_pop()
        # print("inside move")
        # print(Anand.state, Anand.energy)

    def pop_print(Anand):
        for i in range(Anand.popsize):
            print(i, Anand.pop[i], Anand.fits[i])
            # print(i,Anand.fits[i])
        return