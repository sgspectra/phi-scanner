import re
import os


class TextScanner:

    def __init__(self, regexFile, scanFile):
        self.regexFile = regexFile
        self.scanFile = scanFile
        self.regex = []
        self.matches = []

    def get_regex(self):
        with open(self.regexFile, 'r') as file:
            for line in file:

                line = line.rstrip('\n')

                if len(line) > 0:
                    regex = re.compile(line)
                    self.regex.append(regex)

    def find_matches(self):
        for exp in self.regex:

            with open(self.scanFile, 'r') as file:

                for line in file:
                    matches = exp.findall(line)

                    for match in matches:
                        self.matches.append(match)

            file.close()

    def flag_file(self):
        print("flag " + self.scanFile)

    def match_count(self):
        return len(self.matches)


class FileFinder:

    def __init__(self, directory, extension):
        self.dir = directory
        self.ext = extension
        self.output = "./default_output.txt"

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


def main():
    #create a file finder to find text docs
    f = FileFinder('./sampleDir', '.txt')
    #set the output of the file finder
    f.setoutput()
    #scan for files
    f.findfiles(f.dir)

    #open the output file
    txtdocs = open(f.output, 'r')
    #each file in the output file will be a path to a text doc that needs to be scanned
    for line in txtdocs:
        #strip newline
        line = line.rstrip('\n')
        #scan for phi
        scan1 = TextScanner('./lib/phi_regex.txt', line)
        scan1.get_regex()
        scan1.find_matches()
        print(line)
        print(scan1.matches)
        #scan for medTerms
        scan2 = TextScanner('./lib/medTerms.txt', line)
        scan2.get_regex()
        scan2.find_matches()
        print(scan2.matches)
        #scan for drugs
        scan3 = TextScanner('./lib/drugs.txt', line)
        scan3.get_regex()
        scan3.find_matches()
        print(scan3.matches)



if __name__ == "__main__":
    main()
