import xlrd

def get_hydrant_nums():
    file = ("F:\QA IITC\hydrant\hydrants_phones.xls") #exel file path
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    return [sheet.cell_value(i, 0) for i in range(sheet.nrows)]

print(get_hydrant_nums())
"""
with open(r"F:\QA IITC\hydrant\values.txt", "r") as file:
    reading = file.readlines()
    for line in reading:
        split = line.strip().split(":")
        for i in split:"""




       # print(split)



