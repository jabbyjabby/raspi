from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QMessageBox, QLabel
import  sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from WelcomePage0 import Ui_Dialog
from MainDashboard import Ui_MainWindow
import sqlite3
from mysql.connector import errorcode
import mysql.connector
import RPi.GPIO as GPIO
import time
import threading
from rfid_thread import RFIDReaderThread
from datetime import datetime

from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

global con3
con3 = sqlite3.connect('rfid.db')
global cursorlite
cursorlite = con3.cursor()

global con
con = mysql.connector.connect(
            host="192.168.1.23",
            username="root",
            password="pi",
            db="rfid-2" )
        
global cursor
cursor = con.cursor(buffered=True)
#global scan_rfid_status
#scan_rfid_status = False
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("WelcomePage0.ui", self)
        #self.signinButton.clicked.connect(self.gotologin)
        self.signupButton.clicked.connect(self.gotosignup)
        global scan_rfid_status
        self.scan_rfid_status = False
        
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

    def gotosignup(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(2)
    


class LoginScreen(QDialog):

    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("LoginPage.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.loginfunction)
        self.signupButton.clicked.connect(self.signupfunction)
        # self.dashboard = MainDashboard()
        global scan_rfid_status
        self.scan_rfid_status = False
        

    def loginfunction(self):
        un = self.usernamefield.text()
        pw = self.passwordfield.text()
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
          #  host="192.168.1.23",
          #  username="root",
          #  password="pi",
          #  db="rfid-2" )
        
        cursor = con.cursor(buffered=True)
        cursor.execute("select * from userlist where username='"+ un +"' and password= '"+ pw +"'")
        result = cursor.fetchone()
        self.usernamefield.setText("")
        self.passwordfield.setText("")
        self.loginerror1.setText("")
        self.loginerror.setText("")

        if result:
            # self.loginButton.clicked.connect(self.gotoDashboard)
            QMessageBox.information(self, "Data", "Login successfully!")
            widget.setCurrentIndex(3)
            global keep_scanning
            keep_scanning = True
            #global keep_scanning

        elif len(un)==0 or len(pw)==0:
            self.loginerror1.setText("Please input all fields.")
        else:
            self.loginerror.setText("Invalid username or password.")
            # QMessageBox.information(self, "Login Output", "Invalid Data/Signup to access!")


    def signupfunction(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(2)

    def gotoDashboard(self):
        dashboard = MainDashboard()
        widget.addWidget(dashboard)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(3)


class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen, self).__init__()
        loadUi("SignupPage.ui", self)
        #self.passwordtextfield.setEchoMode(QtWidgets.QLineEdit.Password)
        #self.confirmpasswordtextfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.connectMysql.clicked.connect(self.mysqlconnectorfunction)
        #self.loginButton.clicked.connect(self.loginfunction)
        global scan_rfid_status
        self.scan_rfid_status = False

    def registerfunction(self):

        un = self.usernametextfield.text()
        pw = self.passwordtextfield.text()
        cpw = self.confirmpasswordtextfield.text()
        email = self.emailtextfield.text()
        phone = self.phonetextfield.text()
        
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
          #  host="192.168.1.23",
          #  username="root",
          #  password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        cursorlite.execute("select * from userlist where username='"+ un +"' and password= '"+ pw +"'")
        result = cursorlite.fetchone()


        if result:
            QMessageBox.information(self, "Data", "The data is already used choose another data")

        elif len(un) == 0 or len(pw) == 0 or len(cpw) == 0 or len(email) == 0 or len(phone) == 0:
            self.cpwlabel_2.setText("Please input all fields.")
            return

        elif len(pw) != 6:
            self.cpwlabel.setText("Password must have 6 characters")
            return
        elif pw != cpw:
            self.cpwlabel.setText("Password does not matched.")

        else:
            cursor.execute("insert into userlist values('"+ un +"','"+ pw +"','"+ email +"','"+ phone +"')")
            cursorlite.execute("insert into userlist values('"+ un +"','"+ pw +"','"+ email +"','"+ phone +"')")
            con.commit()
            con3.commit()
            #db.commit()
            QMessageBox.information(self, "Data", "You have been successfully registered.")
            self.usernametextfield.setText("")
            self.passwordtextfield.setText("")
            self.confirmpasswordtextfield.setText("")
            self.emailtextfield.setText("")
            self.phonetextfield.setText("")
            widget.setFixedHeight(601)
            widget.setFixedWidth(1013)
            widget.setCurrentIndex(1)
            
    def mysqlconnectorfunction(self):
        
        global host
        host = ""
        global username
        username= ""
        global password
        password= ""
        global db
        db= ""
        
        try:
            hostname = self.hostnamefield.text()
            user = self.usernamefield.text()
            passw = self.passwordfield.text()
            database = self.databasefield.text()
       
            global con
            con = mysql.connector.connect(
                host= hostname,
                username= user,
                password= passw,
                db= database )
        
            global cursor
            cursor = con.cursor(buffered=True)
            widget.setCurrentIndex(1)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.information(self, "Error", "INVALID USERNAME OR PASSWORD")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.information(self, "Error", "INVALID DATABASE")
            else :
                QMessageBox.information(self, "IP Address", f"{err}")
            
        print(db)
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
          #  host="192.168.1.23",
          #  username="root",
          #  password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        
        


    def loginfunction(self):
        self.cpwlabel.setText("")
        self.cpwlabel_2.setText("")
        self.usernametextfield.setText("")
        self.passwordtextfield.setText("")
        self.confirmpasswordtextfield.setText("")
        self.emailtextfield.setText("")
        self.phonetextfield.setText("")
        login = LoginScreen()
        widget.addWidget(login)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

class MainDashboard(QMainWindow):
    def __init__(self):
        super(MainDashboard, self).__init__()
        loadUi("MainDashboard.ui", self)
        self.transactlist.clicked.connect(self.transactnav)
        self.borrower_1.clicked.connect(self.borrowernav)
        self.equip.clicked.connect(self.equipmentnav)
        #self.myprofile.clicked.connect(self.myprofilenav)
        self.logout.clicked.connect(self.logoutnav)
        self.viewmoreBtn.clicked.connect(self.transactnav)
        
        self.loadTable()
        
        header = self.data_table.horizontalHeader()
        self.data_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.data_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        #global scan_rfid_status
        self.scan_rfid_status = True
       
        
        self.rfid_thread = RFIDReaderThread()
        self.rfid_thread.new_data.connect(self.update_label)
        self.rfid_thread.start()
        
        
   
        self.search.textChanged.connect(self.searchData)
        

    def searchData(self):
        search = self.search.text().strip()
        if not search:
            self.loadTable()
            
            
        else:
            #con = sqlite3.connect('rfid.db')
            #cursor = con.cursor(
            
            #con = mysql.connector.connect(
            #host="192.168.1.23",
            #username="root",
            #password="pi",
            #db="rfid-2" )
        
            #cursor = con.cursor(buffered=True)
        
            query = f"SELECT rfid_tag, name, date, time, action, bor_returnName FROM rfid_data WHERE rfid_tag LIKE '%{search}%' OR name LIKE '%{search}%' OR date LIKE '%{search}%' OR time LIKE '%{search}%' OR action LIKE '%{search}%' OR bor_returnName LIKE '%{search}%'"
            
            cursor.execute(query)
            data = cursor.fetchall()
            
            #cursor.close()
            self.updateDataSearch(data)

    def updateDataSearch(self, data):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
           # host="192.168.1.23",
           # username="root",
           # password="pi",
           # db="rfid-2" )
        
        #cursor = con.cursor()
        
        
        self.data_table.setRowCount(len(data))
        for row_number, row_data in enumerate(data):
            #self.tableWidget.insertRow(row_number)
            for column_number, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.data_table.setItem(row_number, column_number, item)
        #cursor.close()
        
    def update_label(self, data):
        self.data = str(data)
        self.equipment.setText(self.data)
        print(self.data)
        
        self.cur_date = datetime.now().strftime("%Y-%m-%d")
        self.cur_time = datetime.now().strftime("%H:%M:%S")
        
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
       
        cursorlite2 = con3.cursor()
        cursorlite3 = con3.cursor()
        cursor2 = con.cursor(buffered=True)
        cursor3 = con.cursor(buffered=True)
        cursorlite2.execute("select NameD from devicelist where tagD= '"+ self.data +"'")
        result2 = cursorlite2.fetchone()
        cursorlite1 = con3.cursor()
        cursor1 = con.cursor(buffered=True)
        cursorlite1.execute("select NameB from borrowlist where tagB= '"+ self.data +"'")
        result1 = cursorlite1.fetchone()
        
        
        
		#name 
        self.equipmentInOut.setText("Tag") 
        self.borrowerInOut.setText("Name")
        self.timeInOut.setText("Time")
        self.dateInOut.setText("Date")
        read_count = {}
        
        #self.action = " "
        if result1:
            #self.equipment.setText(self.data)
            self.name1 = result1[0]
            self.borrower.setText(self.name1)
            self.time.setText(self.cur_time)
            self.date.setText(self.cur_date)
            cursorlite1.execute("SELECT COUNT(*) FROM rfid_data WHERE rfid_tag= '"+ self.data +"'")
            self.record_count = cursorlite1.fetchone()[0]
            #read_count[name1] += 1
            if self.record_count % 2 == 0:
                self.action = "Borrower In"
                self.bor_return.setText("Action")
                self.track.setText(self.action)
                
                cursor1.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ self.name1 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                con.commit()
                cursorlite1.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ self.name1 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                con3.commit()
                self.loadTable()
                TransactionList.loadDataTransact()
               
                 
                
                
                    
                    
            else:
                self.action = "Borrower Out"
                self.bor_return.setText("Action")
                self.track.setText(self.action)
                
                cursor1.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ self.name1 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                con.commit()
                cursorlite1.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ self.name1 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                con3.commit()
                self.loadTable()
                
                
            
          
        elif result2:
            
            
            
            #self.equipment.setText(self.data)
            name2 = result2[0]
            self.borrower.setText(name2)  
            self.time.setText(self.cur_time)
            self.date.setText(self.cur_date)
            cursor2.execute("SELECT action FROM rfid_data WHERE rfid_tag= '"+ self.data +"'")
            data2 = cursor2.fetchone()
            datta2 = data2
            
            
              
                
            if self.action == "Borrower In":
                cursorlite2.execute("select bor_returnName from rfid_data where name= '"+ self.name1 +"'")
                borrower_name = cursorlite2.fetchone()
                bor_name = borrower_name[0]
            #cursor2.execute("select action from rfid_data where rfid_tag= '"+ self.data +"'")
                act_borrowed = cursor2.fetchone()
            #act = act_borrowed[0]
            
                
                cursorlite2.execute("SELECT COUNT(*) FROM rfid_data WHERE rfid_tag= '"+ self.data +"'")
                self.record_count2 = cursorlite2.fetchone()[0]
                #cursor2.execute("SELECT * FROM rfid_data ORDER BY time DESC") 
                if bor_name == self.name1 and self.record_count2 % 2 == 0:
                #self.action = (self.name1)
                    self.bor_return.setText("Borrowed by")
                    self.track.setText(self.name1)
                    self.action = ("Borrowed")
                    print(self.action)
                    cursor2.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ name2 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                    con.commit() 
                    cursorlite2.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ name2 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                    con3.commit() 
                    self.loadTable()
                   
                    
               
            
                elif bor_name != self.name1 and self.record_count2 % 2 == 0: 
                    QMessageBox.information(self, "Error", "Please make the borrower return the device")
                    return
                else:
                    cursorlite2.execute("select action from rfid_data where rfid_tag= '"+ self.data +"'")
                    act_borrowed = cursorlite2.fetchone()
                    act = act_borrowed[0]
                
                    self.bor_return.setText("Returned by")
                    self.track.setText(self.name1)
                    self.action = ("Returned")
                    cursor2.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ name2 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                    con.commit() 
                    cursorlite2.execute("INSERT INTO rfid_data (rfid_tag, name, date, time, action, bor_returnName) VALUES ('"+ self.data +"', '"+ name2 +"', '"+ self.cur_date +"', '"+ self.cur_time +"', '"+ self.action +"', '"+ self.name1 +"')")
                    con3.commit() 
                    self.loadTable()
                   
                    
            elif datta2 != "Borrower In" :
                QMessageBox.information(self, "Error", "Please make the borrower with tag return the device")
                self.bor_return.setText("Invalid")
                self.track.setText("Unknown")
                self.action2 = ("Invalid not Borrower")
                return        
                
            
                
            else:
                QMessageBox.information(self, "Error", "Please make the borrower return the device")
                
            
        
                 
                           
        else:
            self.borrower.setText("Unknown")   
            self.equipmentIcon.setText  
            QMessageBox.information(self, "Error", "Unknown tag, Please register...")
               
    
       
       
        
    def loadTable(self):
        
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
        #    host="192.168.1.23",
        #    username="root",
        #    password="pi",
        #    db="rfid-2" )
        
        #cursorlite = con3.cursor()
       
        query = "SELECT rfid_tag, name, date, time, action, bor_returnName FROM rfid_data ORDER BY date, time DESC"
        #cursor = db.cursor()
        cursorlite.execute(query)
        result = cursorlite.fetchall()
        self.data_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.data_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.data_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        #cursorlite.close()
        
    def equipmentnav(self):
        equipment = Equipment()
        widget.addWidget(equipment)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(4)

    def borrowernav(self):
        borrower = Borrower()
        widget.addWidget(borrower)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(5)

    def transactnav(self):
        transact = TransactionList()
        widget.addWidget(transact)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(6)

    def logoutnav(self):
        QMessageBox.information(self, "Data", "You have been successfully logout.")
        logout = LoginScreen()
        widget.addWidget(logout)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

    def myprofilenav(self):
        myprofile = MyProfile()
        widget.addWidget(myprofile)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(7)
        
    

class Equipment(QMainWindow):
    def __init__(self):
        super(Equipment, self).__init__()
        loadUi("Equipment.ui", self)
        self.loadData()
        self.transactlist_2.clicked.connect(self.transactnav)
        self.borrower_2.clicked.connect(self.borrowernav)
        self.home_2.clicked.connect(self.gotoDashboard)
        self.logout_2.clicked.connect(self.logoutnav)
        #self.myprofile_2.clicked.connect(self.myprofilenav)

        self.add.clicked.connect(self.addnav)
        #self.LoadData.clicked.connect(self.loadData)
        self.searchbut.clicked.connect(self.searchData)
        self.edit.clicked.connect(self.editnav)
        self.dele.clicked.connect(self.delnav)

        self.tableWidget.cellDoubleClicked.connect(self.selectedCell)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        global scan_rfid_status
        self.scan_rfid_status = False
        
        self.search.textChanged.connect(self.searchData)
        

    def searchData(self):
        search = self.search.text().strip()
        if not search:
            self.loadData()
            
            
        else:
            #con = sqlite3.connect('rfid.db')
            #cursor = con.cursor()
            
            #con = mysql.connector.connect(
            #host="192.168.1.23",
            #username="root",
            #password="pi",
            #db="rfid-2" )
        
            #cursor = con.cursor(buffered=True)
        
        
        #try:
            query = f"SELECT tagD, NameD, DescD FROM devicelist WHERE tagD LIKE '%{search}%' OR NameD LIKE '%{search}%' OR DescD LIKE '%{search}%'"
            #value = (search, search, search,)
            #cursor = db.cursor()
            #cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            #cursor.close()
            self.updateDataSearch(data)

    def updateDataSearch(self, data):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
           # host="192.168.1.23",
            #username="root",
           # password="pi",
           # db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        self.tableWidget.setRowCount(len(data))
        for row_number, row_data in enumerate(data):
            #self.tableWidget.insertRow(row_number)
            for column_number, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_number, column_number, item)
        #cursor.close()
    
    def loadData(self):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
          #  password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        query = "SELECT tagD, NameD, DescD FROM devicelist"
        #cursor = db.cursor()
        cursorlite.execute(query)
        result = cursorlite.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        #cursorlite.close()

    def selectedCell(self):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
           # host="192.168.1.23",
           # username="root",
          #  password="pi",
           # db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)

        #self.index = self.tableWidget.selectedItems()
        query = "SELECT tagD, NameD, DescD FROM devicelist"
        #value = (self.index[1].text(),)
        cursor.execute(query)
        data = cursor.fetchall()
        selected_items1 = self.tableWidget.selectedItems()
        try:
            
            if selected_items1:
                tag_item = selected_items1[0]
                name_item = selected_items1[1]
                des_item = selected_items1[2]
                
                self.TagDev_3.setText(tag_item.text())
                self.NameDev_3.setText(name_item.text())
                self.DescDev_3.setText(des_item.text())
        except:
            print("Failed")
        

    def gotoDashboard(self):
        #dashboard = MainDashboard()
        #widget.addWidget(dashboard)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(3)
        #self.scan_rfid_status = True
        #global keep_scanning
        #keep_scanning = True
        #self.rfid_thread = RFIDReaderThread()
       # self.rfid_thread.new_data.connect(self.update_label)
        #self.rfid_thread.start()

    def borrowernav(self):
        borrower = Borrower()
        widget.addWidget(borrower)
        widget.setCurrentIndex(5)

    def transactnav(self):
        transact = TransactionList()
        widget.addWidget(transact)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(6)

    def logoutnav(self):
        QMessageBox.information(self, "Data", "You have been successfully logout.")
        logout = LoginScreen()
        widget.addWidget(logout)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

    def myprofilenav(self):
        myprofile = MyProfile()
        widget.addWidget(myprofile)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(7)

    def addnav(self):

        TagD = self.TagDev_3.text()
        NameD = self.NameDev_3.text()
        DescD = self.DescDev_3.text()
        # ScanD = self.ScanDev.pushButton()

        #con3 = sqlite3.connect('rfid.db')
        #cursorlite1 = con3.cursor()
        
        #con = mysql.connector.connect(
        #    host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
        #cursor1 = con.cursor(buffered=True)
        cursor.execute("select * from devicelist where tagD='"+ TagD +"' OR NameD= '"+ NameD +"'")
        result1 = cursor.fetchone()


        if result1:
            QMessageBox.information(self, "Data", "The data is already used choose another data")

        elif len(TagD) == 0 or len(NameD) == 0 or len(DescD) == 0:
            self.errorlabel_3.setText("Please input all fields.")

        else:
            cursor.execute("insert into devicelist values('"+ TagD +"','"+ NameD +"','"+ DescD +"')")
            con.commit()
            cursorlite.execute("insert into devicelist values('"+ TagD +"','"+ NameD +"','"+ DescD +"')")
            con3.commit()
            QMessageBox.information(self, "Data", "Device have been successfully Added.")
            self.TagDev_3.setText("")
            self.NameDev_3.setText("")
            self.DescDev_3.setText("")
            self.errorlabel_3.setText("")
            self.loadData()

    def editnav(self):
        # edit = EditDevice()
        # widget.addWidget(edit)
        # widget.setCurrentIndex(9)
        
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
          #  password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        NameD = self.NameDev_3.text()
        TagD = self.TagDev_3.text()
        DescD = self.DescDev_3.text()
        cursor.execute("SELECT * FROM devicelist WHERE tagD='"+ TagD +"' OR NameD= '"+ NameD +"'")
        result = cursor.fetchone()
        if result:
            if not (result[0] == TagD and result[1]  == NameD and result[2] == DescD):
                editq = "UPDATE devicelist SET tagD = ?, NameD = ?, DescD = ? WHERE tagD = ?"
                value = (TagD, NameD, DescD, TagD, )

                cursor.execute(editq, value)
                con.commit()
                
                cursorlite.execute(editq, value)
                con3.commit()
                
                QMessageBox.information(self, "Data", "Edit Successfully")
                self.TagDev_3.setText("")
                self.NameDev_3.setText("")
                self.DescDev_3.setText("")
                self.errorlabel_3.setText("")
                self.loadData()
            # else:
            #     QMessageBox.information(self, "Data", "Data")

        else:
            QMessageBox.information(self, "Data", "Data does not Exist.")
            self.errorlabel_3.setText("")
            

    def delnav(self):
        # dele = DeleteDevice()
        # widget.addWidget(dele)
        # widget.setCurrentIndex(10)
        
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con3.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        NameD = self.NameDev_3.text()
        TagD = self.TagDev_3.text()
        cursor.execute("SELECT * FROM devicelist WHERE tagD='"+ TagD +"' OR NameD= '"+ NameD +"'")
        result = cursor.fetchone()
        if result:
            # deleteq = "DELETE FROM devicelist WHERE NameD = $s"
            # value = (NameD,)
            # cursor.execute(deleteq, value)
            # db.commit()
            # QMessageBox.information(self, "Data", "Deleted Successfully")
            # self.NameDev_2.setText("")
            # self.backDev()
            # QMessageBox.information(self, "Data", "Data does not Exist.")
        # else:
            # QMessageBox.information(self, "Data", "Data does not Exist.")
            deleteq = "DELETE FROM devicelist WHERE NameD = ?"
            value = (NameD, )
        # try:
            cursor.execute(deleteq, value)
            con.commit()
            
            cursorlite.execute(deleteq, value)
            con3.commit()
            
            QMessageBox.information(self, "Data", "Deleted Successfully")
            self.NameDev_3.setText("")
            self.TagDev_3.setText("")
            self.DescDev_3.setText("")
            self.errorlabel_3.setText("")
            self.loadData()
        # except:
        else:
            print("Failed DELETE")
            QMessageBox.information(self, "Data", "Data does not Exist.")
            # cursor2.execute(deleteq, value)
            # db1.commit()
            # QMessageBox.information(self, "Data", "Deleted Successfully")
            # self.NameDev_2.setText("")
            # self.backDev()

class Borrower(QMainWindow):
    def __init__(self):
        super(Borrower, self).__init__()
        loadUi("Borrower.ui", self)
        self.loadDataBorrower()
        self.transactlist_3.clicked.connect(self.transactnav)
        self.equip_3.clicked.connect(self.equipmentnav)
        self.home_3.clicked.connect(self.gotoDashboard)
        self.logout_3.clicked.connect(self.logoutnav)
        #self.myprofile_3.clicked.connect(self.myprofilenav)

        self.add.clicked.connect(self.addnav)
        #self.LoadData.clicked.connect(self.loadDataBorrower)
        self.searchbut_3.clicked.connect(self.searchDataBorrower)
        self.edit.clicked.connect(self.editnav)
        self.dele.clicked.connect(self.delnav)
        self.search_3.textChanged.connect(self.searchDataBorrower)

        self.tableWidget.cellDoubleClicked.connect(self.selectedCellBorrower)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        global scan_rfid_status 
        self.scan_rfid_status = False
        
    def loadDataBorrower(self):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
          ##  password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        query = "SELECT tagB, NameB, DescB, number, gmail FROM borrowlist"
        #cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        #cursor.close()

    def selectedCellBorrower(self):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
          #  password="pi",
         #   db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
       # cursor.execute("SELECT tagB, NameB, DescB, number, gmail FROM borrowlist")
        #data = cursor.fetchall()
        
        query = "SELECT tagB, NameB, DescB, number,gmail FROM borrowlist"
        #value = (self.index[4].text(),)
        cursor.execute(query)
        data = cursor.fetchall()
        selected_items = self.tableWidget.selectedItems()
        try:
            #cursor.execute(query)
            #row = cursor.fetchall()
            

            if selected_items:
                tag_item = selected_items[0]
                name_item = selected_items[1]
                des_item = selected_items[2]
                num_item = selected_items[3]
                gmail_item = selected_items[4]
                
                self.TagBor.setText(tag_item.text())
                self.NameBor.setText(name_item.text())
                self.DescBor.setText(des_item.text())
                self.number.setText(num_item.text())
                self.gmail.setText(gmail_item.text())

        except:
            print("Failed")
    
    
        

    def searchDataBorrower(self):
        search = self.search_3.text().strip()
        if not search:
            self.loadDataBorrower()
            
            
        else:
            #con = sqlite3.connect('rfid.db')
            #cursor = con.cursor()
            
           # con = mysql.connector.connect(
           # host="192.168.1.23",
           # username="root",
           # password="pi",
           # db="rfid-2" )
        
            #cursor = con.cursor(buffered=True)
        #try:
            query = f"SELECT tagB, NameB, DescB, number, gmail FROM borrowlist WHERE tagB LIKE '%{search}%' OR NameB LIKE '%{search}%' OR DescB LIKE '%{search}%' OR number LIKE '%{search}%' OR gmail LIKE '%{search}%'"
            #value = (search, search, search,)
            #cursor = db.cursor()
            #cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
           # cursor.close()
            self.updateDataSearchBorrower(data)

    def updateDataSearchBorrower(self, data):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        self.tableWidget.setRowCount(len(data))
        for row_number, row_data in enumerate(data):
            #self.tableWidget.insertRow(row_number)
            for column_number, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_number, column_number, item)

   
    


    def addnav(self):

        TagB = self.TagBor.text()
        NameB = self.NameBor.text()
        DescB = self.DescBor.text()
        num = self.number.text()
        gmail = self.gmail.text()
        # ScanD = self.ScanDev.pushButton()

        #con3 = sqlite3.connect('rfid.db')
        #cursorlite1 = con3.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
        #cursor1 = con.cursor(buffered=True)
        cursor.execute("select * from borrowlist where tagB='"+ TagB +"' OR NameB= '"+ NameB +"'")
        result1 = cursor.fetchone()


        if result1:
            QMessageBox.information(self, "Data", "The data is already used choose another data")

        elif len(TagB) == 0 or len(NameB) == 0 or len(DescB) == 0 or len(num) == 0 or len(gmail) == 0:
            self.errorlabel_3.setText("Please input all fields.")

        else:
            cursor.execute("insert into borrowlist values('"+ TagB +"','"+ NameB +"','"+ DescB +"','"+ num +"','"+ gmail +"')")
            con.commit()
            
            cursorlite.execute("insert into borrowlist values('"+ TagB +"','"+ NameB +"','"+ DescB +"','"+ num +"','"+ gmail +"')")
            con3.commit()
            
            #db.commit()
            QMessageBox.information(self, "Data", "Borrower have been successfully Added.")
            self.TagBor.setText("")
            self.NameBor.setText("")
            self.DescBor.setText("")
            self.number.setText("")
            self.gmail.setText("")
            self.errorlabel_3.setText("")
            self.loadDataBorrower()

    def editnav(self):
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con.cursor()
        
        #con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
         #   password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        NameBor = self.NameBor.text()
        TagBor = self.TagBor.text()
        DescBor = self.DescBor.text()
        num = self.number.text()
        gmailBor = self.gmail.text()
        cursor.execute("SELECT * FROM borrowlist WHERE tagB='"+ TagBor +"' OR NameB= '"+ NameBor+"'")
        result = cursor.fetchone()
        if result:
        # try:
            if not (result[0] == TagBor and result[1]  == NameBor and result[2] == DescBor and result[3] == num and result[4] == gmailBor):
                editq = "UPDATE borrowlist SET tagB = ?, NameB = ?, DescB = ?, number = ?, gmail = ? WHERE tagB = ?"
                value = (TagBor, NameBor, DescBor, num, gmailBor, TagBor,)
                cursor.execute(editq, value)
                con.commit()
                
                cursorlite.execute(editq, value)
                con3.commit()
                
                #db.commit()
                QMessageBox.information(self, "Data", "Edit Successfully")
                self.TagBor.setText("")
                self.NameBor.setText("")
                self.DescBor.setText("")
                self.number.setText("")
                self.gmail.setText("")
                self.errorlabel_3.setText("")
                self.loadDataBorrower()

        else:
            QMessageBox.information(self, "Data", "Borrower does not Exist.")
            self.errorlabel_3.setText("")

    def delnav(self):
        #con3 = sqlite3.connect('rfid.db')
        #cursorlite = con.cursor()
        
       # con = mysql.connector.connect(
        #    host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
       # cursor = con.cursor(buffered=True)
        
        NameB = self.NameBor.text()
        TagB = self.TagBor.text()
        cursor.execute("SELECT * FROM borrowlist WHERE tagB='"+ TagB +"' OR NameB= '"+ NameB +"'")
        result = cursor.fetchone()

        if result:
            deleteq = "DELETE FROM borrowlist WHERE NameB = ?"
            value = (NameB, )
            cursor.execute(deleteq, value)
            con.commit()
            
            cursorlite.execute(deleteq, value)
            con3.commit()
            
            #db.commit()
            QMessageBox.information(self, "Data", "Deleted Successfully")
            self.NameBor.setText("")
            self.TagBor.setText("")
            self.DescBor.setText("")
            self.errorlabel_3.setText("")
            self.loadDataBorrower()

        else:
            print("Failed DELETE")
            QMessageBox.information(self, "Data", "Borrower does not Exist.")

    def gotoDashboard(self):
        #dashboard = MainDashboard()
        #widget.addWidget(dashboard)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(3)
       

    def equipmentnav(self):
        equipment = Equipment()
        widget.addWidget(equipment)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(4)

    def transactnav(self):
        transact = TransactionList()
        widget.addWidget(transact)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(6)

    def logoutnav(self):
        QMessageBox.information(self, "Data", "You have been successfully logout.")
        logout = LoginScreen()
        widget.addWidget(logout)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

    def myprofilenav(self):
        myprofile = MyProfile()
        widget.addWidget(myprofile)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(7)

class TransactionList(QMainWindow):
    def __init__(self):
        super(TransactionList, self).__init__()
        loadUi("Transaction List.ui", self)
        self.home_4.clicked.connect(self.gotoDashboard)
        self.borrower_4.clicked.connect(self.borrowernav)
        self.equip_4.clicked.connect(self.equipmentnav)
        self.logout_4.clicked.connect(self.logoutnav)
        #self.myprofile_4.clicked.connect(self.myprofilenav)
        self.search.textChanged.connect(self.searchDataTransact)
        global scan_rfid_status
        self.scan_rfid_status = False
        self.loadDataTransact()
        
        header = self.transactTable.horizontalHeader()
        self.transactTable.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.transactTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.loadDataTransact()
        
    def loadDataTransact(self):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
       # con = mysql.connector.connect(
         #   host="192.168.1.23",
         #   username="root",
         #   password="pi",
         #   db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        query = "SELECT rfid_tag, name, date, time, action, bor_returnName FROM rfid_data ORDER BY date, time DESC"
        #cursor = db.cursor()
        cursorlite.execute(query)
        result = cursorlite.fetchall()
        self.transactTable.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.transactTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.transactTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                #self.transactTable.sortItems(0, Qt.AscendingOrder)
        #cursorlite.close()
        

    def searchDataTransact(self):
        search = self.search.text().strip()
        if not search:
            self.loadDataTransact()
            
            
        else:
            #con = sqlite3.connect('rfid.db')
            #cursor = con.cursor()
            
            #con = mysql.connector.connect(
            #host="192.168.1.23",
            #username="root",
            #password="pi",
            #db="rfid-2" )
        
            #cursor = con.cursor(buffered=True)
        #try:
            query = f"SELECT rfid_tag, name, date, time, action, bor_returnName FROM rfid_data WHERE rfid_tag LIKE '%{search}%' OR name LIKE '%{search}%' OR date LIKE '%{search}%' OR time LIKE '%{search}%' OR action LIKE '%{search}%' OR bor_returnName LIKE '%{search}%'"
            #value = (search, search, search,)
            #cursor = db.cursor()
            #cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            #cursor.close()
            self.updateDataSearchTransact(data)

    def updateDataSearchTransact(self, data):
        #con = sqlite3.connect('rfid.db')
        #cursor = con.cursor()
        
       # con = mysql.connector.connect(
          #  host="192.168.1.23",
          #  username="root",
          #  password="pi",
          #  db="rfid-2" )
        
        #cursor = con.cursor(buffered=True)
        
        self.transactTable.setRowCount(len(data))
        for row_number, row_data in enumerate(data):
            #self.tableWidget.insertRow(row_number)
            for column_number, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.transactTable.setItem(row_number, column_number, item)
                #self.transactTable.sortItems(column_number, Qt.AscendingOrder)
        #cursor.close()
        
    def gotoDashboard(self):
        #dashboard = MainDashboard()
        #widget.addWidget(dashboard)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(3)
        #global keep_scanning
        #keep_scanning = True
        #self.scan_rfid_status = True
        #self.rfid_thread = RFIDReaderThread()
        #self.rfid_thread.new_data.connect(self.update_label)
        #self.rfid_thread.start()

    def equipmentnav(self):
        equipment = Equipment()
        widget.addWidget(equipment)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(4)

    def borrowernav(self):
        borrower = Borrower()
        widget.addWidget(borrower)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(5)

    def logoutnav(self):
        QMessageBox.information(self, "Data", "You have been successfully logout.")
        logout = LoginScreen()
        widget.addWidget(logout)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

    def myprofilenav(self):
        myprofile = MyProfile()
        widget.addWidget(myprofile)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(7)

class MyProfile(QMainWindow):
    def __init__(self):
        super(MyProfile, self).__init__()
        loadUi("MyProfile.ui", self)
        self.home_5.clicked.connect(self.gotoDashboard)
        self.borrower_5.clicked.connect(self.borrowernav)
        self.equip_5.clicked.connect(self.equipmentnav)
        self.logout_5.clicked.connect(self.logoutnav)
        self.myprofile_5.clicked.connect(self.myprofilenav)
        self.transactlist_5.clicked.connect(self.transactnav)
        global scan_rfid_status
        self.scan_rfid_status = False

    def gotoDashboard(self):
        #dashboard = MainDashboard()
        #widget.addWidget(dashboard)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(3)
       
      
       

    def equipmentnav(self):
        equipment = Equipment()
        widget.addWidget(equipment)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(4)

    def borrowernav(self):
        borrower = Borrower()
        widget.addWidget(borrower)
        widget.setFixedHeight(607)
        widget.setFixedWidth(1293)
        widget.setCurrentIndex(5)

    def transactnav(self):
        transact = TransactionList()
        widget.addWidget(transact)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(6)

    def logoutnav(self):
        QMessageBox.information(self, "Data", "You have been successfully logout.")
        logout = LoginScreen()
        widget.addWidget(logout)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(1)

    def myprofilenav(self):
        myprofile = MyProfile()
        widget.addWidget(myprofile)
        widget.setFixedHeight(601)
        widget.setFixedWidth(1013)
        widget.setCurrentIndex(7)



        
# main
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    signinpage = LoginScreen()
    signuppage = SignupScreen()
    dashboard = MainDashboard()
    equipment = Equipment()
    borrower = Borrower()
    transact = TransactionList()
    #myprof = MyProfile()
    # add = AddDevice()
    # edit = EditDevice()
    # dele = DeleteDevice()
    widget = QtWidgets.QStackedWidget()
    widget.setCurrentIndex(0)
    widget.addWidget(mainwindow)
    widget.addWidget(signinpage)
    widget.addWidget(signuppage)
    widget.addWidget(dashboard)
    widget.addWidget(equipment)
    widget.addWidget(borrower)
    widget.addWidget(transact)
    #widget.addWidget(myprof)
    # widget.addWidget(add)
    # widget.addWidget(edit)
    # widget.addWidget(dele)
    # widget.setFixedHeight(491)
    # widget.setFixedWidth(761)
    widget.setFixedHeight(601)
    widget.setFixedWidth(1013)
    widget.show()
    sys.exit(app.exec_())
#keep_scanning = True

#def stop_scanning():
       # global keep_scanning
       # keep_scanning = False

    
#try:
  #  sys.exit(app.exec_())
#except:
  #  print("Exiting")
