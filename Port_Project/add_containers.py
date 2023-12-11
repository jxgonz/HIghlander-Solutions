from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from login import *
from ai import *


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
        self.label_containerName.setText("Please enter the name of the container you would like to add:")

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
        self.pushButton_addDone = QtWidgets.QPushButton(self)
        self.pushButton_addDone.setGeometry(QtCore.QRect(146, 485, 250, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_addDone.setFont(font)
        self.pushButton_addDone.setObjectName("pushButton_addDone")
        self.pushButton_addDone.setText("Add Container")

        # Adding the "No containers to add" button
        self.pushButton_noContainersToAdd = QtWidgets.QPushButton(self)
        self.pushButton_noContainersToAdd.setGeometry(QtCore.QRect(406, 485, 250, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_noContainersToAdd.setFont(font)
        self.pushButton_noContainersToAdd.setObjectName("pushButton_noContainersToAdd")
        self.pushButton_noContainersToAdd.setText("No Containers to Add")

        # List that holds containers selected to be added to ship
        self.containers_add = []
        # Note that here, containers_remove is now a list of strings!
        self.containers_remove = []
        self.container_names = []
        self.weights = []
        self.coords = []

        # AI Algo needs file to process 2D arrays
        self.fileName = ""

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
        self.pushButton_addDone.clicked.connect(self.add_done)
        self.pushButton_noContainersToAdd.clicked.connect(self.noContainersToLoad)
        self.fileMenu.aboutToShow.connect(self.show_shipGrid_window)
        self.loginWindow.aboutToShow.connect(self.show_login_window)

    def noContainersToLoad(self):
        # Call heuristic algorithm here and below in showDialog() function when the user is done adding containers
        return driver(self.fileName, self.containers_remove, self.containers_add)

    def add_done(self):
        # If the user enters a container name and clicks "done"
        if self.lineEdit_addContainers.text():
            self.containers_add.append(self.lineEdit_addContainers.text())
            print(self.containers_add)
            # Show dialog to ask if user would like to add another container
            self.showDialog()

        # If the user does not enter a container name and clicks "done"
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Please enter a container name.")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def show_login_window(self):
        # If login window is not open, open it
        if self.LoginWindow is None:
            self.LoginWindow = Ui_Dialog_LoginPage(self)
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.LoginWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.LoginWindow.show()
    
    # QMessageBox that asks user if they want to add another container
    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Would you like to add another container?")
        msgBox.setWindowTitle("Add Containers Onto Ship")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()
        # If user would like to add another container
        if returnValue == QMessageBox.Yes:
            self.lineEdit_addContainers.clear()
            msgBox.close()
        # If user is done adding containers
        else:
            msgBox.close()
            #call heuristic algorithm function here and then open window to display stepwise solution
            print("Adding Containers Complete. Need to open step wise solution window here.")
            return driver(self.fileName, self.containers_remove, self.containers_add)

    def show_shipGrid_window(self):
        self.close()