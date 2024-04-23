from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)


client = MongoClient('')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/logged_in')
def login():
    return render_template("logged_in.html")

@app.route('/logged_out')
def logout():
    return render_template("logged_out.html")


@app.route('/read_keys')
def read_keys():
    try:
        with open('mw_req.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON file'}), 400

    keys = list(data.keys())

    return jsonify({'keys': keys})


if __name__ == "__main__":
    app.run(debug=True)
