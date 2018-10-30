# @reFileName is the name of the file containing regular expressions to be searched for.
# expressions are separated by newline
# @fileToScanName is the name of the file that you would like to run the regex against.
# It is read all at once and the results returned in @match

import re

#reFileName = input("Please enter the name of the file containing regular expressions:")
#reFile = open(reFileName, 'r')
reFile = open('lib/phi_regex.txt', 'r')
#fileToScanName = input("Please enter the name of the file you wish to scan:")
fileToScanName = 'test_text.txt'
for line in reFile:
    fileToScan = open(fileToScanName, 'r')
    #stip the newline from the regex
    line = line.rstrip('\n')
    print(line)
    exp = re.compile(line)
    print(exp)
    match = exp.findall(fileToScan.read())
    print(match)
    fileToScan.close()