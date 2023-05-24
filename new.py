import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

#Set up the tags
tag = " "

def read_rfid_data():
	try:
		while True:
			print("Hold a tag near the reader")
			id, text = reader.read()
			tag = str(id)
			return tag
			
			#if id == tag:
			#	print("ERROR")
			#else:
			#	print(id)
			#	return id
			#print(f"Text: {text}")
		
			time.sleep(2) 
    
		#return id
	finally:

		GPIO.cleanup()
		
print(tag)
read_rfid_data()		
		
		

