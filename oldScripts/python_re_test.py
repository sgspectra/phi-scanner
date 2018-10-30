# Proof of concept file reading regex from one file and testing against another txt file
# Input file consists of python regex each on a separate line

import re

reFileName = input("Please enter the name of the file containing regular expressions:")
reFile = open(reFileName, 'r')
fileToScanName = input("Please enter the name of the file you wish to scan:")
fileToScan = open(fileToScanName, 'r')
for line in reFile:
    line = line.rstrip("\n")
    print(line)
    exp = re.compile(line)
    print(exp)
    for scanLine in fileToScan:
        print(scanLine)
        match = exp.match(scanLine)
        print(match)


