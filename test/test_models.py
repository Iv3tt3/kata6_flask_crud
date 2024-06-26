from datetime import date
from mi_cartera.models import Movement, MovementDAO, MovemenetDAOSqlite
import pytest
import os
import csv
import sqlite3

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
    with pytest.raises(ValueError):
        m = Movement("0002-01-31","Concepto",0, "EUR")

def test_fail_is_amount_not_is_float():
    with pytest.raises(ValueError):
        m = Movement("0002-01-31","Concepto","1000,25", "EUR")
    m = Movement("0002-01-31","Concepto","1100.25", "EUR")
    assert m.amount == 1100.25

def test_fail_if_amount_change_to_zero():
    m = Movement("0002-01-31","Concepto",1000, "EUR")
    with pytest.raises(ValueError):
        m.amount = 0

def test_fail_if_curency_not_in_currencies():
    with pytest.raises(ValueError):
        m = Movement("0002-01-31","Concepto",1000,"YEN")

def test_fail_if_change_currency_not_in_currencies():
    m = Movement("0002-01-31","Concepto",1000,"EUR")
    with pytest.raises(ValueError):
        m.currency = "GPD"

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
    assert cabecera == "Date,Abstract,Amount,Currency\n"

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

    assert list_reader[0] == ["Date","Abstract","Amount","Currency"]
    assert list_reader[1] == ["0002-01-31","Concepto","1000.0","EUR"]


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
    assert list_reader[0] == ["Date","Abstract","Amount","Currency"]
    assert list_reader[1] == ["0010-01-31","Primero","1000.0","EUR"]
    assert list_reader[2] == ["0002-01-31","Segundo","1000.0","EUR"]

def test_all_movements():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)
    mv1 = Movement("0010-01-01","Primero",1000,"EUR")
    dao.insert(mv1)
    mv2 = Movement("0010-01-02","Segundo",1000,"EUR")
    dao.insert(mv2)
    mv3 = Movement("0010-01-03","Tercero",1000,"EUR")
    dao.insert(mv3)

    dao.all()
    assert dao.all_movements[0] == mv1
    assert dao.all_movements[1] == mv2
    assert dao.all_movements[2] == mv3

def test_dao_get():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)
    mv1 = Movement("0010-01-01","Primero",1000,"EUR")
    dao.insert(mv1)
    mv2 = Movement("0010-01-02","Segundo",1000,"EUR")
    dao.insert(mv2)
    mv3 = Movement("0010-01-03","Tercero",1000,"EUR")
    dao.insert(mv3)

    register = dao.get(1)
    assert register == mv2

def test_dao_get_outofindex():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)
    mv1 = Movement("0010-01-01","Primero",1000,"EUR")
    dao.insert(mv1)
    mv2 = Movement("0010-01-02","Segundo",1000,"EUR")
    dao.insert(mv2)
    mv3 = Movement("0010-01-03","Tercero",1000,"EUR")
    dao.insert(mv3)

    with pytest.raises(IndexError):
        register = dao.get(5)

def test_dao_get_emptydatainfile():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)

    with pytest.raises(IndexError):
        register = dao.get(0)


def test_dao_update_movement():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)
    mv1 = Movement("0010-01-01","Primero",1000,"EUR")
    dao.insert(mv1)
    mv2 = Movement("0010-01-02","Segundo",1000,"EUR")
    dao.insert(mv2)
    mv3 = Movement("0010-01-03","Tercero",1000,"EUR")
    dao.insert(mv3)

    mv4 = Movement("0010-01-04","Cambio",1000,"EUR")
    dao.update(1,mv4)

    assert dao.get(1) == mv4


def test_dao_update2_emptydatainfile2():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)
    mv1 = Movement("0010-01-01","Primero",1000,"EUR")
    dao.insert(mv1)
    mv2 = Movement("0010-01-02","Segundo",1000,"EUR")
    dao.insert(mv2)
    mv3 = Movement("0010-01-03","Tercero",1000,"EUR")
    dao.insert(mv3)

    mv4 = Movement("0010-01-04","Cambio",1000,"EUR")
    dao.update2(2,mv4)

    f = open(path, "r")
    reader = csv.reader(f, delimiter=",", quotechar='"') 
    list_reader = list(reader)

    assert list_reader[3] == ["0010-01-04","Cambio","1000.0","EUR"]




def test_create_dao_sqlite():
    path = "base_cualquiera.db"
    if os.path.exists(path):
        os.remove(path)

    dao = MovemenetDAOSqlite(path)

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * from movements")
    assert cursor.fetchall() == []

def test_insertar_several_mov_sqlite():
    path = "base_cualquiera.db"
    if os.path.exists(path):
        os.remove(path)

    dao = MovemenetDAOSqlite(path)

    dao.insert(Movement("2001-01-01","Concept",12,"EUR", id=1))
    dao.insert(Movement("2001-02-01","Concept2",1,"EUR", id=2))

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * from movements")

    assert cursor.fetchall() == [(1,"2001-01-01","Concept",12.0,"EUR"),(2,"2001-02-01","Concept2",1.0,"EUR")]


def test_read_one_movement_sqlite():
    path = "base_cualquiera.db"
    if os.path.exists(path):
        os.remove(path)

    dao = MovemenetDAOSqlite(path)

    dao.insert(Movement("2001-01-01","Concept",12,"EUR", id=1))
    dao.insert(Movement("2001-02-01","Concept2",1,"EUR", id=2))

    assert dao.get(2) == Movement("2001-02-01","Concept2",1,"EUR", id=2)


def test_read_all_movements_sqlite():
    path = "base_cualquiera.db"
    if os.path.exists(path):
        os.remove(path)

    dao = MovemenetDAOSqlite(path)

    dao.insert(Movement("2001-01-02","Concept",12,"EUR"))
    dao.insert(Movement("2001-01-01","Concept2",1,"EUR"))

    movements = dao.get_all()
    assert movements[0] == Movement("2001-01-01","Concept2",1,"EUR", id=2)
    assert movements[1] == Movement("2001-02-02","Concept",12,"EUR", id=1)


