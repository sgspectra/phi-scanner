#!/usr/bin/python3

import re
import os
import xml.etree.ElementTree as ElementTree
import zipfile
<<<<<<< HEAD
import json
#import pyAesCrypt
=======
import pyAesCrypt
import pandas
>>>>>>> bec88fb359cd12bd831d63232fbe3bf3be30aeba


class TextScanner:

    def __init__(self, regexFile, scanFile):
        self.regexFile = regexFile
        self.scanFile = scanFile
        self.regex = []
        self.matches = {}
        

    def get_regex(self):
        with open(self.regexFile, 'r') as inFile:
            for line in inFile:

                line = line.rstrip('\n')

                if len(line) > 0:
                    regex = re.compile(line)
                    self.regex.append([regex, line])
        inFile.close()

    def find_matches(self):
        for exp in self.regex:
            with open(self.scanFile, 'r') as inFile:
                for line in inFile:
                    matches = exp[0].findall(line)
                    if len(matches) > 0:
                        if not self.regexFile in self.matches.keys():
                            self.matches[self.regexFile] = {}
                        self.matches[self.regexFile][exp[1]] = matches

            inFile.close()

    def flag_file(self):
        print("flag " + self.scanFile)

    def match_count(self):
        return len(self.matches)


class ZipScanner:

    def __init__(self, regexFile, scanFile):
        self.regexFile = regexFile
        self.scanFile = scanFile
        self.regex = []
        self.matches = {}
        self.matches = {}

    def get_regex(self):
        with open(self.regexFile, 'r') as inFile:
            for line in inFile:

                line = line.rstrip('\n')

                if len(line) > 0:
                    regex = re.compile(line)
                    self.regex.append([regex, line])
        inFile.close()

    def find_matches(self):

        inputZipFile = zipfile.ZipFile(self.scanFile)
        for name in inputZipFile.namelist():
            if name.endswith(".xml"):
                inFile =  str(inputZipFile.read(name))

                #split the file to get only the files text
                splitFile = re.split(re.compile("</?[A-Za-z]\:t[\S?.*?]?>"), inFile)
                inFile = '\n'.join(splitFile[1::2])
                for exp in self.regex:                    
                    matches = exp[0].findall(inFile)
                    if len(matches) > 0:
                        if not self.regexFile in self.matches.keys():
                            self.matches[self.regexFile] = {}
                        self.matches[self.regexFile][exp[1]] = matches


class FileFinder:

    def __init__(self, directory, extension = ".txt"):
        self.dir = directory
        self.ext = extension
        self.output = "./lib/default_output.txt"
        self.foundfiles = []

    def changeFiletype(self, ext):
        self.foundfiles = []
        self.ext = ext

    def returnfiles(self, direct):
        for entry in os.scandir(direct):
            if entry.is_dir(follow_symlinks=False):
                self.returnfiles(entry.path)
            elif entry.path.endswith(self.ext):
                self.foundfiles.append(entry.path)
                o = open(self.output, 'a+')
                o.write(entry.path)
                o.write('\n')
                o.close()
        return self.foundfiles

    def setoutput(self):
         print("Please enter the output location:")
         self.output = input()


class ExcelConverter:

    def __init__(self, excel_file, text_file):
        self.excel_file = excel_file
        self.text_file = text_file

    def read_file(self):
        sheets = pandas.read_excel(self.excel_file, sheet_name=None)

        for sheet in sheets:
            data_frame = sheets[sheet]
            rows, columns = data_frame.shape

            for x in range(0, columns):
                data = data_frame.iloc[:, x].tolist()
                data = " ".join(str(x) for x in data)
                self.write_to_file(data)

    def write_to_file(self, data):
        with open(self.text_file, 'w+') as file:
            file.write(data)

        file.close()


def createScanner(regex, fileName, fileType):
    if fileType in ['.docx','.pptx','.zip']:
        return ZipScanner(regex, fileName)
    elif fileType == '.xlsx':
        xls = ExcelConverter(fileName, fileName + '.txt')
        xls.read_file()
        return TextScanner(regex, xls.text_file)
    else:
        return TextScanner(regex, fileName)

def runFullScan(path):
    typelist = ['.txt', '.docx', '.pptx', '.zip', '.csv', '.xlsx']
    regexFiles = ['./lib/medTerms.txt', './lib/drugs.txt', './lib/phi_regex.txt']
    matches = {}

    # create a file finder to find text docs
    f = FileFinder(path)

    for filetype in typelist:

        f.changeFiletype(filetype)

        # scan for files
        foundfiles = f.returnfiles(f.dir)

        print('Found ' + str(len(foundfiles)) + ' files of type ' + filetype)

        # each file in the output file will be a path to a text doc that needs to be scanned
        for line in foundfiles:
            # strip newline
            line = line.rstrip('\n')
            # scan for terms of each regex file
            for regexList in regexFiles:
                scan = createScanner(regexList, line, filetype)
                scan.get_regex()
                scan.find_matches()
                if line in matches.keys():

                    #combine the two dicts together
                    
                    #python 3.5 or greater
                    #matches[line] = {**matches[line], **scan.matches}

                    #python 3.4 or lower
                    matches[line].update(scan.matches)

                else:
                    matches[line] = scan.matches

                #TODO Remove Debugging Code
                dump = open('./lib/dump.txt', 'w+')
                for key in matches.keys():
                    dump.write(key)
                    dump.write('\n')
                    dump.write(str(matches[key]))
                    dump.write('\n')
                dump.close()
    
    return matches

def editPhiTerms():
    option = 0
    while(option != 3):
        print("1. View PHI Regular Expression File")
        print("2. Add to PHI Regular Expression File")
        print("3. Return to Main Menu")
        option = int(input('$'))
        if(option == 1):
            f = open('./lib/phi_regex.txt', 'r')
            for line in f:
                print(line.rstrip('\n'))
            f.close()
        elif(option == 2):
            f = open('./lib/phi_regex.txt', 'a+')
            newRegex = input("Please enter the regular expression to be added:")
            f.write('\n')
            f.write(newRegex)
            f.close()

def editDictionary():
    option = 0
    while(option != 5):
        print("1. View Dictionary of Drug Terms")
        print("2. Edit Dictionary of Drug Terms")
        print("3. View Dictionary of Medical Terms")
        print("4. Edit Dictionary of Medical Terms")
        print("5. Return to Main Menu")
        option = int(input('$'))
        if (option == 1):
            f = open('./lib/drugs.txt', 'r')
            for line in f:
                print(line.rstrip('\n'))
            f.close()
        elif (option == 2):
            f = open('./lib/drugs.txt', 'a+')
            newRegex = input("Please enter the term to be added:")
            f.write('\n')
            f.write(newRegex)
            f.close()
        elif (option == 3):
            f = open('./lib/medTerms.txt', 'r')
            for line in f:
                print(line.rstrip('\n'))
            f.close()
        elif (option == 4):
            f = open('./lib/medTerms', 'a+')
            newRegex = input("Please enter the term to be added:")
            f.write('\n')
            f.write(newRegex)
            f.close()

def generateReport(matches):
<<<<<<< HEAD
    reportName = 'Reports/' + input('Please enter the output file for the report:').strip()
    with open(reportName, 'w') as outfile:
        json.dump(matches, outfile, indent=4)
    print('A copy of this report has been stored in the Reports directory under: ' + reportName)
=======
    reportName = input('Please enter the output file for the report:').strip()
    report = open(reportName, 'w+')
    for key in matches:
        if len(str(matches[key])) > 2:
            report.write(key)
            print(key)
            report.write('\n')
            report.write(str(matches[key]))
            print(str(matches[key]))
            report.write('\n')
    report.close()
    print('A copy of this report has been stored in: ' + reportName)
>>>>>>> bec88fb359cd12bd831d63232fbe3bf3be30aeba


def encryptFiles():
    # buffersize
    bufferSize = 64 * 1024

    # encrypts the file with password and file name
    def encrypt(password, fileName):
        pyAesCrypt.encryptFile(fileName, fileName + ".aes", password, bufferSize)
        if os.path.exists(fileName):
            os.remove(fileName)

    # decrypt file with password and file name
    def decrypt(password, fileName):
        pyAesCrypt.decryptFile(fileName + ".aes", fileName, password, bufferSize)
        if os.path.exists(fileName + ".aes"):
            os.remove(fileName + ".aes")

    done = False
    # runs until the user quits
    while (not done):
        print("Do you want to encrypt, decrypt, or quit? (E/D/Q)")
        answer = input().lower().strip()
        # if user wants to encrypt
        if (answer == "e"):
            print("Enter name of file to encrypt: ")
            fileName = input().strip()
            print("Enter password: ")
            password = input().strip()
            try:
                encrypt(password, fileName)
            except IOError:
                print("ERROR file does not exist")
        # if user wants to decrypt
        elif (answer == "d"):
            print("Enter name of file to decrypt: ")
            fileName = input().strip()
            print("Enter password: ")
            password = input().strip()
            try:
                decrypt(password, fileName)
            except IOError:
                print("ERROR file is not encrypted")
            except ValueError:
                print("ERROR password is incorrect")
        # if user wants to quit
        elif (answer == "q"):
            done = True
            break
        else:
            print("Sorry that is not an option")


def menu():
    userEntry = 0
    print("******* Welcome to PHI Scanner *******")
    while(userEntry != 6):
        print("Please make your selection from the following options:")
        print("1. Scan for files which may contain PHI indicators")
        print("2. Edit PHI Search Terms")
        print("3. Edit Dictionary")
        print("4. Generate Report")
        print("5. Encrypt/Decrypt Files")
        print("6. Exit")
        #TODO make sure userEntry is valid
        userEntry = int(input('$'))
        if(userEntry == 1):
            path = input('Please enter the path to the directory you wish to scan:').strip()
            runFullScan(path)
        elif(userEntry == 2):
            editPhiTerms()
        elif(userEntry == 3):
            editDictionary()
        elif(userEntry == 4):
            path = input('Please enter the path to the directory you wish to scan:').strip()
            generateReport(runFullScan(path))
        elif(userEntry == 5):
            encryptFiles()
        elif(userEntry == 6):
            break
        else:
            print('Please select a valid option')
        print('******* ******* ******* *******')


def main():
    menu()


if __name__ == "__main__":
    main()
