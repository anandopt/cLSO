import datetime, sys
import globvar as GV

###############################################################################
###############################################################################
# Modules to fetch dates from excel sheet and convert in mm-yyyy format
###############################################################################
###############################################################################

def xldate_to_datetime(xldate):
    tempDate = datetime.datetime(1900, 1, 1)
    deltaDays = datetime.timedelta(days=int(xldate))
    secs = (int((xldate%1)*86400)-60)
    detlaSeconds = datetime.timedelta(seconds=secs)
    TheTime = (tempDate + deltaDays + detlaSeconds)
    return TheTime.strftime("%m-%Y")

def Datediff(irpDate, delay):
    month1 = int(irpDate[0:2])
    year1  = int(irpDate[3:])

    year2  = int(delay/12)
    month2 = int(abs(delay)%12)

    if month2>month1:
        year1  = year1  - 1
        month1 = month1 + 12

    retmonth = int(month1 - month2)
    retyear = int(year1 - year2)
    if retmonth == 0:
      retmonth = 12
      retyear = retyear - 1

    retdate = str('{:02d}'.format(retmonth))+'-'+str(retyear)
    return retdate

def Monthdiff(date1, date2):
    month1 = int(date1[0:2])
    year1  = int(date1[3:])

    month2 = int(date2[0:2])
    year2  = int(date2[3:])

    return ((year1-year2)*12 + (month1-month2))

def Datesum(irpDate, delay):
    month1 = int(irpDate[0:2])
    year1  = int(irpDate[3:])

    year2 = int(delay / 12)
    month2 = int(delay % 12)

    retmonth = int((month1 + month2)%12)
    retyear = int((year1 + year2) + int(month1 + month2)/12)
    if retmonth == 0:
      retmonth = 12
      retyear = retyear - 1

    retdate = str('{:02d}'.format(retmonth))+'-'+str(retyear)
    return retdate

def LesserOrEqual(date1, date2):
    month1 = int(date1[0:2])
    year1 = int(date1[3:])

    month2 = int(date2[0:2])
    year2 = int(date2[3:])

    if(year1 < year2):
        return True
    elif(year1 == year2):
        if(month1<=month2):
            return True
    else:
        return False

def Lesser(date1, date2):
    month1 = int(date1[0:2])
    year1 = int(date1[3:])

    month2 = int(date2[0:2])
    year2 = int(date2[3:])

    if(year1 < year2):
        return True
    elif(year1 == year2):
        if(month1 < month2):
            return True
    else:
        return False

###########################Defining IRP Rules####################################
def Minimum(num_refrence_rule_pl, list, n):
    newlist = list[:len(list) - 1]
    return min(i for i in newlist if i>0)

def Average(num_refrence_rule_pl, list, n=0):    ###returns average of non zero values
    newlist = list[:len(list) - 1]
    temp=[i for i in newlist if i]
    return sum(temp, 0.0)/len(temp)

def FreePrice(num_refrence_rule_pl, list, n):
    newlist = list[:len(list) - 1]
    return list[-1]

def CyprusRule(num_refrence_rule_pl, list, n):
    # newlist = list[:len(list) - 1]
    # avgprice=Average(num_refrence_rule_pl,newlist)
    # result1 = avgprice + 0.03 * avgprice
    # result = result1 - 0.085 * result1
    # return result  # Average(num_refrence_rule_pl,list)
    list1 = sorted(list)
    return AvgOfXLowest(4, list1)

def AvgOfXLowest(num_refrence_rule_pl, list, n=0):
    newlist = list[:len(list) - 1]
    temp = [i for i in newlist if i]
    sortedtemp = sorted(temp)
    lsize = num_refrence_rule_pl[n] if len(newlist) > num_refrence_rule_pl[n] else len(newlist)
    return sum(sortedtemp[:int(num_refrence_rule_pl[n])])/lsize

def Average_X(num_refrence_rule_pl, list, n):
    newlist = list[:len(list) - 1]
    return Average(num_refrence_rule_pl, newlist)*(100+num_refrence_rule_pl[n])/100

def JapanRule(num_refrence_rule_pl, list, n):
    newlist = list[:len(list) - 1]
    if len(list) <= 1:
        return list[-1]
    avglist = sum(newlist) / int(len(newlist))
    if list[-1] < 0.75 * avglist:
        #####Increase the price
        nprice = 1/3 * list[-1] + 1/2 * avglist
    elif list[-1] > 1.25 * avglist:
        #####Decrease the price
        nprice = 1/3 * list[-1] + 5/6 * avglist
    else:
        nprice = list[-1]
    # else:
    #     diff = max(newlist) - min(newlist)
    #     if diff > 3 * min(newlist):
    #         nprice = list[-1]
    #     else:  #####Japan’s IRP price = (1/3 x In-market price) + (1/2 x Average foreign price)
    #         nprice = 1 / 3 * list[-1] + 1 / 2 * avglist
    return nprice


def LatviaRule(num_refrence_rule_pl, list, n):
    newlist = list[:len(list) - 1]
    list1 = [val for val in list[:int(len(newlist) - 2)] if val > 0]
    list1 = sorted(list1)
    list2 = newlist[int(len(newlist) - 2):]
    if len(list1)>0:
        if len(list1) == 1:
            list2.append(list1[0])
        elif len(list1) == 2:
            list2.append(list1[1])
        else:
            list2.append(list1[2])
    result = min(i for i in list2 if i > 0)
    return result

def GermanyRule(num_refrence_rule_pl, list, n):
    newlist = list[:len(list) - 1]
    print('Need to define Germany rule')

#########################################################################################

#####Dictionary of referencing rules
rule = {'Minimum': Minimum, 'max': max, 'Average': Average, 'AvgOfXLowest': AvgOfXLowest, 'LatviaRule': LatviaRule, 'Average_X': Average_X,
            'JapanRule': JapanRule, 'Free Price': FreePrice, 'CyprusRule':CyprusRule, 'GermanyRule':GermanyRule}

#####Dictionary of price application dates
# Dates = {'Dossier Submission Date': GV.dossier_submission_date, 'Submission Date': GV.dossier_submission_date, 'Price Approval Date': GV.price_approval_date,
#              'Price Publication Date': GV.price_publication_date, 'Reimbursement Date': GV.reimbursement_date,
#              'Launch Date': GV.volume_pickup_dates, '':GV.pricevol}

Dates = {'Dossier Submission Date': GV.dossier_submission_date, 'Submission Date': GV.dossier_submission_date, 'Price Approval Date': GV.price_approval_date,
             'Price Publication Date': GV.price_publication_date, 'Reimbursement Date': GV.reimbursement_date,
             'Launch Date': GV.price_publication_date, '':GV.pricevol}

###########################################################################################

def Fetch_IRPDates():
    countryIRPDates=[]
    for i in range(GV.num_of_contries):
        countryIRPDates.append([])
        #####Goto next country if country is not participating in the market
        ####At Launch
        if GV.irp_from_date[i] == '' or GV.participation_flag[i] != 1:
            continue

        #####Decide the at launch date of IRP
        if not isinstance(GV.irp_from_date[i], str):
            irpstartdate_al = xldate_to_datetime(GV.irp_from_date[i])
        else:
            irpstartdate_al = Dates[GV.irp_from_date[i]][i]

        countryIRPDates[i].append(irpstartdate_al)

        #####Post Launch
        if GV.periodicity[i] == 0 or GV.periodicity[i] == '':
            continue
        #####End if

        if not isinstance(GV.periodicity_date[i], str):
            irpstartdate_pl = xldate_to_datetime(GV.periodicity_date[i])
        else:
            # if flag == 1:
            #     irpstartdate_pl = GV.periodicity_date[i]
            # else:
            irpstartdate_pl = Dates[GV.periodicity_date[i]][i]
        if Lesser(irpstartdate_pl, irpstartdate_al):
            print('Dates are not correct...')
            print('Post launch IRP is not possible before at launch IRP date...')
            sys.exit()

        if irpstartdate_al != irpstartdate_pl:
            countryIRPDates[i].append(irpstartdate_pl)
            k=1
        else:
            k=0

        # print(countries[i],countryIRPDates[i][0])
        last_date = GV.volume_dates[GV.irp_time_frame - 1]
        #####Finding post launch IRP dates
        #####Including dates when referencing rule is 'fixed'
        if GV.referencing_period_rule_pl[i] == 'Fixed':
            for k1 in range(GV.irp_time_frame):
                if GV.fixed_irp_dates[i][k1] == 1:
                    countryIRPDates[i].append(GV.volume_dates[k1])
        else:
            # k = 1
            while True:
                newIRPDate = Datesum(countryIRPDates[i][k], GV.periodicity[i])
                if LesserOrEqual(newIRPDate, last_date):
                    countryIRPDates[i].append(newIRPDate)
                else:
                    break
                k += 1
            #####End while loop with updated countryIRPDates
            if GV.referencing_period_rule_pl[i] == 'Both':
                for dindex in range(GV.irp_time_frame):
                    if GV.fixed_irp_dates[i][dindex] == 1:
                        ddate = GV.volume_dates[dindex]
                        for iindex in range(len(countryIRPDates[i])):
                            if Lesser(ddate, countryIRPDates[i][iindex]):
                                countryIRPDates[i] = countryIRPDates[i][:iindex] + [ddate] + countryIRPDates[i][
                                                                                                 iindex:]
                            else:
                                continue
    return countryIRPDates

def getBasket(basket_flag, basket_flag_compulsory):
    basket = []
    bcindex = []
    compulsory_bcindex = []
    for c in range(GV.num_of_contries):
        basket.append([])
        bcindex.append([])

        ###Finding countries in the basket of country "c" and their indexes in countries list
        ###Finding basket with division M, L and H for Cyprus
        if (GV.countries[c] == 'Cyprus'):

            basket[c].append('Austria')
            bcindex[c].append(GV.countries.index('Austria'))

            basket[c].append('France')
            bcindex[c].append(GV.countries.index('France'))

            basket[c].append('Italy')
            bcindex[c].append(GV.countries.index('Italy'))

            basket[c].append('Belgium')
            bcindex[c].append(GV.countries.index('Belgium'))

            basket[c].append('Greece')
            bcindex[c].append(GV.countries.index('Greece'))

            basket[c].append('Spain')
            bcindex[c].append(GV.countries.index('Spain'))

            basket[c].append('Portugal')
            bcindex[c].append(GV.countries.index('Portugal'))

            basket[c].append('Sweden')
            bcindex[c].append(GV.countries.index('Sweden'))

            basket[c].append('Denmark')
            bcindex[c].append(GV.countries.index('Denmark'))

            basket[c].append('Germany')
            bcindex[c].append(GV.countries.index('Germany'))

        ###Finding basket for Latvia
        elif GV.countries[c] == 'Latvia':
            for nc in range(GV.num_of_contries):
                if basket_flag[nc][c] == 1 and GV.countries[nc] != 'Estonia' and GV.countries[nc] != 'Lithuania':
                    basket[c].append(GV.countries[nc])
                    bcindex[c].append(nc)  ##finding index of basket countries in countries list
            basket[c].append('Estonia')
            bcindex[c].append(GV.countries.index('Estonia'))
            basket[c].append('Lithuania')
            bcindex[c].append(GV.countries.index('Lithuania'))

        #####Finding basket for countries other than Cyprus and Latvia
        else:
            for nc in range(GV.num_of_contries):
                if basket_flag[nc][c] == 1:
                    basket[c].append(GV.countries[nc])
                    bcindex[c].append(nc)  ##finding index of basket countries in countries list

        #####Finding indices of countris in compulsary basket
        compulsory_bcindex.append([])
        for nc in range(GV.num_of_contries):
            if basket_flag_compulsory[nc][c] == 1:
                # basket[c].append(countries[nc])
                compulsory_bcindex[c].append(nc)  ##finding index of basket countries in countries list
    return basket, bcindex, compulsory_bcindex

