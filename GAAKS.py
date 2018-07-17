import globvar as GV
import cLSOutilities as CU
import numpy as np
import random
from math import *
import csv
from time import clock as ck

dateprice   =[]
netdateprice=[]
revenue     =[]
netrevenue  =[]
interval    =[]

class GA: # popsize must be multiple of 4
    def __init__(Anand, obj, dim, popsize, ngen, pc, pm, etac, etam, aa, bb):
        Anand.EPSILON = 1
        Anand.INFINITY = 10e16
        Anand.obj = obj
        Anand.dim = dim
        Anand.popsize = popsize
        Anand.pop = []#np.zeros(Anand.popsize)
        Anand.popindex = []
        Anand.ngen = ngen
        Anand.pc = pc
        Anand.pm = pm
        Anand.etac = etac
        Anand.etam = etam
        Anand.aa = aa
        Anand.bb = bb
        Anand.RIGID = 0
        Anand.lowb = np.zeros(Anand.dim)  #[0 for i in range(Anand.dim)]  #
        Anand.highb = np.ones(Anand.dim)  #[1 for i in range(Anand.dim)]  #
        Anand.fits = np.zeros(Anand.popsize)
        Anand.genTime = np.zeros(ngen)
        Anand.tourneylist = list(range(0, Anand.popsize))
        Anand.tourneysize = 2    # works for 2 for now
        Anand.bestIndex = 0
        Anand.worstIndex = 0
        Anand.bestmemyet = np.zeros(Anand.dim)  # [0 for i in range(Anand.dim)]  #
        Anand.bestsofar = -np.inf
        Anand.currentbest = -np.inf
        Anand.worstmemyet = np.zeros(Anand.dim)  # [0 for i in range(Anand.dim)]  #
        Anand.worstsofar = np.inf
        Anand.currentworst = np.inf
        #Anand.pop_init()

    def pop_init(Anand, seed):
        random.seed(seed)
        # Anand.pop.append([])

        for i in range(Anand.popsize):
            Anand.pop.append([])
            if i == 0:
                for j in range(Anand.dim):
                    Anand.pop[0].append(int(Anand.lowb[j]))
            else:
                for j in range(Anand.dim):
                    Anand.pop[i].append(random.randint(Anand.lowb[j], Anand.highb[j]))

            ##Make the At launch and Post launch Periodicity application dates as the GA generated dates
            # GV.periodicity_date = Anand.pop[i]

        Anand.eval_pop()
        # results = Anand.obj(Anand.pop[i])
        # Anand.fits.append(results[-3])
        #print(len(Anand.fits), Anand.fits)
        return

    def setbounds(Anand, lows, highs):
        for i in range(Anand.dim):
            Anand.lowb[i] = int(lows[i])
            Anand.highb[i] = int(highs[i])
        return

    def run(Anand, run, seed):
        # ofile = csv.writer(open('GAResults.csv', "w+"), delimiter=',')
        # toPrint = np.column_stack((np.array(Anand.pop), np.array(Anand.fits)))
        # for row in toPrint:
        #     ofile.writerow(row)
        # ofile.writerow('\r')
        ##### Generate initial population
        Anand.pop_init(seed)

        ##### Create a filname with name "genData_runnumber.csv
        fname = 'Output/Genetic/genData_'+str(run)+'.csv'
        csvfile = open(fname, 'w+')
        genfile = csv.writer(csvfile)
        genfile.writerow([Anand.dim, Anand.popsize, Anand.ngen, seed])
        # fname1 = 'GenerationTimes_' + str(run) + '.csv'

        ##### Starts perturbation
        for gen in range(Anand.ngen):
            # print("Generation ", gen)
            starttime = ck()
            Anand.pop = Anand.getnewpop()
            r = random.randint(0,Anand.popsize-1)
            Anand.pop[r] = Anand.bestmemyet
            Anand.eval_pop()

            Anand.genTime[gen] = ck() - starttime
            # print("Time taken in this generation is: ", Anand.genTime[gen])
            # Anand.pop_print()

            #####Print population
            # toPrint = np.column_stack((np.array(Anand.pop), np.array(Anand.fits)))
            # for row in toPrint:
            #     genfile.writerow(row)
            # genfile.writerow('\r')

            #####Print Generational data

            genfile.writerow([run, gen, seed, Anand.genTime[gen], Anand.currentbest, Anand.bestsofar])
            genfile.writerow('\r')
        # genTime = np.array(Anand.genTime)
        # genTime.tofile(fname1, sep="\n")

        # toprint = np.column_stack((np.array(Anand.currentbest), np.array(Anand.bestsofar)))
        # genfile.writerows(toprint)
        # genfile.writerow('\r')
        # csvfile.flush()
        # ofile.close()
        csvfile.close()
        del Anand.pop[:]
        return [Anand.bestmemyet, Anand.bestsofar]

    def getnewpop(Anand):
        newpop = []
        # Anand.tourneylist = xrange(0, Anand.popsize)

        random.shuffle(Anand.tourneylist)
        Anand.tourneypos = 0
        for i in range(0, Anand.popsize, 2):
            # print(i)
            [p1, p2] = Anand.getparents()  # return parents, not just indices
            [c1, c2] = Anand.xover(p1, p2)  # return children, not just indices
            c1 = Anand.mutate(c1)
            c2 = Anand.mutate(c2)
            newpop.append(c1)
            newpop.append(c2)
        return newpop

    def getparents(Anand):
        if (Anand.popsize - Anand.tourneypos) < Anand.tourneysize+2:
            random.shuffle(Anand.tourneylist)
            Anand.tourneypos = 0
        if (Anand.fits[Anand.tourneylist[Anand.tourneypos]] > Anand.fits[Anand.tourneylist[Anand.tourneypos + 1]]):
            p1 = Anand.pop[Anand.tourneylist[Anand.tourneypos]]
        else:
            p1 = Anand.pop[Anand.tourneylist[Anand.tourneypos + 1]]
        Anand.tourneypos += Anand.tourneysize
        if (Anand.fits[Anand.tourneylist[Anand.tourneypos]] > Anand.fits[Anand.tourneylist[Anand.tourneypos + 1]]):
            p2 = Anand.pop[Anand.tourneylist[Anand.tourneypos]]
        else:
            p2 = Anand.pop[Anand.tourneylist[Anand.tourneypos + 1]]
        Anand.tourneypos += Anand.tourneysize
        return [p1, p2]

    def xover(Anand, p1, p2):  # Here p1 and p2 are pop members
        c1 = np.zeros_like(p1)
        c2 = np.zeros_like(p2)
        if random.random() <= Anand.pc:  # do crossover
            for i in range(len(p1)):
                if GV.participation_flag[i] != 1:
                    [c1[i], c2[i]] = [p1[i], p2[i]]
                else:
                    [c1[i], c2[i]] = Anand.crossvars(p1[i], p2[i], Anand.lowb[i], Anand.highb[i])
        else:
            c1 = p1
            c2 = p2
        # print("Parents are:")
        # print(p1, p2)
        # print("Childrens are:")
        # print(c1, c2)
        return [c1, c2]

    def crossvars(Anand, p1, p2, low, high):  # Here p1 and p2 are variables

        beta = Anand.getbeta(Anand.aa, Anand.bb)
        # print(beta)

        c1 = p1 + beta * abs(p1 - p2)
        c2 = p2 + beta * abs(p1 - p2)

        if (random.random() < 0.5):
            c1 = ceil(c1)
        else:
            c1 = floor(c1)

        if (random.random() < 0.5):
            c2 = ceil(c2)
        else:
            c2 = floor(c2)

        c1 = max(low, min(c1, high))
        c2 = max(low, min(c2, high))

        # print(p1, p2, c1, c2)
        return [int(c1), int(c2)]

    def getbeta(Anand, a, b):
        u = random.random()
        # print(u)
        if u < 0.5:
            beta = a - b * log(u)
        else:
            beta = a + b * log(u)

        return beta

    def mutate(Anand, member):
        mut_member = np.zeros_like(member)
        for i in range(len(member)):
            if GV.participation_flag[i] != 1 or random.random() > Anand.pm:
                mut_member[i] = member[i]
            else:
                low = Anand.lowb[i]
                high = Anand.highb[i]
                j = random.randint(0, len(member)-1)
                mut_member[i] = max(low, min(member[j], high))
        return mut_member

    def eval_pop(Anand):
        tmp = np.array(GV.volume_dates)
        for i in range(Anand.popsize):
            # GV.volume_pickup_dates = tmp[Anand.state[:]]
            for c in range(GV.num_of_contries):
                GV.pricevol[c] = tmp[Anand.pop[i][c]]
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
            Anand.fits[i] = results[-4]

        Anand.getBest()
        Anand.getWorst()
        #Anand.fits = [Anand.obj(member) for member in Anand.pop]

        # bestindex = np.argmax(Anand.fits)
        # bestmember = Anand.pop[bestindex]
        # bestfitness = Anand.fits[bestindex]
        # if bestfitness > Anand.bestfityet:
        #     Anand.bestfityet = bestfitness
        #     Anand.bestmemyet = bestmember
        # print("Current best: ", bestfitness, "Best yet: ", Anand.bestfityet)
        # print("Best Solution Found so far:", Anand.bestmemyet)

    def getBest(Anand):
        Anand.bestIndex = np.argmax(Anand.fits)
        bestmember = Anand.pop[Anand.bestIndex]
        Anand.currentbest = Anand.fits[Anand.bestIndex]
        if Anand.currentbest > Anand.bestsofar:
            Anand.bestsofar = Anand.currentbest
            Anand.bestmemyet = bestmember
        # print("Current best: ", Anand.currentbest, "Best yet: ", Anand.bestsofar)
        # print("Best Solution Found so far:", Anand.bestmemyet)

    def getWorst(Anand):
        Anand.worstIndex = np.argmin(Anand.fits)
        worstmember = Anand.pop[Anand.worstIndex]
        Anand.currentworst = Anand.fits[Anand.worstIndex]
        if Anand.currentworst < Anand.worstsofar:
            Anand.worstsofar = Anand.currentworst
            Anand.worstmemyet = worstmember
            # print("Current worst: ", worstfitness, "Worst yet: ", Anand.worstfityet)

    def pop_print(Anand):
        for i in range(Anand.popsize):
            print(i, Anand.pop[i], Anand.fits[i])
            # print(i,Anand.fits[i])
        return