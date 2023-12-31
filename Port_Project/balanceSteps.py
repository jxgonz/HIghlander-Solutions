from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from login import *
from add_logComment import *
from add_containers import *
from pathlib import Path

class Ui_Form_BalanceSteps(QWidget, object):
    def __init__(self, parent, *args, **kwargs):
        #default grid settings
        super(Ui_Form_BalanceSteps,self).__init__()
        self.parent = object
        self.setObjectName("Balance Steps")
        self.resize(1800, 600)
        self.setAutoFillBackground(False)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setupUi(self)

    def setupUi(self, Form):
        #Adding Widget functionality for ship
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(1200, 122, 590, 362))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(9)
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

        #Adding Widget functionality for buffer
        self.tableWidget_Buffer = QtWidgets.QTableWidget(Form)
        self.tableWidget_Buffer.setGeometry(QtCore.QRect(10, 280, 1178, 202))
        self.tableWidget_Buffer.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_Buffer.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_Buffer.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget_Buffer.setCornerButtonEnabled(True)
        self.tableWidget_Buffer.setRowCount(5)
        self.tableWidget_Buffer.setColumnCount(24)
        self.tableWidget_Buffer.setObjectName("tableWidget_Buffer")
        self.tableWidget_Buffer.horizontalHeader().setVisible(False)
        self.tableWidget_Buffer.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget_Buffer.horizontalHeader().setHighlightSections(True)
        self.tableWidget_Buffer.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget_Buffer.verticalHeader().setVisible(False)
        self.tableWidget_Buffer.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget_Buffer.verticalHeader().setMinimumSectionSize(40)
        self.tableWidget_Buffer.verticalHeader().setStretchLastSection(False)
        self.LoginWindow = None
        self.addContainerWindow = None
        self.container_names = []
        self.weights = []
        self.coords = []
        self.balanceCounter = 0
        self.balanceSteps = []
        self.total_balance_cost = 0
        self.commentWindow = None
        self.container_weight = 0

        #Adding label for Ship
        self.label_ship = QtWidgets.QLabel(self)
        self.label_ship.setGeometry(QtCore.QRect(1200, 320, 590, 362))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_ship.setFont(font)
        self.label_ship.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ship.setObjectName("label_ship")
        self.label_ship.setText("Ship")

        #Adding label for Buffer
        self.label_buffer = QtWidgets.QLabel(self)
        self.label_buffer.setGeometry(QtCore.QRect(10, 400, 1180, 202))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_buffer.setFont(font)
        self.label_buffer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_buffer.setObjectName("label_buffer")
        self.label_buffer.setText("Buffer")
        
        # AI Algo needs fileName
        self.fileName = ""

        #Adding label for Ship Grid
        self.label_shipInventory = QtWidgets.QLabel(self)
        self.label_shipInventory.setGeometry(QtCore.QRect(0, 40, 1800, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_shipInventory.setFont(font)
        self.label_shipInventory.setAlignment(QtCore.Qt.AlignCenter)
        self.label_shipInventory.setObjectName("label_shipInventory")
        self.label_shipInventory.setText("Balancing Steps")

        #Adding label for Ship Grid
        self.label_shipGrid = QtWidgets.QLabel(self)
        self.label_shipGrid.setGeometry(QtCore.QRect(0, 80, 1800, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_shipGrid.setFont(font)
        self.label_shipGrid.setAlignment(QtCore.Qt.AlignCenter)
        self.label_shipGrid.setObjectName("label_shipGrid")
        self.label_shipGrid.setText("Please move the green container to the red area. Click the button once complete.")

        # Adding the done button for when user is finished selecting containers to be removed
        self.pushButton_addComment = QtWidgets.QPushButton(self)
        self.pushButton_addComment.setGeometry(QtCore.QRect(10, 30, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_addComment.setFont(font)
        self.pushButton_addComment.setObjectName("pushButton_addComment")
        self.pushButton_addComment.setText("Add comment")

        # Adding the done button for when user is finished selecting containers to be removed
        self.pushButton_next = QtWidgets.QPushButton(self)
        self.pushButton_next.setGeometry(QtCore.QRect(830, 530, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_next.setFont(font)
        self.pushButton_next.setObjectName("pushButton_next")
        self.pushButton_next.setText("Next")

        # Adding the done button for when user is finished selecting containers to be removed
        self.pushButton_removeDone = QtWidgets.QPushButton(self)
        self.pushButton_removeDone.setGeometry(QtCore.QRect(830, 530, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_removeDone.setFont(font)
        self.pushButton_removeDone.setObjectName("pushButton_removeDone")
        self.pushButton_removeDone.setText("Done")
        self.pushButton_removeDone.hide()

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
        self.pushButton_next.clicked.connect(self.next_step)
        self.pushButton_removeDone.clicked.connect(self.remove_done)
        self.pushButton_addComment.clicked.connect(self.addComment_clicked)
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
            # print(coord)
            strIndex = self.coords.index(coord)
            containerStr = self.container_names[strIndex]
            containerStrs.append(containerStr)
        # print(containerStrs)
        return containerStrs

    def addComment_clicked(self):
        # If login window is not open, open it
        if self.commentWindow is None:
            self.commentWindow = Ui_Dialog_AddComment(self)
        # Set login window to application modal so that it must be closed before main window can be used
        # This solves the issue of when you open the login window a second time it will be behind the main window
        self.commentWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.commentWindow.show()

    def next_step(self):
        # Set old coords to grey
        self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).setBackground(QtGui.QColor(169,169,169))
        container_name = self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).text()
        # Set new container coords to blue
        self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][2][0], self.balanceSteps[self.balanceCounter][2][1]).setBackground(QtGui.QColor(0,0,255))
        self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][2][0], self.balanceSteps[self.balanceCounter][2][1]).setText(container_name)
        self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).setText("")

        # Update container names and weights arrays with new container location
        i = 0
        for row in range (8,0,-1):
            for col in range (12):
                if row == (8-self.balanceSteps[self.balanceCounter][0][0]) and col == (self.balanceSteps[self.balanceCounter][0][1]):
                    self.container_names[i] = "UNUSED"
                    self.container_weight = self.weights[i]
                    self.weights[i] = 0
                i=i+1
        
        i = 0
        for row in range (8,0,-1):
            for col in range (12):
                if row == (8-self.balanceSteps[self.balanceCounter][2][0]) and col == (self.balanceSteps[self.balanceCounter][2][1]):
                            self.container_names[i] = container_name
                            self.weights[i] = self.container_weight
                i=i+1

        # Writes to log file
        f = open('log.txt','a') #append
        timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")
        f.write("<" + timeStamp + "> Container "+container_name+" was moved from ["+str(self.balanceSteps[self.balanceCounter][0][0]+1)+", "+str(self.balanceSteps[self.balanceCounter][0][1]+1)+"] to ["+str(self.balanceSteps[self.balanceCounter][2][0]+1)+", "+str(self.balanceSteps[self.balanceCounter][2][1]+1)+"]\n")
        f.close()

        self.balanceCounter = self.balanceCounter + 1
        if self.balanceCounter >= len(self.balanceSteps):
            self.pushButton_next.hide()
            self.pushButton_removeDone.show()
        else:
            # Set intial coords to green
            self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).setBackground(QtGui.QColor(0,255,0))
            # Set new coords to red
            self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][2][0], self.balanceSteps[self.balanceCounter][2][1]).setBackground(QtGui.QColor(255,0,0))
            # Add to total cost
            self.total_balance_cost = self.total_balance_cost + self.balanceSteps[self.balanceCounter][4]

    def remove_done(self):
        
        if len(self.balanceSteps) == 1:
            # Set old coords to grey
            self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).setBackground(QtGui.QColor(169,169,169))
            container_name = self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).text()
            # Set new container coords to blue
            self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][2][0], self.balanceSteps[self.balanceCounter][2][1]).setBackground(QtGui.QColor(0,0,255))
            self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][2][0], self.balanceSteps[self.balanceCounter][2][1]).setText(container_name)
            self.tableWidget.item(8-self.balanceSteps[self.balanceCounter][0][0], self.balanceSteps[self.balanceCounter][0][1]).setText("")
            # Writes to log file
            f = open('log.txt','a') #append
            timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")
            f.write("<" + timeStamp + "> Container "+container_name+" was moved from ["+str(self.balanceSteps[self.balanceCounter][0][0]+1)+", "+str(self.balanceSteps[self.balanceCounter][0][1]+1)+"] to ["+str(self.balanceSteps[self.balanceCounter][2][0]+1)+", "+str(self.balanceSteps[self.balanceCounter][2][1]+1)+"]\n")
            f.close()

            # Update container names and weights arrays with new container location
            i = 0
            for row in range (8,0,-1):
                for col in range (12):
                    if row == (8-self.balanceSteps[self.balanceCounter][0][0]) and col == (self.balanceSteps[self.balanceCounter][0][1]):
                        self.container_names[i] = "UNUSED"
                        self.container_weight = self.weights[i]
                        self.weights[i] = 0
                    i=i+1
            
            i = 0
            for row in range (8,0,-1):
                for col in range (12):
                    if row == (8-self.balanceSteps[self.balanceCounter][2][0]) and col == (self.balanceSteps[self.balanceCounter][2][1]):
                                self.container_names[i] = container_name
                                self.weights[i] = self.container_weight
                    i=i+1

        # If add container window is not open, open it
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        # Writes to log file
        f = open('log.txt','a') #append
        timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")
        f.write("<" + timeStamp + "> Balancing Complete!\n")
        f.close()

        msgBox.setText(f"Balancing Complete! \nThe total number of operations was {len(self.balanceSteps)}.\n The total time taken was {self.total_balance_cost} minutes.\n\n Updated manifest in downloads folder.\n Please send to ship captain!")
        msgBox.setWindowTitle("Balancing Complete")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.printNewManifest()
        self.close()

    def printNewManifest(self):
        # Writes to new manifest
        downloads_path = str(Path.home() / "Downloads")
        f = open(downloads_path+'/manifest.txt','w') #write
        for i in range(0,len(self.container_names)):
            f.write(f"["+str(self.coords[i])+"], {"+str(self.weights[i]).zfill(5)+"}, "+str(self.container_names[i])+"\n")
        f.close()

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
        