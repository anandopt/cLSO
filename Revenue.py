import math
import priceEvolution as PE
import globvar as GV
# import csv
import numpy as np
from time import clock as ck
from scipy import stats

def GetRevenue():
    # tk = ck()
    dateprice, netprices, irpdates = PE.PriceEvolution()
    # ek = ck() - tk
    first_irp_date = []
    # volumes = GV.base_volume, coggs = GV.coggs, royalties = GV.royalties, WACC = GV.WACC, volume_dates = GV.volume_dates

    for i in range(len(irpdates)):
        if len(irpdates[i]) > 0:
            first_irp_date.append(irpdates[i][0])
        else:
            first_irp_date.append('')

    royalties = GV.royalties
    coggs = GV.coggs
    WACC = GV.WACC

    volumes = AdjustVolume()

    netrevenue          = np.zeros((GV.num_of_contries, GV.irp_time_frame), dtype=float)
    monthlyRevenue      = np.zeros(GV.irp_time_frame)
    netmonthlyRevenue   = np.zeros(GV.irp_time_frame)
    countryRevenue      = np.zeros(GV.num_of_contries)
    # netcountryRevenue   = [0 for i in range(len(volumes))]
    netoverallRevenue   = 0
    # overallRevenue      = 0

    startyear = int(GV.volume_dates[0][3:])
    revenue = []
    for date in range(len(netprices[0])):
        currentyear = int(GV.volume_dates[date][3:])

        for contry in range(len(netprices)):
            revenue.append([])
            if (netprices[contry][date]=='' or netprices[contry][date]==0) or volumes[contry][date]=='':
                tmp1 = 0
            else:
                if royalties[contry][date] == '':
                    royalties[contry][date] = 0
                if coggs[contry][date] == '':
                    coggs[contry][date] = 0
                # tmp2 = netprices[contry][date]*volumes[contry][date]
                # tmp3 = tmp2 * (100 - royalties[contry][date])/100
                # tmp4 = tmp3 - volumes[contry][date]*coggs[contry][date]
                # tmp1 = tmp4 * math.pow((1 - WACC/100),(currentyear-startyear))  ## math.pow((1/(1 - WACC/100)),(currentyear-startyear))

                tmp1 = (netprices[contry][date] * (100 - royalties[contry][date]) / 100 * volumes[contry][date] -
                        volumes[contry][date] * coggs[contry][date]) * math.pow(1/(1 + WACC / 100), (
                currentyear - startyear))  ## math.pow((1/(1 - WACC/100)),(currentyear-startyear))
                # print(tmp1)'
            revenue[contry].append(tmp1)
            netrevenue[contry][date] = tmp1
            netmonthlyRevenue[date] += tmp1
            netoverallRevenue += tmp1
        #####End for contry
    #####End for date

    # for contry in range(len(netprices)):
    #     countryRevenue[contry] = sum(netrevenue[contry])
    countryRevenue = netrevenue.sum(axis=1)
    # overallRevenue = sum(map(sum, revenue))
    # netoverallRevenue = sum(map(sum, netrevenue))
    # print(countryRevenue)
    return dateprice, netprices, revenue, netmonthlyRevenue, netoverallRevenue, netmonthlyRevenue, countryRevenue, volumes
#####End GetRevenue module

def AdjustVolume():
    #print(len(first_irp_date), len(volumes), len(volume_dates))
    # print(first_irp_date)
    # print(GV.price_publication_date)
    # unique, counts = np.unique(volumes[:], return_counts=True)
    # k = np.sum(counts)
    # print(k)
    # m = stats.itemfreq(volumes[:])
    # new_volume = []
    # lengthv = []
    new_volume = []
    # blank = np.where(new_volume == '')
    # new_volume[blank] = 0
    # new_volume = new_volume.astype(np.float)
    for contry in range(len(GV.base_volume)):
        # if contry == 26:
        #     print(GV.countries[contry])
        new_volume.append([])
        for date in range(len(GV.base_volume[contry])):
            if GV.base_volume[contry][date] != '':
                new_volume[contry].append(GV.base_volume[contry][date])

    nvolumes = np.zeros((GV.num_of_contries, GV.irp_time_frame))

    l = np.zeros(GV.num_of_contries, dtype=int)
    for contry in range(GV.num_of_contries):
        l[contry] = np.count_nonzero(new_volume[contry])

    for contry in range(GV.num_of_contries):
        if l[contry] == 0:
            continue

        startindex = int(np.where(GV.volume_dates == GV.volume_pickup_dates[contry])[0])
        if (startindex + l[contry]) < GV.irp_time_frame:
            for date in range(startindex, startindex + l[contry]):
                nvolumes[contry][date] = new_volume[contry][date - startindex]
            for date in range(startindex + l[contry], GV.irp_time_frame):
                nvolumes[contry][date] = new_volume[contry][len(new_volume[contry])-1]
        else:
            for date in range(startindex, GV.irp_time_frame):
                nvolumes[contry][date] = new_volume[contry][date - startindex]

    return(nvolumes)