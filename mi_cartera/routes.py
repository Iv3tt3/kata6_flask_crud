from mi_cartera import app #tambien podriamos hacer from . import app
from flask import render_template
import csv


@app.route("/")
def index():
    f = open("movements.dat", "r")
    reader = csv.DictReader(f)
    movements = list(reader)

    return render_template("index.html", the_movements=movements) 

@app.route("/new_movement")
def new_mov():
    return render_template("new_mov_form.html")


