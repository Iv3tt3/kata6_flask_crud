from mi_cartera import app #tambien podriamos hacer from . import app
from flask import render_template, request, redirect
import csv


@app.route("/")
def index():
    f = open("movements.dat", "r")
    reader = csv.DictReader(f)
    movements = list(reader)

    return render_template("index.html", the_movements=movements) 

@app.route("/new_movement", methods=["GET", "POST"]) #Con esta etiqueta acepta peticiones GET i POST
#Con la variable request.method puedes ver si es GET o es POST
def new_mov():
    if request.method == 'GET':
        return render_template("new_mov_form.html")
    else:
        data = request.form
        f = open("movements.dat", "a") #a de append, anade no lee como el r de reader
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)

        return redirect("/") #Es otra funcion de flask que te redirige a una ruta, y le ponemos la ruta de inicio

#request es una instancia que ya existe y el metodo request.form es el que recupera la informacion
