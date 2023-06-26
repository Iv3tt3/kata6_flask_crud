from datetime import date
import csv
import os

CURRENCIES = ("EUR","USD")

class Movement:
    def __init__(self, input_date, abstract, amount, currency):
        #input_date lo cambiamos porque entrava en conflicto con la libreria date
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
        
    @property
    def amount(self): 
        return self._amount
    
    @amount.setter
    def amount(self, value):
        self._amount = float(value)
        if self._amount == 0:
            raise ValueError("Amount can't be 0")
        
    @property
    def currency(self): 
        return self._currency
    
    @currency.setter
    def currency(self, value):
        self._currency = value
        if self._currency not in CURRENCIES:
            raise ValueError(f"Currency must be in {CURRENCIES}")
        

        
class MovementDAO:
    def __init__(self, file_path):
        self.path = file_path
        self.all_movements = [] #Creamos la lista como atributo porque necesitamos utilizarla fuera
        if not os.path.exists(self.path):
            f = open(file_path, "w") 
            f.write("date,abstract,amount,currency\n")

    def insert(self, movement):
        f = open(self.path, "a", newline="")
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow([movement.date, movement.abstract, movement.amount, movement.currency])

    def all(self):
        f = open("movements.dat","r")
        reader = csv.DictReader(f)
        self.all_movements = [] #Vaciamos la lista, sino cada vez que hagamos el metodo all (al refrescar la pagina), va haciendo un append con los movimientos 
        for row in reader:
            mov = Movement(row['Date'],row['Abstract'],row['Amount'],row['Currency'])
            self.all_movements.append(mov) #Nos crea una lista de objetos Movement