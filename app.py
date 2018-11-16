from flask import Flask
import Scanner

app= Flask(__name__)

@app.route("/")
def hello():
    return str(Scanner.main())