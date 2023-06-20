from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route("/")
def index():
    f = open("movements.dat", "r")
    reader = csv.DictReader(f)
    movements = list(reader)

    return render_template("index.html", the_movements=movements) #Con esto le estoy diciendo que en el render utilice los movements

#Esto mezcla el index.htm con los datos movements. Donde jinja2 encuentre una doble llave {{}}, le pone los datos.