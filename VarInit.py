import globvar as GV
import cLSOutilities as CU
from os.path import isfile
import xlrd
import numpy as np


def open_file(path):
    """
    Open and read an Excel file
    """
    # Check if file exists or not
    if not isfile(path):
        print('File doesn\'t exist: ', path)

    # Open the excel sheet
    xl_workbook = xlrd.open_workbook(path)

    # Open the sheet (InputInterface) of excel file (ILSO Last Updated.xlsx) by sheet index
    GV.xl_sheet.append(xl_workbook.sheet_by_name('InputInterface'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[0].name)

    # Open the sheet (Index) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('Index'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[1].name)

    # Open the sheet (MultipleFixedReference) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('MultipleFixedReference'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[2].name)

    # Open the sheet (CountryBasket) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('CountryBasket'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[3].name)

    # Open the sheet (BaseVolumeForecast) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('BaseVolumeForecast'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[4].name)

    # Open the sheet (PriceOverrideAndProdDiscd) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('PriceOverrideAndProdDiscd'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[5].name)

    # Open the sheet (PriceCut) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('PriceCut'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[6].name)

    # Open the sheet (DiscountLevel) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('DiscountLevel'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[7].name)

    # Open the sheet (MultipleDelay) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('MultipleDelay'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[8].name)

    # Open the sheet (CogsAndRoyalties) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('CogsAndRoyalties'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[9].name)

    # Open the sheet (SimulatedAnnealing) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('SimulatedAnnealing'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[10].name)

    # Open the sheet (PriceLevels) of excel file (ILSO Last Updated.xlsx) by sheet name
    GV.xl_sheet.append(xl_workbook.sheet_by_name('RefPriceLevels'))
    # Print name of the sheet fetched
    print(40 * '-' + 'Retrieved worksheet: %s' % GV.xl_sheet[11].name)

    return GV.xl_sheet
###############################################################################

###############################################################################
###############################################################################
# Modules for fetching data from sheet InputInterface
###############################################################################
###############################################################################

def fetch_InputInterface(xl_sheet, col_id):
    #######Fetch countries and no. of countries from sheet "InputInterface"
    col_idx = col_id
    while col_idx < xl_sheet.ncols:
        cell_obj = xl_sheet.cell(19, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        if cell_obj.value == '':
            break
        else:
            GV.countries.append(cell_obj.value)
        col_idx += 1
    # getting number of countries
    # global GV.num_of_contries
    GV.num_of_contries = len(GV.countries)

    #######Fetch Dossier Submission dates from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(21, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.dossier_submission_date.append(CU.xldate_to_datetime(cell_obj.value))
        # print(GV.dossier_submission_date)
        #######Fetch Price approval dates from sheet "InputInterface"
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(22, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.price_approval_date.append(CU.xldate_to_datetime(cell_obj.value))
        # print(GV.price_approval_date)
        #######Fetch Price publication dates from sheet "InputInterface"
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(23, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.price_publication_date.append(CU.xldate_to_datetime(cell_obj.value))
        # print(GV.price_publication_date)
        #######Fetch Reimbursement dates from sheet "InputInterface"
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(24, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.reimbursement_date.append(CU.xldate_to_datetime(cell_obj.value))
        # print(GV.reimbursement_date)
        #######Fetch launch dates from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(25, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        # volDates = CU.xldate_to_datetime(cell_obj.value)
        GV.volume_pickup_dates.append(CU.xldate_to_datetime(cell_obj.value))
        # print(GV.volume_pickup_dates)

        #######Fetch base prices from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(29, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.base_prices.append(cell_obj.value)
        #################################################################################
        # At Launch data
        #################################################################################
        #######Fetch multiple/single delay from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(32, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.multi_single_delay.append(cell_obj.value)
        #######Fetch multiple/single delay from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(34, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.num_refrence_rule.append(cell_obj.value)
        #######Fetch information about IRP/NO IRP from sheet "InputInterface"
    #####col_idx = col_id
    # row = xl_sheet.col(row_id)  # 6th column
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(36, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.irp_noirp.append(cell_obj.value)
        #######Fetch reference rules from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(37, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.reference_rules.append(cell_obj.value)
        #######Fetch multiplier factors from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(38, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.multiplier_factor.append(cell_obj.value)
        #######Fetch price consideration period from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(40, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.delay_price.append(cell_obj.value)
        #######Fetch price consideration period for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(41, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.irp_from_date.append(cell_obj.value)
        #######Fetch pricing rules for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(43, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.price_rules.append(cell_obj.value)
        #######Fetch minimum countries required for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(44, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.min_contries.append(cell_obj.value)
        #######Fetch maximum countries allowed for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(45, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.max_contries.append(cell_obj.value)
        ###############################################################
        # Post Launch data
        ###############################################################

        #######Fetch multiple/single delay from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(61, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.num_refrence_rule_pl.append(cell_obj.value)
        #######Fetch information about IRP/NO IRP from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(63, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.irp_noirp_pl.append(cell_obj.value)
        #######Fetch reference rules from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(64, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.reference_rules_pl.append(cell_obj.value)
        # print(GV.reference_rules_pl)
        #######Fetch multiplier factors from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(65, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.multiplier_factor_pl.append(cell_obj.value)
        #######Fetch price consideration period from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(67, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.delay_price_pl.append(cell_obj.value)
        #######Fetch price consideration period for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(68, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.irp_from_date_pl.append(cell_obj.value)
        #######Fetch periodicity for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(70, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.periodicity.append(cell_obj.value)
        #######Fetch periodicity date for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(71, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.periodicity_date.append(cell_obj.value)
        #######Fetch pricing rules for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(73, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.price_rules_pl.append(cell_obj.value)
        #######Fetch minimum countries required for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(74, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.min_contries_pl.append(cell_obj.value)
        #######Fetch maximum countries allowed for irp from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(75, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.max_contries_pl.append(cell_obj.value)
        #######Fetch rferencing period rule from sheet "InputInterface"
    #####col_idx = col_id
    for col_idx in range(col_id, GV.num_of_contries + col_id):
        cell_obj = xl_sheet.cell(76, col_idx)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.referencing_period_rule_pl.append(cell_obj.value)
        ###########################################################################################
    for con in range(GV.num_of_contries):
        if CU.Lesser(GV.price_publication_date[con], GV.volume_pickup_dates[con]):
            GV.pricevol.append(GV.price_publication_date[con])
        else:
            GV.pricevol.append(GV.volume_pickup_dates[con])
    return

###############################################################################
###############################################################################
# Modules for fetching data from sheet "Index"
###############################################################################
###############################################################################

#######Fetch countries participating in Analysis flag (0/1) and number of participating countries from sheet "Index"
def fetch_participation_flag(xl_sheet, row_id, col_id):
    # global WACC
    # global num_of_markets

    GV.WACC = xl_sheet.cell(3, 5).value

    startdate = CU.xldate_to_datetime(xl_sheet.cell(2, 5).value)
    # startyear = int(startdate[3:])

    for row_idx in range(row_id, GV.num_of_contries + row_id):
        cell_obj = xl_sheet.cell(row_idx, col_id)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.participation_flag.append(cell_obj.value)
    # count number of markets participating in IRP
    num_of_markets = GV.participation_flag.count(1)
    return

###########################################################################################

###############################################################################
###############################################################################
# Modules for fetching data from sheet CountryBasket
###############################################################################
###############################################################################

#######Fetch primary basket at launch flag (0/1) from sheet "CountryBasket"
def fetch_CountryBasket(xl_sheet, col_id):
    c = 0
    # print(len(GV.countries))
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.basket_flag_primary_al.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.basket_flag_primary_al[c].append(cell_obj.value)
        c = c + 1
        # pprint.pprint(GV.basket_flag_primary_al)
        #######Fetch secondary basket at launch flag (0/1) from sheet "CountryBasket"
    c = 0
    # print(len(GV.countries))
    for row_idx in range(130, GV.num_of_contries + 130):
        GV.basket_flag_secondary_al.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.basket_flag_secondary_al[c].append(cell_obj.value)
        c = c + 1
        #######Fetch compulsory basket at launch flag (0/1) from sheet "CountryBasket"
    c = 0
    # print(len(GV.countries))
    for row_idx in range(240, GV.num_of_contries + 240):
        GV.basket_flag_compulsory_al.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.basket_flag_compulsory_al[c].append(cell_obj.value)
        c = c + 1
        #######Fetch primary basket post launch flag (0/1) from sheet "CountryBasket"
    c = 0
    # print(len(GV.countries))
    for row_idx in range(352, GV.num_of_contries + 352):
        GV.basket_flag_primary_pl.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.basket_flag_primary_pl[c].append(cell_obj.value)
        c = c + 1
        # pprint.pprint(GV.basket_flag_primary_pl)
        #######Fetch secondary basket post launch flag (0/1) from sheet "CountryBasket"
    c = 0
    # print(len(GV.countries))
    for row_idx in range(472, GV.num_of_contries + 472):
        GV.basket_flag_secondary_pl.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.basket_flag_secondary_pl[c].append(cell_obj.value)
        c = c + 1
        #######Fetch compulsory basket post launch flag (0/1) from sheet "CountryBasket"
    c = 0
    for row_idx in range(582, GV.num_of_contries + 582):
        GV.basket_flag_compulsory_pl.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.basket_flag_compulsory_pl[c].append(cell_obj.value)
        c = c + 1
    return

###########################################################################################

###############################################################################
###############################################################################
# Modules for fetching data from sheet MultipleFixedReference

###############################################################################
###############################################################################

#######Fetch primary basket at launch flag (0/1) from sheet "MultipleFixedReference"
def fetch_MultipleFixedReference(xl_sheet, col_id):
    c = 0
    # print(len(GV.countries))
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.fixed_irp_dates.append([])
        for col_idx in range(col_id, xl_sheet.ncols):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.fixed_irp_dates[c].append(cell_obj.value)
        c = c + 1
        # pprint.pprint(GV.fixed_irp_dates)
    return

###########################################################################################

###############################################################################
###############################################################################
# Modules for fetching data from sheet BaseVolumeForecast
###############################################################################
###############################################################################


#######Fetch dates for volume pickup and irp time frame from sheet "BaseVolumeForecast"
def fetch_BaseVolumeForecast(xl_sheet, col_id):
    # global irp_time_frame
    # row = xl_sheet.row(row_id)  # 6th column
    GV.basedate = xl_sheet.cell(9,4).value

    for col_idx in range(col_id, xl_sheet.ncols):
        cell_obj = xl_sheet.cell(9, col_idx)
        GV.basedates.append(cell_obj.value)
        GV.volume_dates.append(CU.xldate_to_datetime(cell_obj.value))
    GV.irp_time_frame = len(GV.volume_dates)
    GV.volume_dates = np.array(GV.volume_dates)
    #######Fetch base volume from sheet "BaseVolumeForecast"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.base_volume.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.base_volume[c].append(cell_obj.value)
        c += 1
        # print(np.shape(GV.base_volume))
    return

###########################################################################################

###############################################################################
###############################################################################
# Modules for fetching over ride data from sheet PriceOverrideAndProdDiscd
###############################################################################
###############################################################################


#######Fetch Price over ride data from sheet "PriceOverrideAndProdDiscd"
def fetch_PriceOverrideAndProdDiscd(xl_sheet, col_id):
    #######Fetch over ride data from sheet "BaseVolumeForecast"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.priceOverrideAndProdDiscd.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.priceOverrideAndProdDiscd[c].append(cell_obj.value)
        c += 1
        # print(np.shape(GV.priceOverrideAndProdDiscd))
        # print(GV.priceOverrideAndProdDiscd[0][0])
        # pprint.pprint(GV.priceOverrideAndProdDiscd)
    return
###########################################################################################

###########################################################################################
###############################################################################
# Modules for fetching price cut data from sheet PriceCut
###############################################################################
###############################################################################


def fetch_PriceCut(xl_sheet, col_id):
    #######Fetch price cut from sheet "PriceCut"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.priceCut.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.priceCut[c].append(cell_obj.value)
        c += 1
        # print(np.shape(GV.priceCut))
        # print(GV.priceCut[0][0])
        # pprint.pprint(GV.priceCut)
    return
###############################################################################

    ###############################################################################
    ###############################################################################
    # Modules for fetching discount level data from sheet DiscountLevel
    ###############################################################################
    ###############################################################################


def fetch_DiscountLevel(xl_sheet, col_id):
    #######Fetch discount level from sheet "DiscountLevel"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.discountLevel.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.discountLevel[c].append(cell_obj.value)
        c += 1
        # print(np.shape(GV.discountLevel))
        # print(GV.discountLevel[10][0])
        # pprint.pprint(GV.discountLevel)
    return

##############################################################################

    ###############################################################################
    # Modules for fetching multiple delay data from sheet Price Levels
    ###############################################################################
    ###############################################################################

def fetch_PriceLevels(xl_sheet, col_id):
    #######Fetch base volume from sheet "PriceLevels"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.priceLevels.append([])
        for col_idx in range(col_id, GV.num_of_contries + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.priceLevels[c].append(cell_obj.value)
        c += 1
    return
        # print(np.shape(GV.multipleDelay))
        # print(GV.multipleDelay[0][0])
        # pprint.pprint(GV.multipleDelay)

###############################################################################
    ###############################################################################
    ###############################################################################
    # Modules for fetching multiple delay data from sheet MultipleDelay
    ###############################################################################
    ###############################################################################

def fetch_MultipleDelay(xl_sheet, col_id):
    #######Fetch base volume from sheet "BaseVolumeForecast"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.multipleDelay.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.multipleDelay[c].append(cell_obj.value)
        c += 1
        # print(np.shape(GV.multipleDelay))
        # print(GV.multipleDelay[0][0])
        # pprint.pprint(GV.multipleDelay)
    return

##############################################################################

    ###############################################################################
    ###############################################################################
    # Modules for fetching coggs and royalties data from sheet CogsAndRoyalties
    ###############################################################################
    ###############################################################################

def fetch_CogsAndRoyalties(xl_sheet, col_id):
    #######Fetch base Cogs And Royalties from sheet "CogsAndRoyalties"
    c = 0
    for row_idx in range(10, GV.num_of_contries + 10):
        GV.coggs.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.coggs[c].append(cell_obj.value)
        c += 1
    # print(np.shape(GV.coggs))
    # print(GV.coggs[0][0])
    # pprint.pprint(GV.coggs)

    c = 0
    for row_idx in range(271, GV.num_of_contries + 271):
        GV.royalties.append([])
        for col_idx in range(col_id, GV.irp_time_frame + col_id):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            GV.royalties[c].append(cell_obj.value)
        c += 1
        # print(np.shape(GV.royalties))
        # print(GV.royalties[0][0])
        # pprint.pprint(GV.royalties)
    return
##############################################################################

    ###########################################################################################
    ###############################################################################
    # Modules for fetching coggs and royalties data from sheet CogsAndRoyalties
    ###############################################################################
    ###############################################################################

def fetch_SimulatedAnnealing(xl_sheet, row_id, col_id):
    #######Fetch base volume from sheet "BaseVolumeForecast"
    for row_idx in range(row_id, GV.num_of_contries + row_id):
        cell_obj1 = xl_sheet.cell(row_idx, col_id)
        cell_obj2 = xl_sheet.cell(row_idx, col_id + 1)
        cell_obj3 = xl_sheet.cell(row_idx, col_id+2)
        # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        # print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
        GV.dmin.append(int(cell_obj1.value))
        GV.initdates.append(int(cell_obj2.value))
        # GV.dmax.append(GV.basedate + (cell_obj3.value*30))

        if not isinstance(GV.periodicity_date[row_idx-row_id], str):
            date_i = CU.xldate_to_datetime(GV.periodicity_date[row_idx-row_id])
            dindex = int(np.where(GV.volume_dates == date_i)[0])
            GV.dmax.append(dindex)
        else:
            GV.dmax.append(int(cell_obj1.value + 24))
    return

def GetDifferences():
    ##### Calculates differences of various dates from price evolution date
    for c in range(GV.num_of_contries):
        # GV.volume_pickup_dates[c] = GV.price_publication_date[c]
        GV.datediff.append([])
        GV.datediff[c].append(CU.Monthdiff(GV.dossier_submission_date[c], GV.pricevol[c]))
        GV.datediff[c].append(CU.Monthdiff(GV.price_approval_date[c], GV.pricevol[c]))
        GV.datediff[c].append(CU.Monthdiff(GV.price_publication_date[c], GV.pricevol[c]))
        GV.datediff[c].append(CU.Monthdiff(GV.reimbursement_date[c], GV.pricevol[c]))
        GV.datediff[c].append(CU.Monthdiff(GV.volume_pickup_dates[c], GV.pricevol[c]))
    return