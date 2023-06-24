from mi_cartera import app 
from mi_cartera.models import MovementDAO, Movement
from flask import render_template, request, redirect
import csv


dao = MovementDAO('movements.dat') 

@app.route("/")
def index():
    dao.all() #Llamamos al metodo all que nos crea la lista de objetos
    return render_template("index.html", the_movements=dao.all_movements) #Pasamos la lista de objetos a index.html

@app.route("/new_movement", methods=["GET", "POST"]) 
def new_mov():
    if request.method == 'GET':
        return render_template("new_mov_form.html")
    else:
        data = request.form
        mov = Movement(data['date'],data['abstract'],data['amount'],data['currency'])
        dao.insert(mov)

        return redirect("/") 