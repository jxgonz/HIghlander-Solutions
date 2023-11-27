# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from login import *
from ship_grid import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from datetime import datetime
import re

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        #default main window settings
        super(Ui_MainWindow,self).__init__()
        self.setObjectName("MainWindow")
        self.resize(803, 600)
        self.setWindowTitle("MainWindow")
        self.setupUi()


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

        #Connecting buttons to functions
        self.pushButton_uploadManifest.clicked.connect(self.upload_manifest)
        self.menuLogin.aboutToShow.connect(self.show_login_window)

    def upload_manifest(self):
        # Open file dialog and get file name
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        # If no file is selected, return
        if name == '':
            return
        # Open file and read each line
        file = open(name, 'r')
        coords, weights, container_names = [], [], []

        for line in file:
            # Remove trailed newline character and brackets/paraenthesis from each line
            line = re.sub(r"[\([{})\]]", "", line)
            line = line.rstrip('\n')
            # Save x coordinate from current line and save rest of line in extra variable
            coord, extra = line.lstrip().split(' ', 1)
            # Remove trailing comma from coordinates
            coord = coord[:-1] 
            # Save weight current current line and save rest of line in extra variable
            weight, extra = extra.lstrip().split(',', 1)
            # Save container name current line
            cont_name = extra.lstrip().split(',', 1)
            cont_name = cont_name[0]

            # Append values from current line to list
            coords.append(coord)
            weights. append(weight)
            container_names.append(cont_name)

        self.populateShipGrid(container_names)
        #self.close()

    def show_login_window(self):
        # If login window is not open, open it
        if self.LoginWindow is None:
            self.LoginWindow = Ui_Dialog_LoginPage(self)
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.LoginWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.LoginWindow.show()

    def populateShipGrid(self, containerNames = []):
        if self.shipGrid is None:
            self.shipGrid = Ui_Form(self)
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
