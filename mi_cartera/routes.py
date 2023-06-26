from mi_cartera import app 
from mi_cartera.models import MovementDAO, Movement
from flask import render_template, request, redirect, flash
import csv


dao = MovementDAO('movements.dat') 

@app.route("/")
def index():
    dao.all() #Llamamos al metodo all que nos crea la lista de objetos
    return render_template("index.html", the_movements=dao.all_movements) #Pasamos la lista de objetos a index.html

@app.route("/new_movement", methods=["GET", "POST"]) 
def new_mov():
    if request.method == 'GET':
        return render_template("new_mov_form.html", the_form = {}) #Tengo que informarle un diccionario vacio porque sino peta debido a que hemos anadido el valor predeterminado 
    else:
        data = request.form
        try:
            mov = Movement(data['date'],data['abstract'],data['amount'],data['currency'])
            dao.insert(mov)
            return redirect("/") 
        except ValueError as error: #Capturamos el mensaje de error con una variable "error"
            flash(str(error)) 
            return render_template("new_mov_form.html", the_form=data)
        