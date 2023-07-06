from mi_cartera import app 
from mi_cartera.models import MovementDAO, Movement, MovemenetDAOSqlite
from flask import render_template, request, redirect, flash, url_for
from mi_cartera.forms import MovementForm


dao = MovemenetDAOSqlite(app.config.get("PATH_SQLITE")) # Antes era dao = MovemenetDAOSqlite('data/movements.db') pero hemos puesto la path en el .env

@app.route("/")
def index():
    movements = dao.get_all() 
    if dao.error != []:
        flash(f"CORRUPTED FILE. Movements with format errors in your data file: {str(dao.error)}")
    return render_template("index.html", the_movements=movements, title = "Todos") #Pasamos la lista de objetos a index.html

'''
Version que han hecho en clase:

@app.route("/")
def index():
    try:
        movements = dao.get_all()
        return render_template("index.html", the_movements=movements, title="Todos")
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("index.html", the_movements=[], title="Todos")'''



@app.route("/new_movement", methods=["GET", "POST"]) 
def new_mov():
    form = MovementForm()
    #form.currency.choices=("lolailo", "lere") Te canviaria los atributos de la instancia de form antes de meterlo en rendertemplate
    #Ya no necesito request.method porque ahora con WTForms, form es un objeto que contienen toda la informacion y mas
    if request.method == 'GET':
        return render_template("new_mov_form.html", the_form = form, title = "Alta de movimientos") 
    else:
        if form.validate(): #Esto es un metodo de la clase WTForms que llama a las validacionnes de forms.py. Aqui le decimos que si nos valida el formulario con el token haga el insert, en caso contrario no haga el insert para evitar que si nos intentan hackear no puedan. Ver forms.py, donde aparecen las validaciones
            try:
                dao.insert(Movement(str(form.date.data),form.abstract.data,form.amount.data,form.currency.data))
                return redirect(url_for("index")) #Esto permite buscar la funcion index y cambiar la ruta sin que se desconecte de otros sitios. Porque esto es parametrizable, en produccion tiene otro nombre 
            except ValueError as error: 
                flash(str(error)) 
                return render_template("new_mov_form.html", the_form=form, title = "Alta de movimientos") 
        else:
            return render_template("new_mov_form.html", the_form=form, title = "Alta de movimientos") 

@app.route("/update_movement/<int:id>", methods=["GET", "POST"])
def edit_mov(id):
    if request.method == "GET":
        try:
            mov = dao.get(id)
            if mov:
                return render_template("update.html", title="Update movement", 
                                the_form=mov, id=id)
            else:
                flash(f"Registro {id} inexistente")
                return redirect(url_for("index"))
        except:
            mov = dao.get_corrupted(id)
            if mov:
                return render_template("update_corrupted.html", title="Update movement", 
                                the_form=mov, id=id)
            else:
                flash(f"Registro {id} inexistente")
                return redirect(url_for("index"))
    else:
        data = request.form
        try:
            mv =Movement(data['date'],data['abstract'],data['amount'],data['currency'])
            dao.update(id, mv)
            return redirect(url_for("index")) 
        except ValueError as error: 
            flash(str(error)) 
            return render_template("update.html", the_form=data, title = "Update movement") 
