import re


class Scanner:

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


def main():
    scanner = Scanner('lib/phi_regex.txt', 'test_text.txt')
    scanner.get_regex()
    print(scanner.regex)

    scanner.find_matches()
    print(scanner.matches)

    if len(scanner.matches) > 10:
        scanner.flag_file()


if __name__ == "__main__":
    main()
