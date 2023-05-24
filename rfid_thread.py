from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QMessageBox, QLabel, QVBoxLayout
import  sys
from PyQt5.QtCore import QThread, pyqtSignal

import sqlite3
import RPi.GPIO as GPIO
import time
import threading
from mfrc522 import SimpleMFRC522
from MainDashboard import Ui_MainWindow
class RFIDReaderThread(QThread):
    new_data = pyqtSignal(str)
    scan_rfid_status = True
    def __init__(self):
        super().__init__()
        
    def run(self):
        reader = SimpleMFRC522()
        while self.scan_rfid_status:
            try:
                id, text = reader.read()
                self.new_data.emit(str(id))
                time.sleep(2)   
                
            except Exception as e:
                print("Error reading RFID:", e)
            GPIO.cleanup()
class RFIDWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        
        self.rfid_thread = RFIDReaderThread()
        self.rfid_thread.new_data.connect(self.update_label)
        self.rfid_thread.start()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Waiting")
        self.layout.addWidget(self.label)
        
        self.setLayout(self.layout)
        
    #def update_label(self, data):
      #  self.label.setText(data)
        

