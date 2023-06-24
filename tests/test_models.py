from datetime import date
from mi_cartera.models import Movement, MovementDAO
import pytest
import os
import csv

def test_create_movement():
    m = Movement("2001-12-01", "Sueldo", 1000, "EUR")
    assert m.date == date( 2001, 12, 1)
    assert m.abstract == "Sueldo"
    assert m.amount == 1000
    assert m.currency == "EUR"

def test_fail_if_date_grater_than_today(): #Este test es para hacer que la fecha no sea mayor que hoy
    with pytest.raises(ValueError): 
        m = Movement("9999-12-31","Concepto",1000, "EUR")

def test_change_atribute_date(): #Este test es para hacer el setter, quiero que m.date me asigne esto
    m = Movement("0002-01-31","Concepto",1000, "EUR")
    m.date = "1970-04-08" 
    assert m.date == date(1970,4,8)
    
def test_fail_if_amount_eq_zero():
    pass

def test_fail_if_amount_change_to_zero():
    pass

def test_fail_if_curency_not_in_currencies():
    pass

def test_fail_if_change_currency_not_in_currencies():
    pass

#Este test esta creado antes de hacer la clase MovementDAO
def test_create_MovementDAO(): 
    fichero = "data_mentira.dat" #Si quisieramos que el fichero se cree en una carpeta concreta se indica aqui, ej: \mi_cartera\data_mentira.dat. Si no lo indico me lo crea en la carpeta general
    if os.path.exists(fichero): #Importamos la libreria os que es del sistema operativo
        os.remove(fichero) #Si el fichero existe, me lo cargo porque en este test lo quiero crear desde 0
    #ahora me creo el Dao que quiero que me escriba las cabeceras
    dao = MovementDAO(fichero) #En esta linea esperamos que se agregue las cabeceras porque el fichero no existe, entonces si el fichero no existe debe crearlo y escribir las cabeceras
    
    f = open(fichero, "r") #
    cabecera = f.readline() # Y aqui leo la cabecera con el readline()

    #Y ahora creo el test, ya que la cabecera tiene que ser esto:
    assert cabecera == "date,abstract,amount,currency\n"

    #Este test me testea MovementDAO e instancia la clase, por lo tanto me crea un data_mentira.dat en el la carpeta principal. Si quisiera ponerlo en una carpeta concreta se tendria que indicar en la linea 35.

#Este test esta creado antes de hacer el metodo .insert
def test_insert_movement_MovementDAO(): 
    fichero = "data_mentira.dat" 
    if os.path.exists(fichero): 
        os.remove(fichero) 

    dao = MovementDAO(fichero) 
    movement_mentira = Movement("0002-01-31","Concepto",1000, "EUR") #Creamos un movimiento que vamos a instertar
    dao.insert(movement_mentira) #Insertamos el movimiento con el metodo insert
    
    #Para comprovar si el test ha ido bien, tenemos que leer el fichero con csv.reader sabiendo que la primera linea va a ser el cabecero y la segunda linea el movimiento que le hemos pasado
    f = open(fichero, "r") 
    reader = csv.reader(f, delimiter=",", quotechar='"') #Importo la libreria csv
    list_reader = list(reader)

    #Ahora ya podemos mirar si lo que leemos es lo que le hemos introducido

    assert list_reader[0] == ["date","abstract","amount","currency"]
    assert list_reader[1] == ["0002-01-31","Concepto","1000","EUR"]


#En este test provamos si hacemos una intancia y se crea el fichero. Si luego insertamos un dato funciona. Pero si luego volvemos a crear una instancia en el nuevo fichero, elimina el movimiento porque lo sobrescribe. Queremos evitar eso, entonces aunque instancie otra vez sobre el mismo fichero lo que debe hacer es no sobreescribirlo si existe, y luego en el caso de que haga el metodo insert me añada una tercera linea con los datos.

def test_instance_dao_path_exists():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)

    dao = MovementDAO(path)
    dao.insert(Movement("0010-01-31","Primero",1000, "EUR"))
    dao = MovementDAO(path)
    dao.insert(Movement("0002-01-31","Segundo",1000, "EUR"))

    f = open(path, "r")
    reader = csv.reader(f, delimiter=",", quotechar='"') 
    list_reader = list(reader)

    assert len(list_reader) == 3
    assert list_reader[0] == ["date","abstract","amount","currency"]
    assert list_reader[1] == ["0010-01-31","Primero","1000","EUR"]
    assert list_reader[2] == ["0002-01-31","Segundo","1000","EUR"]