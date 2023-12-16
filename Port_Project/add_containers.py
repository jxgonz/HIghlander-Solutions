from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from login import *
from ai import *
from transferSteps import *
from container import *
from ship_grid import *
from inputWeight import *


class addContainers_Ui_Form(QWidget, object):
    def __init__(self, parent, *args, **kwargs):
        #default grid settings
        super(addContainers_Ui_Form,self).__init__()
        self.parent = object
        self.setObjectName("Add Containers")
        self.resize(803, 600)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setAutoFillBackground(False)
        self.setupUi(self)

    def setupUi(self, Form):
 
        self.LoginWindow = None
        self.inputWeight = None
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
        font.setPointSize(13)
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
        #2d array of ship containers
        self.inventory_array = []
        self.coords = []
        self.weights = []
        self.container_names = []
        self.coord_solution_steps = []
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
        #call heuristic algorithm function here and then open window to display stepwise solution
        self.coord_solution_steps=driver(self.fileName, self.containers_remove, self.containers_add)
        self.coord_solution_steps.pop(0)
        print(self.coord_solution_steps)
        self.populatetransferSteps()

    def add_done(self):
        # If the user enters a container name and clicks "done"
        if self.lineEdit_addContainers.text():
            self.containers_add.append(self.lineEdit_addContainers.text())
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
            self.coord_solution_steps=driver(self.fileName, self.containers_remove, self.containers_add)
            self.coord_solution_steps.pop(0)
            print(self.coord_solution_steps)
            self.populatetransferSteps()

    def show_shipGrid_window(self):
        self.close()

    def populatetransferSteps(self):
        containerNames = self.container_names
        self.total_transfer_cost = 0
        #if self.transferSteps is None:
        self.transferSteps = Ui_Form_TransferSteps(self)

        # Pass all manifest info to next window (transferSteps)
        self.transferSteps.container_names = self.container_names
        self.transferSteps.weights = self.weights
        self.transferSteps.coords = self.coords
        self.transferSteps.fileName = self.fileName

        # Save State (Initial Sa)
        f = open("save_state.txt", "w")
        for name in self.container_names:
            f.write(name + " ")
        f.write("\n")
        for weight in self.weights:
            f.write(str(weight) + " ")
        f.write("\n")
        for coord in self.coords:
            f.write(coord + " ")
        f.write("\n")
        f.write(self.fileName)
        f.write("\n")
        for container in self.containers_add:
            f.write(container + " ")
        f.write("\n")
        for container in self.containers_remove:
            f.write(container + " ")
        f.write("\n")
        
        f.close()
        
        # Set color of ship grid cells based on NAN, Unused, or Used
        i = 0
        for row in range (8,0,-1):
            for column in range (12):
                if containerNames[i] == "NAN":
                    # Set nan cells to black color
                    self.transferSteps.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.transferSteps.tableWidget.item(row, column).setBackground(QtGui.QColor(0,0,0))
                    # Set nan cells to unclickable
                    self.transferSteps.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                elif containerNames[i] == "UNUSED":
                    # Set unused cells to gray color
                    self.transferSteps.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.transferSteps.tableWidget.item(row, column).setBackground(QtGui.QColor(169,169,169))
                    # Set unused cells to unclickable
                    self.transferSteps.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                else:
                    # Set used cells to blue color
                    self.transferSteps.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.transferSteps.tableWidget.item(row, column).setBackground(QtGui.QColor(0,0,255))
                    self.transferSteps.tableWidget.item(row, column).setText(containerNames[i])
                    self.transferSteps.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                i=i+1
        # Set all buffer cells to unused
        i = 0
        for row in range (4,0,-1):
            for column in range (24):
                # Set unused cells to gray color
                self.transferSteps.tableWidget_Buffer.setItem(row,column,QtWidgets.QTableWidgetItem())
                self.transferSteps.tableWidget_Buffer.item(row, column).setBackground(QtGui.QColor(169,169,169))
                # Set unused cells to unclickable
                self.transferSteps.tableWidget_Buffer.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                i=i+1
        # Set truck cell to unused
        self.transferSteps.tableWidget_truck.setItem(0,0,QtWidgets.QTableWidgetItem())
        self.transferSteps.tableWidget_truck.item(0, 0).setBackground(QtGui.QColor(169,169,169))
        # Set unused cells to unclickable
        self.transferSteps.tableWidget_truck.item(0, 0).setFlags(QtCore.Qt.ItemIsEnabled)

        print(self.coord_solution_steps)

        if self.coord_solution_steps[0][1]=="truck":
            self.transferSteps.tableWidget_truck.item(0, 0).setText(self.containers_add[0])
            # Set intial coords to green
            self.transferSteps.tableWidget_truck.item(0, 0).setBackground(QtGui.QColor(0,255,0))
            # Set intial coords to red
            self.transferSteps.tableWidget.item(9-self.coord_solution_steps[0][2][0], self.coord_solution_steps[0][2][1]-1).setBackground(QtGui.QColor(255,0,0))
            # Set intial coords to red
            self.total_transfer_cost = self.total_transfer_cost + self.coord_solution_steps[0][4]
            if self.inputWeight == None:
                self.inputWeight = Ui_Dialog_InputWeight(self)
                # Set login window to application modal so that it must be closed before main window can be used
                # This solves the issue of when you open the login window a second time it will be behind the main window
                self.inputWeight.setWindowModality(QtCore.Qt.ApplicationModal)
                resp = self.inputWeight.exec_()
                # retrieve text from line edit in dialog and return it
                self.weight = self.inputWeight.spin.value()
                
        elif self.coord_solution_steps[0][3]=="truck":
            # Set intial coords to green
            self.transferSteps.tableWidget.item(9-self.coord_solution_steps[0][0][0], self.coord_solution_steps[0][0][1]-1).setBackground(QtGui.QColor(0,255,0))
            # Set intial coords to red
            self.transferSteps.tableWidget_truck.item(0, 0).setBackground(QtGui.QColor(255,0,0))
            # Set intial coords to red
            self.total_transfer_cost = self.total_transfer_cost + self.coord_solution_steps[0][4]
        else:
            # Set intial coords to green
            self.transferSteps.tableWidget.item(9-self.coord_solution_steps[0][0][0], self.coord_solution_steps[0][0][1]-1).setBackground(QtGui.QColor(0,255,0))
            # Set intial coords to red
            self.transferSteps.tableWidget.item(9-self.coord_solution_steps[0][2][0], self.coord_solution_steps[0][2][1]-1).setBackground(QtGui.QColor(255,0,0))
            # Set intial coords to red
            self.total_transfer_cost = self.total_transfer_cost + self.coord_solution_steps[0][4]

        self.transferSteps.transferSteps = self.coord_solution_steps
        self.transferSteps.weight = self.weight
        self.transferSteps.containers_add = self.containers_add
        self.transferSteps.total_transfer_cost = self.total_transfer_cost

        self.transferSteps.setWindowModality(QtCore.Qt.ApplicationModal)
        self.transferSteps.tableWidget.clearSelection()
        self.transferSteps.show()
        self.hide()