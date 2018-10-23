# @reFileName is the name of the file containing regular expressions to be searched for.
# expressions are separated by newline
# @fileToScanName is the name of the file that you would like to run the regex against.
# It is read all at once and the results returned in @match

import re

reFileName = input("Please enter the name of the file containing regular expressions:")
reFile = open(reFileName, 'r')
fileToScanName = input("Please enter the name of the file you wish to scan:")
fileToScan = open(fileToScanName, 'r')
for line in reFile:
    print(line)
    exp = re.compile(line)
    match = exp.findall(fileToScan.read())
    print(match)