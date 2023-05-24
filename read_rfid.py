import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522




#Set up the tags


def get_rfid():
	reader = SimpleMFRC522()
	
	try:
		while True:
			
			id, text = reader.read()
			#return id, text
			print(str(id))
			time.sleep(2)
	finally:
		GPIO.cleanup()
		
		
print(str(id))
get_rfid()
