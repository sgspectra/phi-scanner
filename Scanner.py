import re
import os
import xml.etree.ElementTree as ElementTree
import zipfile

class TextScanner:

    def __init__(self, regexFile, scanFile):
        self.regexFile = regexFile
        self.scanFile = scanFile
        self.regex = []
        self.matches = []

    def get_regex(self):
        with open(self.regexFile, 'r') as inFile:
            for line in inFile:

                line = line.rstrip('\n')

                if len(line) > 0:
                    regex = re.compile(line)
                    self.regex.append(regex)
        inFile.close()

    def find_matches(self):
        for exp in self.regex:

            with open(self.scanFile, 'r') as inFile:

                for line in inFile:
                    matches = exp.findall(line)

                    for match in matches:
                        self.matches.append(match)

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
        self.matches = []

    def get_regex(self):
        with open(self.regexFile, 'r') as inFile:
            for line in inFile:

                line = line.rstrip('\n')

                if len(line) > 0:
                    regex = re.compile(line)
                    self.regex.append(regex)
        inFile.close()

    def find_matches(self):

        inputZipFile = zipfile.ZipFile(self.scanFile)
        for name in inputZipFile.namelist():
            if name.endswith("document.xml"):
                for exp in self.regex:

                    inFile =  str(inputZipFile.read(name))
                    matches = exp.findall(inFile)

                    #TODO Remove code for debugging false positives
                    # dump = open('./dump.txt', 'a+')
                    # dump.write(name)
                    # dump.write('\n')
                    # dump.write(str(matches))
                    # dump.write('\n')
                    # dump.close()

                    for match in matches:
                        self.matches.append(match)



class FileFinder:

    def __init__(self, directory, extension = ".txt"):
        self.dir = directory
        self.ext = extension
        self.output = "./default_output.txt"
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

"""
    def findfiles(self, direct):
        output = open(self.output, 'a+')
        for entry in os.scandir(direct):
            if entry.is_dir(follow_symlinks=False):
                self.findfiles(entry.path)
            elif entry.path.endswith(self.ext):
                output.write(entry.path)
                output.write('\n')
        output.close()
"""

def createScanner(regex, fileName, fileType):
    if fileType in ['.docx','.pptx','.zip']:
        return ZipScanner(regex, fileName)
    else:
        return TextScanner(regex, fileName)

def runFullScan():
    typelist = ['.txt', '.docx', '.pptx', '.zip']
    regexFiles = ['./lib/medTerms.txt', './lib/drugs.txt', './lib/phi_regex.txt']
    matches = {}

    # create a file finder to find text docs
    f = FileFinder('./sampleDir')

    for filetype in typelist:

        f.changeFiletype(filetype)

        # scan for files
        foundfiles = f.returnfiles(f.dir)
        print(foundfiles)

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
                    matches[line] += scan.matches
                else:
                    matches[line] = scan.matches

                #TODO Remove Debugging Code
                dump = open('./dump.txt', 'w+')
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

def menu():
    userEntry = 0
    print("******* Welcome to PHI Scanner *******")
    while(userEntry != 4):
        print("Please make your selection from the following options:")
        print("1. Scan for files which may contain PHI indicators")
        print("2. Edit PHI Search Terms")
        print("3. Edit Dictionary")
        print("4. Exit")
        #TODO make sure userEntry is valid
        userEntry = int(input('$'))
        if(userEntry == 1):
            runFullScan()
        elif(userEntry == 2):
            editPhiTerms()
        elif(userEntry == 3):
            editDictionary()
        print('******* ******* ******* *******')


def main():
    menu()


if __name__ == "__main__":
    main()
