import sqlite3
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
con = sqlite3.connect('rfid.db')
cursor = con.cursor()
  
try:
	id, text = reader.read()
	idno = str(id)
	print(idno)
                #print(idno)
	#con = sqlite3.connect('rfid.db')
    #cursor2 = con.cursor()
	cursor.execute("select * from borrowlist where tagB= '"+ idno +"'")
except sqlite3.OperationalError as e:
	print("Error", e)
else:
	result2 = cursor.fetchone()
	print("Query Results:", result2)
                #cursor1 = con.cursor()
                #cursor1.execute("select * from borrowlist where tagB= '"+ idno +"'")
                #result1 = cursor1.fetchone()
