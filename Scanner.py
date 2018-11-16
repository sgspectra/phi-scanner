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
            if name.endswith(".xml"):
                for exp in self.regex:

                    inFile =  str(inputZipFile.read(name))
                    matches = exp.findall(inFile)

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
                self.findfiles(entry.path)
            elif entry.path.endswith(self.ext):
                self.foundfiles.append(entry.path)
        return self.foundfiles

    def setoutput(self):
         print("Please enter the output location:")
         self.output = input()

    def findfiles(self, direct):
        output = open(self.output, 'a+')
        for entry in os.scandir(direct):
            if entry.is_dir(follow_symlinks=False):
                self.findfiles(entry.path)
            elif entry.path.endswith(self.ext):
                output.write(entry.path)
                output.write('\n')
        output.close()


def createScanner(regex, fileName, fileType):
    if fileType in ['.docx','.pptx','.zip']:
        return ZipScanner(regex, fileName)
    else:
        return TextScanner(regex, fileName)

def main():
    typelist = ['.txt','.docx','.pptx','.zip']
    regexFiles = ['./lib/medTerms.txt', './lib/drugs.txt', './lib/phi_regex.txt']

    # create a file finder to find text docs
    f = FileFinder('./sampleDir')

    for filetype in typelist:

        f.changeFiletype(filetype)

        # scan for files
        foundfiles = f.returnfiles(f.dir)

        # each file in the output file will be a path to a text doc that needs to be scanned
        for line in foundfiles:
            # strip newline
            line = line.rstrip('\n')
            # scan for terms of each regex file
            for regexList in regexFiles:
                scan = createScanner(regexList, line, filetype)
                scan.get_regex()
                scan.find_matches()
                print(scan.matches)


if __name__ == "__main__":
    main()
