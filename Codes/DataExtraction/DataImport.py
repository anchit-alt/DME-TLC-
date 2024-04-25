import csv

with open('DataExtraction\TaperRollerData_Condense_Sorted.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)