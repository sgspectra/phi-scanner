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

    def match_count(self):
        return len(self.matches)



def main():
    scanner_phi = Scanner('lib/phi_regex.txt', 'test_text.txt')
    scanner_drugs = Scanner('lib/drugs.txt', 'test_text.txt')
    scanner_medterms = Scanner('lib/medTerms.txt', 'test_text.txt')

    # TODO If we move the scan for drugs and med terms to be the first scans, the scan
    # TODO for PHI indicators will become irrelevant

    # Scan for popular drugs
    scanner_drugs.get_regex()
    scanner_drugs.find_matches()
    print(scanner_drugs.matches)
    if len(scanner_drugs.matches) > 10:
        scanner_drugs.flag_file()
    
    # Scan for popular medical terms
    scanner_medterms.get_regex()
    scanner_medterms.find_matches()
    print(scanner_medterms.matches)
    if len(scanner_medterms.matches) > 10:
        scanner_medterms.flag_file()

    if scanner_drugs.match_count() > 0 or scanner_medterms.match_count() > 0:
        # Scan for PHI Indicators
        scanner_phi.get_regex()
        scanner_phi.find_matches()
        print(scanner_phi.matches)
        if len(scanner_phi.matches) > 10:
            scanner_phi.flag_file()


if __name__ == "__main__":
    main()
