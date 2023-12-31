from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from login import *
from ship_grid import *
from ai import *
from transferSteps import *
from add_containers import *
from balanceSteps import *
from grid_balance import *
from aStar_balance import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from datetime import datetime
import re
import os
import pathlib

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        #default main window settings
        super(Ui_MainWindow,self).__init__()
        self.setObjectName("MainWindow")
        self.resize(803, 600)
        self.setWindowTitle("MainWindow")
        self.move(QtWidgets.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setupUi()
        # if self.load_state() == False:
        #     self.setupUi()
        

    def load_state(self):
        working_dir = str(pathlib.Path().resolve())
        if os.stat(working_dir + "\save_state.txt").st_size == 0:
            return False
        else:
            f = open(working_dir + "\save_state.txt", "r")
            # Names
            line = f.readline()
            names = line.split()
            # Weights
            line = f.readline()
            weights_str = line.split()
            weights = list(map(int, weights_str))
            # Coords
            line = f.readline()
            coords = line.split()
            # Filename
            line = f.readline()
            fileName = line.split("\n")[0]
            # Containers Add
            line = f.readline()
            containersAdd = line.split()
            # Containers Remove
            line = f.readline()
            containersRemove = line.split()
            f.close()

            self.add_containers = addContainers_Ui_Form(self)
            self.add_containers.container_names = names
            self.add_containers.weights = weights
            self.add_containers.coords = coords
            self.add_containers.fileName = fileName
            self.add_containers.containers_add = containersAdd
            self.add_containers.containers_remove = containersRemove
            self.add_containers.coord_solution_steps = driver(self.add_containers.fileName, self.add_containers.containers_remove, self.add_containers.containers_add)
            self.add_containers.coord_solution_steps.pop(0)
            self.add_containers.populatetransferSteps()

    def setupUi(self):

        #Adding Widget functionality
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        #Adding the uploadManifest button
        self.pushButton_uploadManifest = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_uploadManifest.setGeometry(QtCore.QRect(330, 380, 141, 61))
        self.pushButton_uploadManifest.setObjectName("pushButton_uploadManifest")
        self.pushButton_uploadManifest.setText("Upload Manifest")

        #Adding label for Long Beach Port
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 150, 801, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("Long Beach Port")

        #Adding label for CMS Software
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 230, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Container Moving Software (CMS)")
        self.setCentralWidget(self.centralwidget)

        #Adding menubar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 22))
        self.menubar.setObjectName("menubar")
        self.menuLogin = QtWidgets.QMenu(self.menubar)
        self.menuLogin.setObjectName("menuLogin")
        self.menuLogin.setTitle("Login")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuLogin.menuAction())
        self.LoginWindow = None # Set login window to none to show it has not been open yet
        self.shipGrid = None # Set ship grid window to none to show it has not been open yet
        self.balanceSteps = None
        self.container_names = []
        self.weights = []
        self.xCoords = []
        self.yCoords = []
        self.coords = []
        self.total_balance_cost = 0
        
        # AI Algo in add_containers.py needs fileName
        self.fileName = ""
        
        self.inital_ship_grid = None
        self.solution = None
        self.solution_trace = []
        self.solution_len = 0
        self.solution_count = 1
        self.coord_solution_steps = []

        # Make ship inventory grid 9x12 and initialize with all 0s
        self.inventory_array = [[0 for col in range(0,12)] for row in range(0,9)]
        # Make buffer inventory grid 4x24 and initialize with all 0s 
        self.buffer_inventory = [[0 for col in range(0,24)] for row in range(0,5)] 

        #Connecting buttons to functions
        self.pushButton_uploadManifest.clicked.connect(self.upload_manifest)
        self.menuLogin.aboutToShow.connect(self.show_login_window)

    def show_login_window(self):
        # If login window is not open, open it
        if self.LoginWindow is None:
            self.LoginWindow = Ui_Dialog_LoginPage(self)
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.LoginWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.LoginWindow.show()
        
    def upload_manifest(self):
        self.coords.clear()
        self.xCoords.clear()
        self.yCoords.clear()
        self.weights.clear()
        self.container_names.clear()
        # Open file dialog and get file name
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', filter="(*.txt)", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        # If no file is selected, return
        if name == '':
            return
        # Open file and read each line
        file = open(name, 'r')

        # AI Algo in AddContainers.py needs fileName
        self.fileName = name

        for line in file:
            # Remove trailed newline character and brackets/paraenthesis from each line
            line = re.sub(r"[\([{})\]]", "", line)
            line = line.rstrip('\n')
            # Save x,y coordinate from current line and save rest of line in extra variable
            x, extra = line.lstrip().split(',', 1)
            y, extra = extra.lstrip().split(',', 1)
            # Save weight current current line and save rest of line in extra variable
            weight, extra = extra.lstrip().split(',', 1)
            # Save container name current line
            cont_name = extra.lstrip().split(',', 1)
            cont_name = cont_name[0]


            # Append values from current line to list
            self.coords.append(f"{x},{y}")
            self.xCoords.append(x)
            self.yCoords.append(y)
            self.weights. append(weight)
            self.container_names.append(cont_name)

            # Map string values to integer values
            self.xCoords = list(map(int, self.xCoords))
            self.yCoords = list(map(int, self.yCoords))
            self.weights = list(map(int, self.weights))

        # Load 2d array with container objects and attributes
        index = 0
        for row in range(0,9):
            for col in range(0,12):
                if row == 8:
                    self.inventory_array[row][col] = Container("UNUSED", col+1, row+1, 0)
                else:
                    self.inventory_array[row][col] = Container(self.container_names[index], self.yCoords[index], self.xCoords[index], self.weights[index])
                index = index + 1

        # Load initial buffer with empty container objects
        for row in range(0,5):
            for col in range(0,24):
                self.buffer_inventory[row][col] = Container("UNUSED", col+1, row+1, 0)

        # Initial state of grid
        self.inital_ship_grid = Grid(self.inventory_array, self.buffer_inventory, removeRow=None, removeCol=None, parent=None, craneRow=8, craneCol=0, craneContainer=None)
        
        # Writes to lof file
        f = open('log.txt','a') #append
        timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")
        f.write("<" + timeStamp + "> User uploaded a manifest\n")
        f.close()

        # Show operation selection window
        self.showDialog()

    # QMessageBox that asks user if they want to add another container
    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Which operation would you like to perform?")
        msgBox.setWindowTitle("Choose Operation")
        balance_button = msgBox.addButton('Balance', QtWidgets.QMessageBox.NoRole)
        transfer_button = msgBox.addButton('Transfer', QtWidgets.QMessageBox.YesRole)

        returnValue = msgBox.exec()
        # If user would like to perform transfer operation
        if returnValue == 1:
            f = open('log.txt','a') #append
            timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")
            f.write("<" + timeStamp + "> Transfer operation in progress...\n")
            f.close()
            self.populateShipGrid()
            msgBox.close()
        # If user would like to perform balance operation
        else:
            # Writes to log file
            f = open('log.txt','a') #append
            timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")
            f.write("<" + timeStamp + "> Balancing operation in progress...\n")
            f.close()
            self.solution = a_star(self.inital_ship_grid)
            self.coord_solution_steps.clear()
            msgBox.close()
            if self.solution == None:
                #print(self.solution)
                pass
            if self.solution:

                while self.solution:
                    self.solution_trace.append(self.solution)
                    if self.solution.coordinate_tracking[0] != None:
                        self.solution.coordinate_tracking.append(self.solution.manhattan_distance)
                        self.coord_solution_steps.append(self.solution.coordinate_tracking)
                    self.solution = self.solution.parent
                    self.solution_len += 1

                # Open window and display steps to balance ship
                self.populateBalanceSteps()

            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("No solution found. Ship cannot be balanced!")
                msgBox.setWindowTitle("No Solution")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

    def populateBalanceSteps(self):
        containerNames = self.container_names
        self.total_balance_cost = 0
        #if self.balanceSteps is None:
        self.balanceSteps = Ui_Form_BalanceSteps(self)

        if len(self.coord_solution_steps) == 1:
            self.balanceSteps.pushButton_next.hide()
            self.balanceSteps.pushButton_removeDone.show()

        # Pass all manifest info to next window (balanceSteps)
        self.balanceSteps.container_names = self.container_names
        self.balanceSteps.weights = self.weights
        self.balanceSteps.coords = self.coords
        self.balanceSteps.fileName = self.fileName

        # Set color of ship grid cells based on NAN, Unused, or Used
        i = 0
        for row in range (8,0,-1):
            for column in range (12):
                if containerNames[i] == "NAN":
                    # Set nan cells to black color
                    self.balanceSteps.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.balanceSteps.tableWidget.item(row, column).setBackground(QtGui.QColor(0,0,0))
                    # Set nan cells to unclickable
                    self.balanceSteps.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                elif containerNames[i] == "UNUSED":
                    # Set unused cells to gray color
                    self.balanceSteps.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.balanceSteps.tableWidget.item(row, column).setBackground(QtGui.QColor(169,169,169))
                    # Set unused cells to unclickable
                    self.balanceSteps.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                else:
                    # Set used cells to blue color
                    self.balanceSteps.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.balanceSteps.tableWidget.item(row, column).setBackground(QtGui.QColor(0,0,255))
                    self.balanceSteps.tableWidget.item(row, column).setText(containerNames[i])
                    self.balanceSteps.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                i=i+1
        # Set all buffer cells to unused
        i = 0
        for row in range (4,0,-1):
            for column in range (24):
                # Set unused cells to gray color
                self.balanceSteps.tableWidget_Buffer.setItem(row,column,QtWidgets.QTableWidgetItem())
                self.balanceSteps.tableWidget_Buffer.item(row, column).setBackground(QtGui.QColor(169,169,169))
                # Set unused cells to unclickable
                self.balanceSteps.tableWidget_Buffer.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                i=i+1

        # Set intial coords to green
        self.balanceSteps.tableWidget.item(8-self.coord_solution_steps[0][0][0], self.coord_solution_steps[0][0][1]).setBackground(QtGui.QColor(0,255,0))
        # Set intial coords to red
        self.balanceSteps.tableWidget.item(8-self.coord_solution_steps[0][2][0], self.coord_solution_steps[0][2][1]).setBackground(QtGui.QColor(255,0,0))
        # Set intial coords to red
        self.total_balance_cost = self.total_balance_cost + self.coord_solution_steps[0][4]

        self.balanceSteps.balanceSteps = self.coord_solution_steps
        self.balanceSteps.total_balance_cost = self.total_balance_cost

        self.balanceSteps.setWindowModality(QtCore.Qt.ApplicationModal)
        self.balanceSteps.tableWidget.clearSelection()
        self.balanceSteps.show()

    def populateShipGrid(self):
        containerNames = self.container_names
        self.shipGrid = Ui_Form(self)
        # Pass all manifest info to next window (ShipGrid)
        self.shipGrid.container_names = self.container_names
        self.shipGrid.weights = self.weights
        self.shipGrid.coords = self.coords
        self.shipGrid.inventory_array = self.inventory_array
        self.shipGrid.fileName = self.fileName

        # Set color of ship grid cells based on NAN, Unused, or Used
        i = 0
        for row in reversed(range (8)):
            for column in range (12):
                if containerNames[i] == "NAN":
                    # Set nan cells to black color
                    self.shipGrid.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.shipGrid.tableWidget.item(row, column).setBackground(QtGui.QColor(0,0,0))
                    # Set nan cells to unclickable
                    self.shipGrid.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                elif containerNames[i] == "UNUSED":
                    # Set unused cells to gray color
                    self.shipGrid.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.shipGrid.tableWidget.item(row, column).setBackground(QtGui.QColor(169,169,169))
                    # Set unused cells to unclickable
                    self.shipGrid.tableWidget.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)
                else:
                    # Set used cells to blue color
                    self.shipGrid.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem())
                    self.shipGrid.tableWidget.item(row, column).setBackground(QtGui.QColor(0,0,255))
                    self.shipGrid.tableWidget.item(row, column).setText(containerNames[i])
                i=i+1
        self.shipGrid.setWindowModality(QtCore.Qt.ApplicationModal)
        self.shipGrid.tableWidget.clearSelection()
        self.shipGrid.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())