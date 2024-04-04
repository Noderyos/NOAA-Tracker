from flask import Flask, render_template, send_file
import mysql.connector
from datetime import datetime
import requests

database = mysql.connector.connect(
    host="127.0.0.1",
    user="noaa",
    password="noaa",
    database="noaa"
)

app = Flask(__name__)


def get_passes(satellite=""):
    cursor = database.cursor()

    sql = "SELECT * from pass"
    if satellite:
        cursor.execute(
            "SELECT * from pass WHERE satellite=%s",
            (satellite,)
        )
    else:
        cursor.execute("SELECT * from pass")
    passes = [
        dict(zip(["start", "satellite", "duration", "elevation"], a))
        for a in cursor.fetchall()
    ]
    cursor.close()
    database.commit()

    for p in passes:
        start = p["start"]
        p["id"] = int(start.timestamp())
        end = datetime.fromtimestamp(start.timestamp() + p["duration"])
        p["start"] = start.strftime("%H:%M")
        p["end"] = end.strftime("%H:%M")
        p["date"] = start.strftime("%d %B %Y")
    return passes[::-1]


@app.route("/")
def index():
    return render_template("base.html", passes=get_passes())


@app.route("/noaa15")
def noaa15():
    return render_template("base.html", passes=get_passes("NOAA 15"))


@app.route("/noaa18")
def noaa18():
    return render_template("base.html", passes=get_passes("NOAA 18"))


@app.route("/noaa19")
def noaa19():
    return render_template("base.html", passes=get_passes("NOAA 19"))


@app.route("/thumbnail/<id>.png")
def thumbnail(id):
    return send_file(f"/opt/NOAA/images/{id}/raw_unsync.png")

@app.route("/image/<id>/<name>")
def image(id, name):
    return send_file(f"/opt/NOAA/images/{id}/{name}")

import os

@app.route("/details/<id>")
def details(id):
    files = [a for a in os.listdir("/opt/NOAA/images/" + id) if a.startswith("avhrr_3_rgb_")]
    files = sorted(files, key=lambda x:"map" not in x)
    names = [a[12:-4].replace("_", " ") for a in files]

    return render_template("details.html", id=id, images=list(zip(names, files)))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
