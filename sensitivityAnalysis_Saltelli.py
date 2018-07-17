# import matplotlib.pyplot as plt
from xlwt import easyxf as ezxf
import numpy as np
import pandas as pd
import os.path, random
from os.path import isfile
import xlrd
import pprint
import cLSOutilities as CU
import globvar as GV
import Revenue as REV

class SA: # popsize must be multiple of 4
    def __init__(Anand, dfA, dfB, perturbations):
        Anand.perturbs = perturbations
        Anand.dfA = dfA
        Anand.dfB = dfB
        Anand.A = np.zeros((Anand.perturbs, Anand.dfA.shape[1] - 1), dtype=int)   #####dimension is perturbations X 61
        Anand.fA = np.zeros(Anand.perturbs, dtype=float)                    #####dimension is perturbations
        Anand.B = np.zeros((Anand.perturbs, Anand.dfB.shape[1] - 1), dtype=int)   #####dimension is perturbations X 61
        Anand.fB = np.zeros(Anand.perturbs, dtype=float)                    #####dimension is perturbations
        Anand.C = np.zeros((Anand.dfB.shape[1] - 1, Anand.perturbs, Anand.dfB.shape[1] - 1), dtype=int)
                                                            #####dimension is perturbations X 61 X perturbations
        Anand.fC = np.zeros((Anand.dfB.shape[1] - 1, Anand.perturbs), dtype=float)
                                                            #####dimension is 61 X perturbations
        Anand.Analysis()
        Anand.ComputeSensitivityIndeices()

    def Analysis(Anand):
        for i in range(Anand.perturbs):
            randomloc = random.randint(0, Anand.dfA.shape[0]-1)
            Anand.A[i,0:Anand.dfA.shape[1]-1] = Anand.dfA.iloc[randomloc, 0:Anand.dfA.shape[1]-1]
            Anand.fA[i] = Anand.dfA.iloc[randomloc, Anand.dfA.shape[1]-1]

        for i in range(Anand.perturbs):
            randomloc = random.randint(0, Anand.dfB.shape[0]-1)
            Anand.B[i,0:Anand.dfB.shape[1]-1] = Anand.dfB.iloc[randomloc, 0:Anand.dfB.shape[1]-1]
            Anand.fB[i] = Anand.dfB.iloc[randomloc, Anand.dfB.shape[1]-1]

            Anand.C = np.zeros((Anand.dfB.shape[1]-1,Anand.perturbs,Anand.dfB.shape[1]-1), dtype=int)

        for block in range(Anand.dfB.shape[1]-1):
            if block == 0:
                Anand.C[block,:,:] = np.column_stack((Anand.A[:,block], Anand.B[:,block+1:]))
            else:
                Anand.C[block,:,:] = np.column_stack((Anand.B[:,:block], Anand.A[:,block], Anand.B[:,block+1:]))
            for pop in range(len(Anand.A)):
                candidates = Anand.C[block,pop,:]
                # print(candidates)
                GV.periodicity_date = candidates
                dateprice, netdateprice, revenue, overallRevenue, monthlyRevenue, netrevenue, Anand.fC[block,pop], netmonthlyRevenue, countryRevenue, volumes = REV.GetRevenue(candidates)

        # print(Anand.fC)

    def ComputeSensitivityIndeices(Anand):

        yA = Anand.fA           #####Dimension is perturbations
        yB = Anand.fB           #####Dimension is perturbations
        yC = Anand.fC           #####Dimension is 61 X perturbations
        yA_dot_yC = np.zeros(yC.shape[0])
        yB_dot_yC = np.zeros(yC.shape[0])
        S = np.zeros(yC.shape[0])
        S_T = np.zeros(yC.shape[0])

        #####Computation of f0^2
        sigma_YA = np.sum(Anand.fA)

        f0_square = (sigma_YA/Anand.fA.size)**2
        for i in range(yC.shape[0]):
            yA_dot_yC[i] = np.dot(yA, yC[i,:], out=None)
            yB_dot_yC[i] = np.dot(yB, yC[i,:], out=None)
        yA_dot_yA = np.dot(yA, yA, out=None)

        # for i in range(yC.shape[0]):
        #     for j in range(Anand.perturbs):
        #         yA_dot_yC[i] += yA.item(j) * yC.item(i,j)
        #         yB_dot_yC[i] += yB.item(j) * yC.item(i,j)
        #     yA_dot_yC[i] = yA_dot_yC[i]/Anand.perturbs
        #     yB_dot_yC[i] = yB_dot_yC[i] / Anand.perturbs
        #
        # yA_dot_yA = 0
        # for i in range(yA.size):
        #     yA_dot_yA += yA[i]*yA[i]
        # yA_dot_yA = yA_dot_yA/yA.size

        #####First order index
        for i in range(yC.shape[0]):
            S[i] = (yA_dot_yC[i] - f0_square) / (yA_dot_yA - f0_square)

        #####Total order index
        for i in range(yC.shape[0]):
            S_T[i] = 1 - ((yB_dot_yC[i] - f0_square) / (yA_dot_yA - f0_square))

        #####Calculation of probable_error
        # sigma_Ya_Yc = np.zeros(yC.shape[0])



        # f = open("Sensitivity_index.csv", "w")
        # f.write("{},{}\n".format("Si", "STi"))
        # for x in zip(S, S_T):
        #     f.write("{},{}\n".format(x[0], x[1]))
        # f.close()
        df = pd.DataFrame({"Si" : S, "STi" : S_T})
        df.to_csv("Sensitivity_index.csv", sep=",")









