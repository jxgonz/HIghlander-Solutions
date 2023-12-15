from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QSpinBox
from datetime import datetime

class Ui_Dialog_InputWeight(QDialog, object):
    def __init__(self, parent, *args, **kwargs):
        super(Ui_Dialog_InputWeight,self).__init__()
        self.parent = object
        self.setObjectName("Dialog_InputWeight")
        self.resize(487, 320)
        self.setWindowTitle("Dialog_InputWeight")

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
        self.label.setText("Crane Operator")

        #Label 2
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Please pick up truck container and enter its weight:")

      # creating spin box 
        self.spin = QSpinBox(self)
        font = QtGui.QFont()
        font.setPointSize(12) 
        self.spin.setFont(font)
        # setting geometry to spin box 
        self.spin.setGeometry(150, 150, 150, 40) 
        self.spin.setMaximum(99999)
        self.spin.setMinimum(0)
        self.spin.setValue(0)

        #confirm push button
        self.pushButton_confirmWeight = QtWidgets.QPushButton(self)
        self.pushButton_confirmWeight.setGeometry(QtCore.QRect(100, 230, 111, 41))
        self.pushButton_confirmWeight.setObjectName("pushButton_confirmWeight")
        self.pushButton_confirmWeight.clicked.connect(self.done_clicked)
        self.pushButton_confirmWeight.setText("Done")
        
        #cancel push button
        self.pushButton_cancelLogin = QtWidgets.QPushButton(self)
        self.pushButton_cancelLogin.setGeometry(QtCore.QRect(280, 230, 111, 41))
        self.pushButton_cancelLogin.setObjectName("pushButton_cancelLogin")
        self.pushButton_cancelLogin.clicked.connect(self.cancel_login)
        self.pushButton_cancelLogin.setText("Cancel")
        self.weight = 0

    def done_clicked(self):

            #Saves the name of the user on the line edit
            self.weight = self.spin.value()

            #Creates the time stamp for when the use signs in
            # mm/dd/YY H:M
            timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")

            #Opens the log.txt file and appends the username to it and closes it
            f = open('log.txt','a') #append
            f.write("<" + timeStamp + "> User entered weight for loading container as: [" + str(self.weight) + "]\n")
            f.close()

            #Clears the line edit and closes the window
            self.hide()

    def cancel_login(self):
        #Clears the line edit and closes the window
        self.spin.setValue(0)
        self.hide()