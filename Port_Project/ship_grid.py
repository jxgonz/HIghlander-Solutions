from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from login import *
from add_containers import *


class Ui_Form(QWidget, object):
    def __init__(self, parent, *args, **kwargs):
        #default grid settings
        super(Ui_Form,self).__init__()
        self.parent = object
        self.setObjectName("Remove Containers")
        self.resize(803, 600)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center()- self.rect().center())
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
        self.LoginWindow = None
        self.addContainerWindow = None
        self.container_names = []
        self.weights = []
        self.coords = []
        self.inventory_array = []

        # AI Algo needs fileName
        self.fileName = ""

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
        self.loginWindow = QMenu("Login")

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addAction(self.fileMenu.menuAction())
        self.layout.setMenuBar(self.menuBar)

        self.menuBar.addMenu(self.loginWindow)
        self.menuBar.addAction(self.loginWindow.menuAction())
        self.layout.setMenuBar(self.menuBar)
        
        #Connecting buttons to functions
        self.pushButton_removeDone.clicked.connect(self.remove_done)
        self.fileMenu.aboutToShow.connect(self.show_main_window)
        self.loginWindow.aboutToShow.connect(self.show_login_window)
        
    # Converts coordinates of container to their strings. This is needed for
    # converting the AI Algo
    def coordsToStrings(self, containerCoords):
        containerStrs = []
        for coord in containerCoords:
            # Reverse lookup the index of the coordinate since
            # these arrays are parallel. That way we can just call
            # the container name from that coordinates index!
            #print(coord)
            strIndex = self.coords.index(coord)
            containerStr = self.container_names[strIndex]
            containerStrs.append(containerStr)
        #print(containerStrs)
        return containerStrs

    def remove_done(self):
        # If add container window is not open, open it
        if self.addContainerWindow is None:
            self.addContainerWindow = addContainers_Ui_Form(self)
            # Pass all manifest info and containers to remove to addContainers window
            self.addContainerWindow.container_names = self.container_names
            self.addContainerWindow.weights = self.weights
            self.addContainerWindow.coords = self.coords
            self.addContainerWindow.inventory_array = self.inventory_array

            # AI Algo needs strings of containers to remove, not the coordinates
            # Here, i'll convert the list of container coords to their names
            self.containers_remove = self.coordsToStrings(self.containers_remove)
            self.addContainerWindow.containers_remove = self.containers_remove

            self.addContainerWindow.fileName = self.fileName
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.addContainerWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.close()
        self.addContainerWindow.show()

    def show_login_window(self):
        # If login window is not open, open it
        if self.LoginWindow is None:
            self.LoginWindow = Ui_Dialog_LoginPage(self)
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.LoginWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.LoginWindow.show()

    def show_main_window(self):
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
        #print(self.containers_remove)
