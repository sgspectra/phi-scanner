# Proof of concept file reading regex from one file and testing against another txt file

import re

reFileName = input("Please enter the name of the file containing regular expressions:")
reFile = open(reFileName, 'r')
fileToScanName = input("Please enter the name of the file you wish to scan:")
fileToScan = open(fileToScanName, 'r')
for line in reFile:
    print(line)
    exp = re.compile(line)
    for scanLine in fileToScan:
        print(scanLine)
        match = exp.match(scanLine)
        print(match)


