from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def date_le_today(form, field): #El field es el campo donde pones la funcion, es decir date. El form es el formulario.
    if field.data > date.today():
        raise ValidationError("Date must be today or lower like an external function")
    #Aqui non usamos el form, porque no tenemos que validarlo con un valor del mismo formulario

#Al añadir date_le_today enn date, cuando se invoca la fucion se envian como parametro de entrada form=formulario y field=campo date porque es donde se esta validando la funcion

class MovementForm(FlaskForm):
    date = DateField("Fecha", validators =[DataRequired("La fecha es obligatoria"), date_le_today]) #Aqui añado mis validadores, aparte de los que ya tiene el formulario. Por ejemplo la funcion externa date_le_today sin invocarla. Podria crear un fichero con mis validadores, importarlos y aqui los pongo.
    #Si en vez de con una funcion externa lo hacemos con un metodo entonces seria asi:
    #date = DateField("Fecha", validators =[DataRequired("La fecha es obligatoria")]) #Si creamos el metodo no hace falta poner el metodo en los validadores, puesto que el validate busca el metodo validate_date, validate_amount, etc. y si lo encuentra lo ejecuta.
    abstract = StringField("Concepto", validators =[DataRequired("Concepto obligatorio"), Length(min=5, message="Debe tener al menos 5 caracteres")])
    amount = FloatField("Cantidad", validators = [DataRequired("Cantidad obligatoria")])
    currency = SelectField("Moneda", validators = [DataRequired("Moneda obligatoria")], choices=[("EUR", "Euros"), ("USD", "Dólares")])

    submit = SubmitField("Enviar")

    #Si lo hacemos como un metodo tenemos que usar validate_NombreDelCampo:
    def validate_date(self, field): #El field es el campo donde pones la funcion, es decir date. El form es el formulario.
        if field.data > date.today():
            raise ValidationError("Date must be today or lower like a method")
        #Aqui non usamos el form, porque no tenemos que validarlo con un valor del mismo formulario

