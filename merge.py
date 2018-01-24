
import csv

tags = open("tags.csv","r")
tables = open("seats.csv","r")

tag = {}
table = {}

# Load the data
for row in csv.reader(tags):
    tag[(row[0],row[1])] = row[2]

for row in csv.reader(tables):
    if row[0] == "First Name":
        continue
    table[(row[0],row[1])] = row[6]

# Sanity Check
for (f,l) in tag:
    if (f,l) not in table:
        print("Tables list missing " + f + " " + l)

for (f,l) in table:
    if (f,l) not in tag:
        print("Tags list missing " + f + " " + l)

# Dump combined csv

out = open("table_data.csv","w")
for (f,l) in tag:
    out.write(f+","+l+","+tag[(f,l)]+","+table[(f,l)]+"\n")
out.close()
