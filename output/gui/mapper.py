from xlrd import open_workbook
from xlutils.copy import copy
import os

dirname = os.getcwd()

def format():
    rb = open_workbook(dirname + '/Format.xls', formatting_info=True)
    wb = copy(rb)
    wb.save(dirname + '/Output.xls')

def output():
    rb = open_workbook(dirname + '/Output.xls', formatting_info=True)
    wb = copy(rb)
    return wb
    
def xls1_2(contract_list, bidnum_dict):
    wb=output()
    sheet1 = wb.get_sheet(0)
    rownum = 2
    for contract in contract_list:
        try:
            sheet1.write(rownum, 0, rownum-1)
            sep = contract.find(":")
            sheet1.write(rownum, 1, contract[sep+2:])
            sep = bidnum_dict[contract].find(":")
            sheet1.write(rownum, 2, bidnum_dict[contract][sep+2:])
        except:
            continue
        finally:
            rownum+=1
    wb.save(dirname + '/Output.xls')

        
def xls3_12(*args):
    
    wb=output()
    sheet1 = wb.get_sheet(0)
    rownum = 2
    colnum = 3
    
    for arg in args:
        for item in arg:
            sep = item.find(":")
            sheet1.write(rownum, colnum, item[sep+2:])
            rownum += 1
        colnum+= 1
        rownum = 2
    
    wb.save(dirname + '/Output.xls')
    
def xls13_14(*args):
    
    wb=output()
    sheet1 = wb.get_sheet(0)
    rownum = 2
    colnum = 13
    
    for arg in args:
        for item in arg:
            sheet1.write(rownum, colnum, item)
            rownum += 1
        colnum+= 1
        rownum = 2
    
    wb.save(dirname + '/Output.xls')
    
    
