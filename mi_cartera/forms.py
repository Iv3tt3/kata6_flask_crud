#Realmente forms pertenece a la vista porque es validacion de datos de entrada. Es util para validar ficheros json tambien
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
#Esta es la clase de la que van a heredar todos los formularios

class MovementForm(FlaskForm):
    #no me tengo que preocupar de casi nada porque hereda de flaskform, solo tengo que indicarle los campos
    date = DateField("Fecha", validators =[DataRequired("La fecha es obligatoria")]) #Fields son a lo que llaman tipos de datos. Y validators heredan de wtforms.validators. Ver docs
    #Lo que pongo dentro de la instancia DataRequired es el mensaje que aparece cuando el usuario no introduce bien los datos. 
    abstract = StringField("Concepto", validators =[DataRequired("Concepto obligatorio"), Length(min=5)])
    amount = FloatField("Cantidad", validators = [DataRequired("Cantidad obligatoria")])
    currency = SelectField("Moneda", validators = [DataRequired("Moneda obligatoria")], choices=[("EUR", "Euros"), ("USD", "Dólares")])

    submit = SubmitField("Enviar")

#Al usar WTForms ya esta todo validado