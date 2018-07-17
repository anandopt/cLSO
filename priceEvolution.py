import pprint
import globvar as GV
import cLSOutilities as CU
from math import fabs
import numpy as np
# import csv
from time import clock as ck

def PriceEvolution():
    ###initialize list prices on particular date for each country
    ###price=0 indicates no price available for the corresponding country
    dateprice = np.zeros((GV.num_of_contries, GV.irp_time_frame), dtype=float)
    ######################## Finding IRP Dates of all the countries in "countryIRPDates" list ##########################
    countryIRPDates = CU.Fetch_IRPDates()
    # print(GV.countries[16], countryIRPDates[16])
    # for i in range(len(countryIRPDates[21])):
    #     print(i, GV.volume_dates.index(countryIRPDates[21][i]))
    # print(countryIRPDates[21])
    # print(len(countryIRPDates[21]), countryIRPDates[21][len(countryIRPDates[21]) - 1])
    # pprint.pprint(countryIRPDates)
    #     pprint.pprint(countryIRPDates[i])
    ##### End for loop with updated countryIRPDate

    ##### Initializing at launch prices to base prices, modified later if required
    for i in range(GV.num_of_contries):
        # print(GV.countries[noirpCountryIndex_pl[i]])
        if GV.participation_flag[i] != 1:
            continue
        # if i==32:
        #     print("Here")
        if not isinstance(GV.irp_from_date[i], str):
            alirpdate = CU.xldate_to_datetime(GV.irp_from_date[i])
        else:
            # if flag == 1:
            #     alirpdate = GV.irp_from_date[i]
            # else:
            # CU.Dates[GV.irp_from_date[i]][i]
            alirpdate = CU.Dates[GV.irp_from_date[i]][i]

        # if CU.Lesser(GV.pricevol[i], alirpdate):
        #     sl = int(np.where(GV.volume_dates == GV.pricevol[i])[0])
        # else:
        #     sl = int(np.where(GV.volume_dates == alirpdate)[0])

        dateprice[i][np.where(GV.volume_dates == GV.pricevol[i])] = GV.base_prices[i]

        if alirpdate < GV.pricevol[i]:
            continue

        # print('PE', GV.countries[i])
        # if GV.countries[i] == 'UAE':
        #     print(i)
        start = int(np.where(GV.volume_dates == GV.pricevol[i])[0])+1
        # problem is with end date
        end = int(np.where(GV.volume_dates == alirpdate)[0])+1
        for idates in range(int(np.where(GV.volume_dates == GV.pricevol[i])[0])+1,int(np.where(GV.volume_dates == alirpdate)[0])+1):
            ##### if Price override then the new price will be override price.
            if alirpdate == GV.volume_dates[np.where(GV.volume_dates == GV.pricevol[i])]:
                dateprice[i][idates] = GV.base_prices[i]
            else:
                dateprice[i][idates] = dateprice[i][idates - 1]

            # if GV.priceOverrideAndProdDiscd[i][idates] != '':
            #     dateprice[i][idates] = GV.priceOverrideAndProdDiscd[i][idates]
            #     continue
            #
            # ##### if Price cut then the new price will be as per the price cut. No IRP at this point even if scheduled
            # if GV.priceCut[i][idates] != '':
            #     dateprice[i][idates] = dateprice[i][idates - 1] * (1 - fabs(GV.priceCut[i][idates]) / 100)
            #     continue

        # dateprice[i][np.where(GV.volume_dates == alirpdate)] = GV.base_prices[i]
    # pprint.pprint(countryIRPDates[0])
    #####End for loop

    #####Getting basket countries for each country
    basket_al, bcindex_al, compulsory_bcindex_al = CU.getBasket(GV.basket_flag_primary_al, GV.basket_flag_compulsory_al)
    basket_pl, bcindex_pl, compulsory_bcindex_pl = CU.getBasket(GV.basket_flag_primary_pl, GV.basket_flag_compulsory_pl)

    # for c in range(GV.num_of_contries):
    #     with open("countrybasket2.txt", "a") as text_file:
    #         print(f"Basket GV.countries of {GV.countries[c]}: {basket[c]}", file=text_file)

    # Check for future code optimization
    # for con in range(GV.num_of_contries):
    #     if GV.irp_noirp[con] == 0 and GV.irp_noirp_pl[con] == 0:
    #         startdate = int(np.where(GV.volume_dates == GV.pricevol[con])[0])
    #         for nmonth in range(startdate,GV.irp_time_frame):
    #             dateprice[con][nmonth] = GV.base_prices[i]
    #     else:
    #         pass

    ###################### Price updated monthly for all countries ####################
    for nmonth1 in range(GV.irp_time_frame):       ##### First monthly loop
        irpdate = GV.volume_dates[nmonth1]

        # if irpdate == '09-2021':
        #     print("halt1")
        for cindex in range(GV.num_of_contries):

            if GV.participation_flag[cindex] != 1:
                continue

            ##### if the IRP date is before the first scheduled IRP date, do nothing and go for the next country

            if not isinstance(GV.irp_from_date[cindex], str):
                alirpdate = CU.xldate_to_datetime(GV.irp_from_date[cindex])
            else:
                alirpdate = CU.Dates[GV.irp_from_date[cindex]][cindex]

            if CU.Lesser(irpdate, GV.pricevol[cindex]):
                continue

            if CU.Lesser(irpdate, alirpdate):
                if dateprice[cindex][nmonth1-1] > 0:
                    dateprice[cindex][nmonth1] = dateprice[cindex][nmonth1-1]
                else:
                    continue

            ##### if Price override then the new price will be override price. No IRP at this point even if scheduled
            if GV.priceOverrideAndProdDiscd[cindex][nmonth1] != '':
                dateprice[cindex][nmonth1] = GV.priceOverrideAndProdDiscd[cindex][nmonth1]
                continue

            ##### if Price cut then the new price will be as per the price cut. No IRP at this point even if scheduled
            if GV.priceCut[cindex][nmonth1] != '':
                if irpdate == GV.pricevol[cindex]:
                    temp = GV.base_prices[cindex]
                else:
                    temp = dateprice[cindex][nmonth1-1]
                dateprice[cindex][nmonth1] = temp*(1-fabs(GV.priceCut[cindex][nmonth1])/100)
                continue

            ##### if no IRP at all, base prices will be continued through out
            if GV.irp_noirp[cindex] == 0 and GV.irp_noirp_pl[cindex] == 0:
                if dateprice[cindex][nmonth1 - 1] > 0:
                    dateprice[cindex][nmonth1] = dateprice[cindex][nmonth1 - 1]
                else:
                    dateprice[cindex][nmonth1] = GV.base_prices[cindex]
                continue

            ##### at least no IRP at launch date then price will be base price on launch date.
            if GV.irp_noirp[cindex] == 0 and irpdate == countryIRPDates[cindex][0]:
                if dateprice[cindex][nmonth1-1] > 0:
                    dateprice[cindex][nmonth1] = dateprice[cindex][nmonth1-1]
                else:
                    dateprice[cindex][nmonth1] = GV.base_prices[cindex]
                continue

            ##### Do at launch IRP and no post launch IRP
            ##### At launch price is repeated for all IRP dates after the launch date.
            if GV.irp_noirp[cindex] == 1 and (GV.irp_noirp_pl[cindex] == 0 and CU.Lesser(countryIRPDates[cindex][0], irpdate)):
                # print(dateprice[c][GV.volume_dates.index(alirpdate)])
                dateprice[cindex][nmonth1] = dateprice[cindex][np.where(GV.volume_dates == alirpdate)]
                continue

            ##### Filling prices from last IRP date to rest period of IRP duration
            if len(countryIRPDates[cindex]) > 0 and CU.Lesser(countryIRPDates[cindex][len(countryIRPDates[cindex]) - 1],irpdate):
                dateprice[cindex][nmonth1] = dateprice[cindex][nmonth1 - 1]
                continue

            ##### select date or number of IRPs of a country, whichever is lesser
            if nmonth1 < len(countryIRPDates[cindex]):
                nloops = nmonth1
            else:
                nloops = len(countryIRPDates[cindex])
            ##### End if for nloops
            priceconsdate = irpdate
            ##### Finding delay for price consideration of a country "c"
            if GV.multi_single_delay[cindex] == 1:
                if GV.multipleDelay[cindex][nmonth1] != '':
                    priceconsdate = CU.Datediff(irpdate, GV.multipleDelay[cindex][nmonth1])
            else:
                if irpdate == alirpdate:
                    priceconsdate = CU.Datediff(irpdate, GV.delay_price[cindex])
                else:
                    priceconsdate = CU.Datediff(irpdate, GV.delay_price_pl[cindex])

            if CU.Lesser(priceconsdate,GV.volume_dates[0]):
                if dateprice[cindex][nmonth1 - 1] > 0:
                    dateprice[cindex][nmonth1] = dateprice[cindex][nmonth1 - 1]
                else:
                    dateprice[cindex][nmonth1] = GV.base_prices[cindex]
                continue

            ##### End if nloops

            if irpdate == countryIRPDates[cindex][0]:
                basket, bcindex, compulsory = basket_al[cindex], bcindex_al[cindex], compulsory_bcindex_al[cindex]
            else:
                basket, bcindex, compulsory = basket_pl[cindex], bcindex_pl[cindex], compulsory_bcindex_pl[cindex]

            for nmonth2 in range(nloops):
                # print(GV.countries[c], irpdate,GV.price_publication_date[c], countryIRPDates[c][nmonth2])
                if CU.Lesser(irpdate,countryIRPDates[cindex][nmonth2]):
                    ### IRP date will lie ahead for the country and will be checked on next nmonth1
                    ### Take price from previous month and go for the next country
                    dateprice[cindex][nmonth1]=dateprice[cindex][nmonth1-1]
                    break
                elif not CU.LesserOrEqual(irpdate,countryIRPDates[cindex][nmonth2]):
                    ### In this case check for the next IRP date of the country by incrementing nmonth2
                    ### untill either first if condition is met or
                    ### the date is IRP date for the country in which case IRP will be perform
                    continue
                else:

                    ### do IRP
                    validindices    =[]
                    invalidindices  =[]
                    validprices     =[]
                    validlength     =0
                    cflag           =0

                    ### Start IRP Process
                    # print(GV.countries[cindex] + ' refers following ' + str(
                    # len(basket)) + ' GV.countries to do IRP with GV.periodicity of ' + str(GV.periodicity[cindex]) + ' and delay of ' + str(GV.delay_price[cindex]) + ' months...')
                    # print(basket)
                    # print('IRP Date is ' + irpdate + ' and price considered date is', priceconsdate)

                    ##### Finding GV.countries in the country basket which satisfy IRP vs Price publication date constraint

                    # if (GV.countries[cindex] == 'Cyprus'):
                    #     ##### Check for Austria
                    #     if not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[0]]) and dateprice[bcindex[0]][np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[0])
                    #         validprices.append(dateprice[bcindex[0]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### If Austria is not valid then check for Italy
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[2]]) and dateprice[bcindex[2]][np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[2])
                    #         validprices.append(dateprice[bcindex[2]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### Otherwise check for Belgium
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[2]]) and dateprice[bcindex[2]][np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[3])
                    #         validprices.append(dateprice[bcindex[3]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### No country has valid price
                    #     else:
                    #         invalidindices.append(bcindex[0])
                    #         invalidindices.append(bcindex[2])
                    #         invalidindices.append(bcindex[3])
                    #     ##### End if Austria####################
                    #
                    #     ##### Check for France
                    #     if not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[1]]) and dateprice[bcindex[1]][np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[1])
                    #         validprices.append(dateprice[bcindex[1]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### If France is not valid then check for Italy
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[2]]) and dateprice[bcindex[2]][np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[2])
                    #         validprices.append(dateprice[bcindex[2]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### Otherwise check for Belgium
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[2]]) and dateprice[bcindex[2]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[3])
                    #         validprices.append(dateprice[bcindex[3]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### No country has valid price
                    #     else:
                    #         invalidindices.append(bcindex[1])
                    #         invalidindices.append(bcindex[2])
                    #         invalidindices.append(bcindex[3])
                    #         # for check in [1, 2, 3]:
                    #         #     try:
                    #         #         t = compulsory.index(bcindex[check])
                    #         #     except ValueError:
                    #         #         cflag = 1
                    #         #     else:
                    #         #         pass
                    #     ##### End if France ####################
                    #
                    #     ##### Check for Greece
                    #     if not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[4]]) and dateprice[bcindex[4]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[4])
                    #         validprices.append(dateprice[bcindex[4]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### If France is not valid then check for Spain
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[5]]) and dateprice[bcindex[5]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[5])
                    #         validprices.append(dateprice[bcindex[5]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### Otherwise check for Portugal
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[6]]) and dateprice[bcindex[6]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[6])
                    #         validprices.append(dateprice[bcindex[6]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### No country has valid price
                    #     else:
                    #         invalidindices.append(bcindex[4])
                    #         invalidindices.append(bcindex[5])
                    #         invalidindices.append(bcindex[6])
                    #         # for check in [4, 5, 6]:
                    #         #     try:
                    #         #         t = compulsory.index(bcindex[check])
                    #         #     except ValueError:
                    #         #         cflag = 1
                    #         #     else:
                    #         #         pass
                    #     ##### End if Greece####################
                    #
                    #     ##### Check for Sweden
                    #     if not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[7]]) and dateprice[bcindex[7]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[7])
                    #         validprices.append(dateprice[bcindex[7]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### If France is not valid then check for Spain
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[8]]) and dateprice[bcindex[8]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[8])
                    #         validprices.append(dateprice[bcindex[8]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### Otherwise check for Portugal
                    #     elif not CU.LesserOrEqual(priceconsdate, GV.price_publication_date[bcindex[9]]) and dateprice[bcindex[9]][
                    #         np.where(GV.volume_dates == priceconsdate)]:
                    #         validindices.append(bcindex[9])
                    #         validprices.append(dateprice[bcindex[9]][np.where(GV.volume_dates == priceconsdate)])
                    #     ##### No country has valid price
                    #     else:
                    #         invalidindices.append(bcindex[7])
                    #         invalidindices.append(bcindex[8])
                    #         invalidindices.append(bcindex[9])
                    #         # for check in [7, 8, 9]:
                    #         #     try:
                    #         #         t = compulsory.index(bcindex[check])
                    #         #     except ValueError:
                    #         #         cflag = 1
                    #         #     else:
                    #         #         pass
                    #     #####End if Sweden####################
                    #     validlength = len(validprices)

                    #####Country basket for Latvia
                    # elif GV.countries[cindex] == 'Latvia':
                    if GV.countries[cindex] == 'Latvia':
                        for bc in range(len(bcindex)):
                            validindices.append(bcindex[bc])  #####index of countries of basket satisfying the date range rule
                            validprices.append(dateprice[bcindex[bc]][np.where(GV.volume_dates == priceconsdate)])##prices in the country
                        validlength = sum(1 for r in validprices if r>0)
                    #####Country basket for other than Cyprus and Latvia
                    else:
                        for bc in range(len(bcindex)):
                            c = CU.Lesser(priceconsdate, GV.price_publication_date[bcindex[bc]])
                            d = dateprice[bcindex[bc]][np.where(GV.volume_dates == priceconsdate)] == 0
                            e = not (GV.participation_flag[bcindex[bc]] == 1)
                            if (c or d) or e:
                                invalidindices.append(bcindex[bc])
                                # try:
                                #     t = compulsory.index(bcindex[bc])
                                # except ValueError:
                                #     cflag = 1
                                # else:
                                #     pass
                            else:
                                validindices.append(bcindex[bc])  #####index of countries of basket satisfying the date range rule
                                validprices.append(dateprice[bcindex[bc]][np.where(GV.volume_dates == priceconsdate)])##prices in the country
                        #####End for loop for bcindex
                        validlength = len(validprices)

                    #####Japan rule requires its older price
                    if irpdate > countryIRPDates[cindex][0]:
                        validprices.append(dateprice[cindex][nmonth1 - 1])
                    else:
                        validprices.append(GV.base_prices[cindex])
                    # print(str(validindices)+'      '+str(validprices)+'     '+str(invalidindices))

                    #####Check minimum number of countries must have valid price
                    #####If yes update price else continue at older price
                    if validlength < int(GV.min_contries_pl[cindex]) or validlength > int(GV.max_contries_pl[cindex]):  # or dateprice[bcindex[bc]][GV.volume_dates.index(priceconsdate)] == 0:
                        dateprice[cindex][nmonth1] = dateprice[cindex][nmonth1 - 1] if dateprice[cindex][nmonth1 - 1] > 0 else GV.base_prices[cindex]
                    else:
                        if irpdate == alirpdate:
                            newprice = CU.rule[GV.reference_rules[cindex]](GV.num_refrence_rule_pl, validprices, cindex)       #####see here...
                        else:
                            newprice = CU.rule[GV.reference_rules_pl[cindex]](GV.num_refrence_rule_pl, validprices, cindex)


                        if GV.price_rules_pl[cindex] == 'Minimum':
                            if dateprice[cindex][nmonth1 - 1] == 0:
                                dateprice[cindex][nmonth1] = min(newprice, GV.base_prices[cindex])
                            else:
                                dateprice[cindex][nmonth1] = min(newprice, dateprice[cindex][nmonth1 - 1])
                            #####End nonzero dateprice check
                        else:
                            dateprice[cindex][nmonth1] = newprice
                        #####End if price rules

                    break
                    #End if validlendth
                #End if comparision between irpdate and countryIRPDates

            #End for nmonth2

        #End for c
    #End nmonth1

    #####Computing net price after applying discounts
    import copy
    netdateprice = copy.deepcopy(dateprice)

    for c in range(GV.num_of_contries):
        for d in range(GV.irp_time_frame):
            if GV.discountLevel[c][d] == '':
                netdateprice[c][d] = dateprice[c][d]
            else:
                tempk = fabs(GV.discountLevel[c][d]) / 100.0
                netdateprice[c][d] = dateprice[c][d] * (1 - abs(tempk))

    # fname = 'prices_' + str(GV.pricecalled) + '.csv'
    # csvfile = open(fname, 'w+')
    # pricefile = csv.writer(csvfile)
    # pricefile.writerows(netdateprice)
    # GV.pricecalled += 1
    # csvfile.close()
    return dateprice, netdateprice, countryIRPDates ###,dateprice
#####End PriceEvolution module
