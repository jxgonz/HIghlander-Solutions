from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from datetime import datetime

class Ui_Dialog_LoginPage(QDialog, object):
    def __init__(self, parent, *args, **kwargs):
        super(Ui_Dialog_LoginPage,self).__init__()
        self.parent = object
        self.setObjectName("Dialog_LoginPage")
        self.resize(487, 320)
        self.setWindowTitle("Dialog_LoginPage")

        self.setupUi()

    def setupUi(self):
        #Adding Widget functionality
        self.secondarywidget = QtWidgets.QWidget()
        self.secondarywidget.setObjectName("secondarywidget")

        #Label 1
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 30, 491, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("Login Page")

        #Label 2
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Please enter your name:")

        #Line edit name
        self.lineEdit_name = QtWidgets.QLineEdit(self)
        self.lineEdit_name.setGeometry(QtCore.QRect(20, 150, 451, 31))
        self.lineEdit_name.setClearButtonEnabled(False)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setFocus()

        #confirm push button
        self.pushButton_confirmLogin = QtWidgets.QPushButton(self)
        self.pushButton_confirmLogin.setGeometry(QtCore.QRect(100, 230, 111, 41))
        self.pushButton_confirmLogin.setObjectName("pushButton_confirmLogin")
        self.pushButton_confirmLogin.clicked.connect(self.login_clicked)
        self.pushButton_confirmLogin.setText("Login")
        
        #cancel push button
        self.pushButton_cancelLogin = QtWidgets.QPushButton(self)
        self.pushButton_cancelLogin.setGeometry(QtCore.QRect(280, 230, 111, 41))
        self.pushButton_cancelLogin.setObjectName("pushButton_cancelLogin")
        self.pushButton_cancelLogin.clicked.connect(self.cancel_login)
        self.pushButton_cancelLogin.setText("Cancel")
        self.username = ""

    def login_clicked(self):
        # If the user enters a login name and clicks "login"
        if self.lineEdit_name.text():
            #Saves the name of the user on the line edit
            self.username = self.lineEdit_name.text()

            #Creates the time stamp for when the use signs in
            # mm/dd/YY H:M
            timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")

            #Opens the log.txt file and appends the username to it and closes it
            f = open('log.txt','a') #append
            f.write("<" + timeStamp + "> [" + self.username + "] Logged in\n")
            f.close()

            #Clears the line edit and closes the window
            self.lineEdit_name.clear()
            self.done(1)

        # If the user does not enter a login name and clicks "login"
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Please enter a name to login.")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def cancel_login(self):
        #Clears the line edit and closes the window
        self.lineEdit_name.clear()
        self.done(1)