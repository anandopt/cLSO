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
import csv

class SA: # popsize must be multiple of 4
    def __init__(Anand, dfA, perturbations):
        Anand.perturbs = perturbations
        Anand.dim = len(dfA)
        Anand.dfA = dfA
        Anand.A = np.empty((Anand.perturbs, Anand.dim), dtype=dfA.dtype)   ##### dimension is perturbations X 61
        Anand.fA = np.zeros(Anand.perturbs, dtype=float)                    #####dimension is perturbations
        # Anand.B = np.zeros((Anand.perturbs, Anand.dfB.shape[1] - 1), dtype=int)   #####dimension is perturbations X 61
        # Anand.fB = np.zeros(Anand.perturbs, dtype=float)                    #####dimension is perturbations
        # Anand.C = np.zeros((Anand.dfB.shape[1] - 1, Anand.perturbs, Anand.dfB.shape[1] - 1), dtype=int)
        #                                                     ##### dimension is perturbations X 61 X perturbations
        # Anand.fC = np.zeros((Anand.dfB.shape[1] - 1, Anand.perturbs), dtype=float)
        #                                                     #####dimension is 61 X perturbations
        Anand.Analysis()
        # Anand.ComputeSensitivityIndices()

    def Analysis(Anand):
        for con in range(1, Anand.dim+1):

            fname = 'sensitiviti_analysis_' + str(con-1) + '.csv'
            csvfile = open(fname, 'w', newline='')
            genfile = csv.writer(csvfile)

            for i in range(Anand.perturbs):
                Anand.A[i,0:con-1] = Anand.dfA[0:con-1]
                move = int(Anand.perturbs/2) - i
                if move < 0:
                    Anand.A[i,con-1] = CU.Datediff(Anand.dfA[con-1],move)
                else:
                    Anand.A[i, con-1] = CU.Datesum(Anand.dfA[con-1], move)
                if CU.Lesser(Anand.A[i,con-1], GV.volume_dates[GV.dmin[con-1]]):
                    Anand.A[i, con-1] = GV.volume_dates[GV.dmin[con-1]]
                if not CU.LesserOrEqual(Anand.A[i, con-1], GV.volume_dates[GV.dmax[con-1]]):
                    Anand.A[i, con-1] = GV.volume_dates[GV.dmax[con-1]]
                Anand.A[i,con:Anand.dim] = Anand.dfA[con:Anand.dim]
                GV.pricevol = Anand.A[i,:]
                for d in range(len(GV.datediff[con-1])):
                    if GV.datediff[con-1][0] < 0:
                        GV.dossier_submission_date[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][0])
                    else:
                        GV.dossier_submission_date[con-1] = CU.Datesum(GV.pricevol[con-1], GV.datediff[con-1][0])

                    if GV.datediff[con-1][1] < 0:
                        GV.price_approval_date[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][1])
                    else:
                        GV.price_approval_date[con-1] = CU.Datesum(GV.pricevol[con-1], GV.datediff[con-1][1])

                    if GV.datediff[con-1][2] < 0:
                        GV.price_publication_date[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][2])
                    else:
                        GV.price_publication_date[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][2])

                    if GV.datediff[con-1][3] < 0:
                        GV.reimbursement_date[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][3])
                    else:
                        GV.reimbursement_date[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][3])

                    if GV.datediff[con-1][4] < 0:
                        GV.volume_pickup_dates[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][4])
                    else:
                        GV.volume_pickup_dates[con-1] = CU.Datediff(GV.pricevol[con-1], GV.datediff[con-1][4])
                # if con == 34 and i == 5:
                #     print('Here')
                # print(con, i)
                results = REV.GetRevenue()
                Anand.fA[i] = results[-4]
                k = Anand.A[:,[con - 1]]
                # print(k)
            genfile.writerows(np.column_stack((Anand.A, Anand.fA)))
        return

        # for i in range(Anand.perturbs):
        #     randomloc = random.randint(0, Anand.dfB.shape[0]-1)
        #     Anand.B[i,0:Anand.dfB.shape[1]-1] = Anand.dfB.iloc[randomloc, 0:Anand.dfB.shape[1]-1]
        #     Anand.fB[i] = Anand.dfB.iloc[randomloc, Anand.dfB.shape[1]-1]
        #
        #     Anand.C = np.zeros((Anand.dfB.shape[1]-1,Anand.perturbs,Anand.dfB.shape[1]-1), dtype=int)
        #
        # for block in range(Anand.dfB.shape[1]-1):
        #     if block == 0:
        #         Anand.C[block,:,:] = np.column_stack((Anand.A[:,block], Anand.B[:,block+1:]))
        #     else:
        #         Anand.C[block,:,:] = np.column_stack((Anand.B[:,:block], Anand.A[:,block], Anand.B[:,block+1:]))
        #     for pop in range(len(Anand.A)):
        #         candidates = Anand.C[block,pop,:]
        #         # print(candidates)
        #         GV.periodicity_date = candidates
        #         dateprice, netdateprice, revenue, overallRevenue, monthlyRevenue, netrevenue, Anand.fC[block,pop], netmonthlyRevenue, countryRevenue, volumes = REV.GetRevenue(candidates)
        # print(Anand.fC)

    def ComputeSensitivityIndices(Anand):

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









