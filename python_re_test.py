import re

reFileName = input("Please enter the name of the file containing regular expressions:")
reFile = open(reFileName, 'r')
fileToScanName = input("Please enter the name of the file you wish to scan:")
fileToScan = open(fileToScanName, 'r')
for line in reFile:
    data = reFile.readline()
    exp = re.compile(data)
    for scanLine in fileToScan:
        testString = fileToScan.readline()
        match = exp.match(testString)
        print(match)


