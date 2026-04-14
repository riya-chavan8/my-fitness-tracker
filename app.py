from flask import Flask, render_template, request, redirect
import json
from datetime import date

app = Flask(__name__)
FILE = "data.json"

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":

        workout = request.form["workout"]
        water = request.form["water"]
        sleep = request.form["sleep"]

        data = load_data()

        data[str(date.today())] = {
            "workout": workout,
            "water": water,
            "sleep": sleep
        }

        save_data(data)

        return redirect("/progress")

    return render_template("index.html")


@app.route("/progress")
def progress():

    data = load_data()

    return render_template("progress.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)