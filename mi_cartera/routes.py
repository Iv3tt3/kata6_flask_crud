from mi_cartera import app 
from mi_cartera.models import MovementDAO, Movement
from flask import render_template, request, redirect
import csv


dao = MovementDAO('movements.dat') #Asi se genera cuando se levanta la aplicacion

@app.route("/")
def index():
    #f = MovementDAO(movements.dat)
    f = open("movements.dat", "r")
    reader = csv.DictReader(f)
    movements = list(reader)
    # DEBERES Decir que los movemennts es el resultado de dao.all y hacerlo con test

    return render_template("index.html", the_movements=movements) 

@app.route("/new_movement", methods=["GET", "POST"]) 
def new_mov():
    if request.method == 'GET':
        return render_template("new_mov_form.html")
    else:
        #dao = MovementDAO("movements.dat") En vez de instanciarlo aqui lo movemos al inicio para no tener que ir instanciandolo cada vez
        data = request.form
        mov = Movement(data['date'],data['abstract'],data['amount'],data['currency'])
        dao.insert(mov)

        return redirect("/") 