from flask import Flask, request, jsonify,render_template

app = Flask(__name__)

@app.route('/')
def indexPage():
    return render_template("index.html")
