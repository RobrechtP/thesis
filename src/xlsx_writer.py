import xlsxwriter
import os

path = "test.txt"
filename = "test.xlsx"

workbook = xlsxwriter.Workbook(filename)


data = []
file = open(path)
for line in file:
    data.append(line.split(","))

file.close()
worksheet = workbook.add_worksheet()
for row in range(len(data)):
    for col in range(len(data[row])):
        worksheet.write_number(row,col, float(data[row][col].replace(" ","")))

workbook.close()