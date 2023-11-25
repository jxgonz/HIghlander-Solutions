# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ship_grid.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from mainwindow import *


class Ui_Form(QWidget):
    def __init__(self):
        #default grid settings
        super(Ui_Form,self).__init__()
        self.setObjectName("Remove Containers")
        self.resize(803, 600)
        self.setAutoFillBackground(False)
        self.setupUi(self)

    def setupUi(self, Form):
        #Adding Widget functionality
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(110, 130, 590, 325))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.verticalHeader().setMinimumSectionSize(40)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        #Adding label for Ship Grid
        self.label_shipInventory = QtWidgets.QLabel(self)
        self.label_shipInventory.setGeometry(QtCore.QRect(0, 40, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_shipInventory.setFont(font)
        self.label_shipInventory.setAlignment(QtCore.Qt.AlignCenter)
        self.label_shipInventory.setObjectName("label_shipInventory")
        self.label_shipInventory.setText("Ship Inventory")

        #Adding label for Ship Grid
        self.label_shipGrid = QtWidgets.QLabel(self)
        self.label_shipGrid.setGeometry(QtCore.QRect(0, 80, 801, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_shipGrid.setFont(font)
        self.label_shipGrid.setAlignment(QtCore.Qt.AlignCenter)
        self.label_shipGrid.setObjectName("label_shipGrid")
        self.label_shipGrid.setText("Please Select Any Blue Container To Remove From Ship")

        # Adding the done button for when user is finished selecting containers to be removed
        self.pushButton_removeDone = QtWidgets.QPushButton(self)
        self.pushButton_removeDone.setGeometry(QtCore.QRect(330, 485, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_removeDone.setFont(font)
        self.pushButton_removeDone.setObjectName("pushButton_removeDone")
        self.pushButton_removeDone.setText("Done")

        # List that holds containers selected to be removed from ship
        self.containers_remove = []
        # Checks if selection was changed on ship grid
        self.tableWidget.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        # Set highlighted color on ship grid to red when a container is selected to be removed
        self.tableWidget.setStyleSheet("QTableWidget::item:selected{ background-color: %s }" % QtGui.QColor(255,0,0).name())

        #Adding Tool bar for back button 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.menuBar = QMenuBar()
        self.fileMenu = QMenu("Back")

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addAction(self.fileMenu.menuAction())
        self.layout.setMenuBar(self.menuBar)
        
        #Connecting buttons to functions
        self.pushButton_removeDone.clicked.connect(self.remove_done)
        self.fileMenu.aboutToShow.connect(self.show_main_window)
        
    def remove_done(self):
        #show window to input crates to load onto ship
        #hide current window
        pass

    def show_main_window(self):
        self.main_window = Ui_MainWindow()
        self.main_window.show()
        self.close()

    def on_selectionChanged(self, selected, deselected):
        # If container is selected, format and append to list
        for i in selected.indexes():
            row = i.row()
            column = i.column()
            row = 8-row
            row = f"0{row}"
            column = column+1
            if column < 10:
                column = f"0{column}"
            container = f"{row},{column}"
            self.containers_remove.append(container)

        # If container is deselected, format and remove from list
        for i in deselected.indexes():
            row = i.row()
            column = i.column()
            row = 8-row
            row = f"0{row}"
            column = column+1
            if column < 10:
                column = f"0{column}"
            container = f"{row},{column}"
            self.containers_remove.remove(container)
        
        # Print all containers to be removed
        print(self.containers_remove)    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = Ui_Form()
    Form.show()
    sys.exit(app.exec_())
