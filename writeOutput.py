from xlutils.copy import copy
import xlrd

def write_xls(file_name, sheet1, data1, sheet2, data2, sheet3, data3, sheet4, data4, headings1, headings2, heading_xf, data_xfs, monthlyRevenue, netoverallRevenue, contryRevenue, sheet6):
    ##### Writes IRP output on file "Output/price_evolution"
    book = xlrd.open_workbook(file_name)
    #sheet = book.sheet_by_name(sheet_name,cell_overwrite_ok=True)
    tempbook = copy(book)

    tempsheet1 = tempbook.get_sheet(sheet1)
    tempsheet1.write(0, 0, 'Countries/Dates', heading_xf)

    for colx in range(len(headings1)):
        tempsheet1.write(0, colx+1, headings1[colx], heading_xf)
        tempsheet1.col(colx).width = 4444

    for rowx in range(len(headings2)):
        tempsheet1.write(rowx+1, 0, headings2[rowx], heading_xf)
        tempsheet1.set_panes_frozen(True) # frozen headings instead of split panes
    #sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
        tempsheet1.set_remove_splits(True) # if user does unfreeze, don't leave a split there
    # print(len(data))
    # print(len(data[0]))
    # rowx=0
    #
    for rowx in range(len(data1)):
        for colx in range(len(data1[0])):
            tempsheet1.write(rowx+1, colx+1, data1[rowx][colx])

    tempsheet2 = tempbook.get_sheet(sheet2)
    tempsheet2.write(0, 0, 'Countries/Dates', heading_xf)

    for colx in range(len(headings1)):
        tempsheet2.write(0, colx + 1, headings1[colx], heading_xf)
        tempsheet2.col(colx).width = 4444

    for rowx in range(len(headings2)):
        tempsheet2.write(rowx + 1, 0, headings2[rowx], heading_xf)
        tempsheet2.set_panes_frozen(True)  # frozen headings instead of split panes
        # sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
        tempsheet2.set_remove_splits(True)  # if user does unfreeze, don't leave a split there
    # print(len(data))
    # print(len(data[0]))
    # rowx=0
    #
    for rowx in range(len(data2)):
        for colx in range(len(data2[0])):
            tempsheet2.write(rowx + 1, colx + 1, data2[rowx][colx])

    tempsheet3 = tempbook.get_sheet(sheet3)
    tempsheet3.write(0, 0, 'Countries/Dates', heading_xf)

    for colx in range(len(headings1)):
        tempsheet3.write(0, colx + 1, headings1[colx], heading_xf)
        tempsheet3.col(colx).width = 4444

    for rowx in range(len(headings2)):
        tempsheet3.write(rowx + 1, 0, headings2[rowx], heading_xf)
        tempsheet3.set_panes_frozen(True)  # frozen headings instead of split panes
        # sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
        tempsheet3.set_remove_splits(True)  # if user does unfreeze, don't leave a split there

    for rowx in range(len(data4)):
        for colx in range(len(data4[0])):
            tempsheet3.write(rowx + 1, colx + 1, data3[rowx][colx])
    # print(len(data))
    # print(len(data[0]))
    # rowx=0
    #

    tempsheet4 = tempbook.get_sheet(sheet4)
    tempsheet4.write(0, 0, 'Countries/Dates', heading_xf)

    for colx in range(len(headings1)):
        tempsheet4.write(0, colx + 1, headings1[colx], heading_xf)
        tempsheet4.col(colx).width = 4444

    for rowx in range(len(headings2)):
        tempsheet4.write(rowx + 1, 0, headings2[rowx], heading_xf)
        tempsheet4.set_panes_frozen(True)  # frozen headings instead of split panes
        # sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
        tempsheet4.set_remove_splits(True)  # if user does unfreeze, don't leave a split there

    for rowx in range(len(data4)):
        for colx in range(len(data4[0])):
            tempsheet4.write(rowx + 1, colx + 1, data4[rowx][colx])

    ############################################################
    tempsheet6 = tempbook.get_sheet(sheet6)
    tempsheet6.write(0, 0, 'Net Over All Revenue', heading_xf)
    tempsheet6.write(0, 1, netoverallRevenue)
    tempsheet6.write(3, 0, 'DD-MM-YYYY', heading_xf)
    tempsheet6.write(3, 1, 'Revenue', heading_xf)
    for rowx in range(len(headings1)):
        tempsheet6.write(rowx+4, 0, headings1[rowx])
        tempsheet6.col(colx).width = 4444
    for rowx in range(len(monthlyRevenue)):
        tempsheet6.write(rowx+4, 1, monthlyRevenue[rowx])

    tempsheet6.write(3, 4, 'Country', heading_xf)
    tempsheet6.write(3, 5, 'Country Revenue', heading_xf)
    for rowx in range(len(headings2)):
        tempsheet6.write(rowx + 4, 4, headings2[rowx])
        tempsheet6.col(colx).width = 4444
    for rowx in range(len(contryRevenue)):
        tempsheet6.write(rowx + 4, 5, contryRevenue[rowx])
    tempbook.save(file_name)
