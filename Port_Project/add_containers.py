from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from login import *


class addContainers_Ui_Form(QWidget, object):
    def __init__(self, parent, *args, **kwargs):
        #default grid settings
        super(addContainers_Ui_Form,self).__init__()
        self.parent = object
        self.setObjectName("Add Containers")
        self.resize(803, 600)
        self.setAutoFillBackground(False)
        self.setupUi(self)

    def setupUi(self, Form):
 
        self.LoginWindow = None

        #Adding label for Ship Grid
        self.label_loadContainers = QtWidgets.QLabel(self)
        self.label_loadContainers.setGeometry(QtCore.QRect(0, 80, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_loadContainers.setFont(font)
        self.label_loadContainers.setAlignment(QtCore.Qt.AlignCenter)
        self.label_loadContainers.setObjectName("label_loadContainers")
        self.label_loadContainers.setText("Load Containers Onto Ship")

        #Adding label for Ship Grid
        self.label_containerName = QtWidgets.QLabel(self)
        self.label_containerName.setGeometry(QtCore.QRect(0, 240, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_containerName.setFont(font)
        self.label_containerName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_containerName.setObjectName("label_shipGrid")
        self.label_containerName.setText("Please enter the name of the crate you would like to add:")

        #Line edit name
        self.lineEdit_addContainers = QtWidgets.QLineEdit(self)
        self.lineEdit_addContainers.setGeometry(QtCore.QRect(175, 285, 451, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_addContainers.setFont(font)
        self.lineEdit_addContainers.setClearButtonEnabled(False)
        self.lineEdit_addContainers.setObjectName("lineEdit_addContainers")
        self.lineEdit_addContainers.setFocus()

        # Adding the done button for when user is finished selecting containers to be removed
        self.pushButton_removeDone = QtWidgets.QPushButton(self)
        self.pushButton_removeDone.setGeometry(QtCore.QRect(330, 485, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_removeDone.setFont(font)
        self.pushButton_removeDone.setObjectName("pushButton_removeDone")
        self.pushButton_removeDone.setText("Done")

        # List that holds containers selected to be added to ship
        self.containers_add = []

        #Adding Tool bar for back button 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.menuBar = QMenuBar()
        self.fileMenu = QMenu("Back")
        self.loginWindow = QMenu("Login")

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addAction(self.fileMenu.menuAction())
        self.layout.setMenuBar(self.menuBar)

        self.menuBar.addMenu(self.loginWindow)
        self.menuBar.addAction(self.loginWindow.menuAction())
        self.layout.setMenuBar(self.menuBar)
        
        #Connecting buttons to functions
        self.pushButton_removeDone.clicked.connect(self.remove_done)
        self.fileMenu.aboutToShow.connect(self.show_shipGrid_window)
        self.loginWindow.aboutToShow.connect(self.show_login_window)

    def remove_done(self):
        self.containers_add.append(self.lineEdit_addContainers.text())
        print(self.containers_add)
        self.showDialog()
        #run algorithm here and then open window to display stepwise solution

    def show_login_window(self):
        # If login window is not open, open it
        if self.LoginWindow is None:
            self.LoginWindow = Ui_Dialog_LoginPage(self)
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.LoginWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.LoginWindow.show()
    
    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Would you like to add another container?")
        msgBox.setWindowTitle("Add Containers Onto Ship")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
            self.lineEdit_addContainers.clear()
            msgBox.close()
        else:
            msgBox.close()
            print("Adding Containers Complete. Need to open step wise solution window here.")

    def show_shipGrid_window(self):
        self.close()