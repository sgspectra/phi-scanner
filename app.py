from flask import Flask
from flask import render_template
import os
import Scanner
import json

app= Flask(__name__)

@app.route("/")
def hello():
    
    allFiles = os.listdir("Reports")
    selectedFile = "scan1"
    statistics = {'files': {}, 'filetypes': {}, 'totalmatches': 0, 
        'totalpaterns': 0, 'regexmatches': {}, 'regexfilematches': {}}
    with open("Reports/"+selectedFile, 'r') as inFile:
        fileData = json.load(inFile)

    for fileName in fileData.keys():
        
        if len(fileData[fileName].keys()) > 0:
            statistics['files'][fileName] = {'total': 0, 'uniquepaterns': 0, 'paterns': {}}
            ext = fileName.split('.')[-1]
            if ext in statistics['filetypes']:
                statistics['filetypes'][ext] += 1
            else:
                statistics['filetypes'][ext] = 1

        for regexfile in fileData[fileName].keys():
            if regexfile in statistics['regexfilematches']:
                statistics['regexfilematches'][regexfile] += 1
            else:
                statistics['regexfilematches'][regexfile] = 1

            for patern in fileData[fileName][regexfile]:

                statistics['totalpaterns'] += 1
                statistics['files'][fileName]['uniquepaterns'] += 1
                statistics['files'][fileName]['paterns'][patern] = 0
                if regexfile in statistics['regexmatches']:
                    statistics['regexmatches'][regexfile] += 1
                else:
                    statistics['regexmatches'][regexfile] = 1

                for match in fileData[fileName][regexfile][patern]:

                    statistics['totalmatches'] += 1
                    statistics['files'][fileName]['paterns'][patern] += 1
                    statistics['files'][fileName]['total'] += 1
        



    return render_template('index.html', foundfiles = allFiles, stats = statistics)

if __name__ == '__main__':
    app.run()#ssl_context='adhoc')
