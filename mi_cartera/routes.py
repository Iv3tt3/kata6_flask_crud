from mi_cartera import app 
from mi_cartera.models import MovementDAO, Movement
from flask import render_template, request, redirect, flash, url_for
import csv


dao = MovementDAO('movements.dat') 

@app.route("/")
def index():
    dao.all() #Llamamos al metodo all que nos crea la lista de objetos
    if dao.error != []:
        flash(f"CORRUPTED FILE. Movements with format errors in your data file: {str(dao.error)}")
    return render_template("index.html", the_movements=dao.all_movements, title = "Todos") #Pasamos la lista de objetos a index.html
        

@app.route("/new_movement", methods=["GET", "POST"]) 
def new_mov():
    if request.method == 'GET':
        return render_template("new_mov_form.html", the_form = {}, title = "Alta de movimientos") 
    else:
        data = request.form
        try:
            mov = Movement(data['date'],data['abstract'],data['amount'],data['currency'])
            dao.insert(mov)
            return redirect(url_for("index")) #Esto permite buscar la funcion index y cambiar la ruta sin que se desconecte de otros sitios. Porque esto es parametrizable, en produccion tiene otro nombre 
        except ValueError as error: 
            flash(str(error)) 
            return render_template("new_mov_form.html", the_form=data, title = "Alta de movimientos") 

@app.route("/update_movement/<int:id>", methods=["GET", "POST"])
def edit_mov(id):
    if request.method == "GET":
        mov = dao.get(id)
        return render_template("update.html", title="Update movement", 
                               the_form=mov, id=id)
    else:
        data = request.form
        try:
            mv =Movement(data['date'],data['abstract'],data['amount'],data['currency'])
            dao.update(id, mv)
            return redirect(url_for("index")) 
        except ValueError as error: 
            flash(str(error)) 
            return render_template("update.html", the_form=data, title = "Update movement") 
