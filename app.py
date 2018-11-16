from flask import Flask
from flask import render_template
import Scanner

app= Flask(__name__)

@app.route("/")
def hello():
    scannerValues = Scanner.main()
    return render_template('index.html', foundfiles = scannerValues)