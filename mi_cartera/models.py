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
        
    def __eq__ (self, other):
        return self.date == other.date and self.abstract == other.abstract and self.amount == other.amount and self.currency == other.currency
    #Anadimos el metodo magico de equal porque sino el test_all_movements peta ya que compara dos objetos diferentes y no pasa el test

    def __repr__(self):
        return '{} {} {} {}'.format(self.date, self.abstract,  self.amount, self.currency)
    #Anadimos el metodo magico repr porque el test falla y asi vemos lo que nos esta comparando

class MovementDAO:
    def __init__(self, file_path):
        self.path = file_path
        self.error = []
        self.all_movements = [] #Creamos la lista como atributo porque necesitamos utilizarla fuera
        if not os.path.exists(self.path):
            f = open(file_path, "w") 
            f.write("Date,Abstract,Amount,Currency\n") #Esta linea estava mal
    
    
    def insert(self, movement):
        f = open(self.path, "a", newline="")
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow([movement.date, movement.abstract, movement.amount, movement.currency])

    def all(self):
        f = open(self.path,"r") #Esta linea estava mal
        reader = csv.DictReader(f)

        self.all_movements = [] #Vaciamos las listas, sino cada vez que hagamos el metodo all (al refrescar la pagina), va haciendo un append
        self.error = []
        for row in reader:
            try:
                mov = Movement(row['Date'],row['Abstract'],row['Amount'],row['Currency'])
                self.all_movements.append(mov) #Nos crea una lista de objetos Movement
            except ValueError as error:
                mov = Movement('0001-01-01',f"FORMAT ERROR {error}",0.001,"EUR")
                self.all_movements.append(mov)
                self.error.append(error)
    
    def get(self, id):
        f = open(self.path,"r") #Esta linea estava mal
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        i = float("-inf")
        for i, row in enumerate(reader):
            if i == id:
                break

        if id > i:
            raise IndexError("Movement don't exist")
        mov = Movement(row['Date'],row['Abstract'],row['Amount'],row['Currency'])
        return mov

    
    def update2(self, id, movement):
        f = open(self.path,"r")
        reader = csv.DictReader(f)
        i = float("-inf")
        f2 = MovementDAO("updated_movements.dat")
        for i, row in enumerate(reader):
            if i != id:
                mov = Movement(row['Date'],row['Abstract'],row['Amount'],row['Currency'])
                f2.insert(mov)
            else:
                f2.insert(movement)
        os.rename("updated_movements.dat", self.path)
        