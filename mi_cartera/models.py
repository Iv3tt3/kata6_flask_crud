from datetime import date
import csv
import os

#Deberes hacer que amount sea solo numero y currency solo sea EUR y USD

class Movement:
    def __init__(self, input_date, abstract, amount, currency):
        self.date=input_date
        self.abstract=abstract
        self.amount=amount
        self.currency=currency

    @property
    def date(self): 
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = date.fromisoformat(value)
        if self._date > date.today():
            raise ValueError("Date must be today or lower")
        
class MovementDAO:
    def __init__(self, file_path):
        self.path = file_path
        if not os.path.exists(self.path):
            #Si no existe el path debe crear el fichero
            f = open(file_path, "w") #Creamos el fichero en escritura y escribimos la cabecera
            f.write("date,abstract,amount,currency\n")

    def insert(self, movement):
        f = open(self.path, "a", newline="")#El newline es para la gente de windows
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow([movement.date, movement.abstract, movement.amount, movement.currency])

    def all(self):
        pass
    #Devolver una lista de Movements con todos los registros, transformados en objeto Movements.
        #Tiene que devolver todos los movimientos no como una cadena sino como una lista de movimientos, de movimientos de la clase Movement. Tiene que hacer: Abrir el fichero en modo lectura, leer todos los registros, quitando la cabecera. Y cada registro lo trannsformais en un movimiento, lo meteis en una lista y devolveis esa lista