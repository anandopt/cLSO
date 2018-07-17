from __future__ import print_function

import datetime, csv
import pandas as pd
import numpy as np
import writeOutput as WO
import Revenue as REV
import globvar as GV
import cLSOutilities as CU
import VarInit as VI
import GAAKS as ga
import Anealing as sa
import os.path
import pathlib
import sensitivityAnalysis_Saltelli as SS
import sensitivityAnalysis_Morris as SM
import xlrd, xlwt
from xlwt import easyxf as ezxf
import distutils.dir_util



# from matplotlib import pylab
# import numpy as np
# %pylab

dateprice   =[]
netdateprice=[]
revenue     =[]
netrevenue  =[]

#----------------------------------------------------------------------
#----------------------------------------------------------------------
##########                   Main function                   ##########
#----------------------------------------------------------------------
#----------------------------------------------------------------------

def document_info():
    """
    
        This software finds the optimal launch sequence of a product in various market
    in order to obtain maximum revenue while complying with all the market restrictions
    and requirements.

        In order to find optimal launch sequence, various optimization algorithms, including
    Genetic Algorithm, Simulated Annealing, Ant Colony Optimization, etc. is applied with
    overall revenue over the period of 10 years as fitness value. The efficiency and accuracy of
    different algorithms are also compared.

    Input:  Input excel file

    Output: 1. Appropriate prices in all the participating markets
            2. 10 years revenue based on the given informatio
            3. Statistics of the results e.g., revenue obtained from the product
               in each month throughout the duration of analysis.
    """

def CreateExcel(filename):
    ##### This function creates the required workbook if workbook is not already exists
    # and adds required sheets to the workbook

    # workbook = xlsxwriter.Workbook(filename)
    if os.path.isfile(filename):
        print("File exists")
    else:
        print("File to be created")
        workbook2 = xlwt.Workbook(filename)
        ws = workbook2.add_sheet('Prices')
        ws = workbook2.add_sheet('Net Prices')
        ws = workbook2.add_sheet('Revenues')
        ws = workbook2.add_sheet('Net Revenues')
        ws = workbook2.add_sheet('Volumes')
        ws = workbook2.add_sheet('Statistics')
        workbook2.save(filename)
    book = xlrd.open_workbook(filename)
    sheet_names = book.sheet_names()
    print(sheet_names)

if __name__ == "__main__":

    print(document_info.__doc__)

    ipath = os.path.join(os.getcwd(), 'Input', 'Input file.xlsx')
    xl_workbook = VI.open_file(ipath)

###############################################################################################
    # print('Fetching data from InputInterface')
    # Fetch participating countries into list "countries".
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_InputInterface(GV.xl_sheet[0], col_id)

################################################################################################
    ############################################################################################
    # Fetching "Country Participation" data from "Index"
    ############################################################################################
    # Fetch flag value expressing countries participating into IRP into list "participation_flag".
    row_id = 5  # row number from which values are to be fetched
    col_id = 8  # column number from which values are to be fetched
    VI.fetch_participation_flag(GV.xl_sheet[1], row_id, col_id)
################################################################################################

    ############################################################################################
    # Fetching "Referencing Strategy" data from "MultipleFixedReference"
    ############################################################################################
    # Fetch primary at launch basket flag for countries in the list "basket_flag_primary_al"
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_MultipleFixedReference(GV.xl_sheet[2], col_id)
################################################################################################

    ############################################################################################
    # Fetching "Country Baskets" data from "CountryBasket"
    ############################################################################################
    # Fetch primary at launch basket flag for countries in the list "basket_flag_primary_al"
    row_id = 10    # row number from which values are to be fetched
    col_id = 4      # column number from which values are to be fetched
    VI.fetch_CountryBasket(GV.xl_sheet[3], col_id)
################################################################################################

    ############################################################################################
    # Fetching "Country Baskets" data from "BaseVolumeForecast"
    ############################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 9  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_BaseVolumeForecast(GV.xl_sheet[4], col_id)
################################################################################################

    #############################################################################################
    #############################################################################################
    # Fetching "Referencing Strategy" from "PriceOverrideAndProdDiscd"
    ##############################################################################################
    ##############################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_PriceOverrideAndProdDiscd(GV.xl_sheet[5], col_id)
################################################################################################

    ################################################################################################
    ###################################################################################################
    # Fetching "Referencing Strategy" from "PriceOverrideAndProdDiscd"
    ###################################################################################################
    ################################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_PriceCut(GV.xl_sheet[6], col_id)
################################################################################################

    ################################################################################################
    ###################################################################################################
    # Fetching "Discount information" from "DiscountLevel"
    ###################################################################################################
    ################################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_DiscountLevel(GV.xl_sheet[7], col_id)

################################################################################################

    ################################################################################################
    ################################################################################################
    ###################################################################################################
    # Fetching "Discount information" from "MultipleDelay"
    ###################################################################################################
    ################################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_MultipleDelay(GV.xl_sheet[8], col_id)
################################################################################################

    ################################################################################################
    ################################################################################################
    ###################################################################################################
    # Fetching "Coggs and Royalties" from "CogsAndRoyalties"
    ###################################################################################################
    ################################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_CogsAndRoyalties(GV.xl_sheet[9], col_id)
################################################################################################

    ################################################################################################
    ################################################################################################
    ###################################################################################################
    # Fetching "max and min bounds on dates" from "SimulatedAnnealing"
    ###################################################################################################
    ################################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 6  # row number from which values are to be fetched
    col_id = 9  # column number from which values are to be fetched
    VI.fetch_SimulatedAnnealing(GV.xl_sheet[10], row_id, col_id)

################################################################################################

    ################################################################################################
    ################################################################################################
    ###################################################################################################
    # Fetching "Price Levels information" from "PriceLevels"
    ###################################################################################################
    ################################################################################################
    # Fetch volume pickup Dates into list "volume_dates" and corresponding
    # volumes in various countries in that months.
    row_id = 10  # row number from which values are to be fetched
    col_id = 4  # column number from which values are to be fetched
    VI.fetch_PriceLevels(GV.xl_sheet[11], col_id)

################################################################################################


    print('IRP process starts...')
    #volume,dateprice,netdateprice,coggs,royalties,WACC = PriceEvolution()
    #pprint.pprint(volume)
    #pprint.pprint(dateprice)
    #####PriceEvolution function returns " GV.base_volume, dateprice, netdateprice, GV.coggs, GV.royalties, GV.WACC, GV.volume_dates "
    # dateprice, netdateprice, revenue, overallRevenue, monthlyRevenue, netrevenue, netoverallRevenue, netmonthlyRevenue, countryRevenue, volumes = REV.GetRevenue(GV.irp_from_date, runmode)#dateprice, netdateprice, volume, coggs, royalties, WACC)

 ################################################################################################

    ##### Getting differences between various dates. Differences are taken from launch dates or volume pickup dates
    VI.GetDifferences()
################################################################################################
    # tmp = [2, 9, 13, 10, 2, 13, 2, 9, 5, 7, 15, 19, 4, 4, 12, 10, 9, 9, 3, 2, 13, 12, 5, 6, 3, 11, 1, 13, 1, 13, 21, 22, 11, 7, 6, 17, 11, 28, 28, 3, 8, 6, 16, 15, 10, 1, 39, 21, 30, 15, 2, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1]
    # GV.pricevol = GV.volume_dates[tmp]
    # for c in range(GV.num_of_contries):
    #     # if c== 32:
    #     #     print("Here")
    #     for d in range(len(GV.datediff[c])):
    #         if GV.datediff[c][0] < 0:
    #             GV.dossier_submission_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][0])
    #         else:
    #             GV.dossier_submission_date[c] = CU.Datesum(GV.pricevol[c], GV.datediff[c][0])
    #
    #         if GV.datediff[c][1] < 0:
    #             GV.price_approval_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][1])
    #         else:
    #             GV.price_approval_date[c] = CU.Datesum(GV.pricevol[c], GV.datediff[c][1])
    #
    #         if GV.datediff[c][2] < 0:
    #             GV.price_publication_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][2])
    #         else:
    #             GV.price_publication_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][2])
    #
    #         if GV.datediff[c][3] < 0:
    #             GV.reimbursement_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][3])
    #         else:
    #             GV.reimbursement_date[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][3])
    #
    #         if GV.datediff[c][4] < 0:
    #             GV.volume_pickup_dates[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][4])
    #         else:
    #             GV.volume_pickup_dates[c] = CU.Datediff(GV.pricevol[c], GV.datediff[c][4])

    #GV.pricevol = GV.volume_dates[tmp]
    # GV.pricevol = ['03-2018', '10-2018', 	'02-2019',	'11-2018', 	'03-2018','02-2019', '03-2018', 	'10-2018', 	'06-2018', 	'08-2018', 	'04-2019',	'08-2019',	'05-2018', 	'05-2018', 	'01-2019',	'11-2018', 	'10-2018', 	'10-2018', 	'04-2018', 	'04-2018', 	'02-2019',	'01-2019',	'06-2018', 	'07-2018', 	'04-2018', 	'12-2018', 	'02-2018', 	'02-2019',	'02-2018', 	'02-2019',	'10-2019',	'11-2019',	'10-2018', 	'07-2018', 	'07-2018', 	'06-2019',	'02-2018', 	'05-2020',	'05-2020',	'04-2018', 	'09-2018', 	'07-2018', 	'05-2019',	'04-2019',	'11-2018', 	'05-2018', 	'04-2021',	'10-2019',	'07-2020',	'04-2019',	'03-2018', 	'02-2019',	'02-2018', 	'11-2018', 	'02-2018', 	'02-2020',	'02-2018', 	'02-2018', 	'10-2019',	'02-2019',	'02-2018']
    dateprice, netdateprice, revenue, netmonthlyRevenue, netoverallRevenue, netmonthlyRevenue, countryRevenue, volumes = REV.GetRevenue()  # dateprice, netdateprice, volume, coggs, royalties, WACC)
    # print(len(revenue[0]))
    # print(len(revenue))
    # print(GV.multiplier_factor)
    mkd = datetime.date
    hdngs1 = ['01-'+s for s in GV.volume_dates]
    hdngs2 = GV.countries[:]
    kinds = 'date    text          int         price         money    text'.split()
    #data = dateprice

    heading_xf = ezxf('font: bold on; align: wrap on, vert centre, horiz center')
    kind_to_xf_map = {
        'date': ezxf(num_format_str='dd-mm-yyyy'),
        'int': ezxf(num_format_str='#,##0'),
        'money': ezxf('font: italic on; pattern: pattern solid, fore-colour grey25', num_format_str='$#,##0.00'),
        'price': ezxf(num_format_str='#0.000000'),
        'text': ezxf(),
    }

    # distutils.dir_util.mkpath(path)
    ##### Creates necessary folders required to store output
    pathlib.Path('Output/Genetic').mkdir(parents=True, exist_ok=True)
    pathlib.Path('Output/Simulated').mkdir(parents=True, exist_ok=True)

    data_xfs = [kind_to_xf_map[k] for k in kinds]
    opath = os.path.join(os.getcwd(), 'Output', 'price_evolution.xls')
    #write_xls(opath, 'Results', dateprice)
    # WO.write_xls(opath, 'Prices', dateprice, 'Net Prices', netdateprice, 'Revenues', revenue, 'Net Revenues', netrevenue, 'Volumes', volumes, hdngs1, hdngs2, heading_xf, data_xfs, monthlyRevenue, overallRevenue, netoverallRevenue, countryRevenue, 'Statistics')

    CreateExcel(opath)          ##### Creates necessary output file and adds required sheets
    WO.write_xls(opath, 'Prices', dateprice, 'Net Prices', netdateprice, 'Revenues', revenue, 'Volumes', volumes,
                 hdngs1, hdngs2, heading_xf, data_xfs, netmonthlyRevenue, netoverallRevenue, countryRevenue,
                 'Statistics')
    print('Price evolution is completed and results are written on "'+opath+'"...')

    print('Run optimization: Y/N')
    optrun = input()
    if optrun.lower() == 'y':
        print('Optimization process is running...')
        # ga = GA(square, dim=2, popsize=40, ngen=50, pc=0.9, pm=0.1, etac=2, etam=100)

        dim = GV.num_of_contries
        popsize = 20
        ngen = 5
        nrun = 10

        ##### Calls Genetic algorithm
        print('Press G/g to Run Genetic Algorithm and S/s to run Simulated Annealing Algorithm')
        optrun = input()
        if optrun.lower() == 'g':
            print("Genetic algorithm is running")
            gc = ga.GA(REV.GetRevenue, dim, popsize, ngen, pc=0.9, pm=0.1, etac=2, etam=100, aa=0, bb=0.5)
        ##### Calls Simulated Annealing algorithm
        if optrun.lower() == 's':
            print("Simulated Annealing algorithm is running")
            gc = sa.Annealing(REV.GetRevenue, GV.num_of_contries, ngen)

        gc.setbounds(GV.dmin, GV.dmax)
        for run in range(nrun):
            seed = int(run*10+999)
            print(seed, gc.run(run, seed))
    else:
        pass

    print('Run sensitivity analysis: Y/N')
    optrun = input()
    if optrun.lower() == 'y':
        print('Sensitivity analysis is running...')
        print('Press S/s to apply Saltelli method for sensitivity anlysis and M/m to apply Morris method.')
        optrun = input()
        if optrun.lower() == 's':
            print('Method proposed by Saltelli (2002)')
            ipath = os.path.join(os.getcwd(), 'old run', 'analysis.csv')
            ipath_1 = os.path.join(os.getcwd(), 'old run', 'analysis_1.csv')
            perturbations = 1000
            dfA = pd.read_csv(ipath, sep=',', header=None)
            dfB = pd.read_csv(ipath_1, sep=',', header=None)
            ss = SS.SA(dfA, dfB, perturbations)

        if optrun.lower() == 'm':
            print('Method proposed by Morris (1991)')
            ipath = os.path.join(os.getcwd(), 'old run', 'analysis.csv')
            ipath_1 = os.path.join(os.getcwd(), 'old run', 'analysis_1.csv')
            perturbations = 10
            dfA = np.array(['03-2018', 	'10-2018', 	'02-2019',	'11-2018', 	'03-2018',	'02-2019',	'03-2018', 	'10-2018', 	'06-2018', 	'08-2018', 	'04-2019',	'08-2019',	'05-2018', 	'05-2018', 	'01-2019',	'11-2018', 	'10-2018', 	'10-2018', 	'04-2018', 	'04-2018', 	'02-2019',	'01-2019',	'06-2018', 	'07-2018', 	'04-2018', 	'12-2018', 	'02-2018', 	'02-2019',	'02-2018', 	'02-2019',	'10-2019',	'11-2019',	'10-2018', 	'07-2018', 	'07-2018', 	'06-2019',	'02-2018', 	'05-2020',	'05-2020',	'04-2018', 	'09-2018', 	'07-2018', 	'05-2019',	'04-2019',	'11-2018', 	'05-2018', 	'04-2021',	'10-2019',	'07-2020',	'04-2019',	'03-2018', 	'02-2019',	'02-2018', 	'11-2018', 	'02-2018', 	'02-2020',	'02-2018', 	'02-2018', 	'10-2019',	'02-2019',	'02-2018'])
            sm = SM.SA(dfA, perturbations)
        # dim = GV.num_of_contries
        # ngen = 1000
        #
        # gc = ga.GA(REV.GetRevenue, dim, popsize, ngen, pc=0.9, pm=0.1, etac=2, etam=100, aa=0, bb=0.5)
        # gc.setbounds(GV.dmin, GV.dmax)
        # for run in range(10):
        #     seed = int(run * 10 + 9011)
        #     print(seed, gc.run(run, seed))
    else:
        pass

    print('Process Complete...Thank you')
