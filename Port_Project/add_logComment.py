from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from datetime import datetime

class Ui_Dialog_AddComment(QDialog, object):
    def __init__(self, parent, *args, **kwargs):
        super(Ui_Dialog_AddComment,self).__init__()
        self.parent = object
        self.setObjectName("Dialog_AddComment")
        self.resize(487, 320)
        self.setWindowTitle("Dialog_AddComment")

        self.setupUi()

    def setupUi(self):
        #Adding Widget functionality
        self.secondarywidget = QtWidgets.QWidget()
        self.secondarywidget.setObjectName("secondarywidget")

        #Label 1
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 30, 491, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("Add comment to log file")

        #Label 2
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Please enter your comment:")

        #Line edit name
        self.lineEdit_comment = QtWidgets.QLineEdit(self)
        self.lineEdit_comment.setGeometry(QtCore.QRect(20, 150, 451, 31))
        self.lineEdit_comment.setClearButtonEnabled(False)
        self.lineEdit_comment.setObjectName("lineEdit_comment")
        self.lineEdit_comment.setFocus()

        #confirm push button
        self.pushButton_confirmComment = QtWidgets.QPushButton(self)
        self.pushButton_confirmComment.setGeometry(QtCore.QRect(100, 230, 111, 41))
        self.pushButton_confirmComment.setObjectName("pushButton_confirmComment")
        self.pushButton_confirmComment.clicked.connect(self.comment_clicked)
        self.pushButton_confirmComment.setText("Done")
        
        #cancel push button
        self.pushButton_cancelComment = QtWidgets.QPushButton(self)
        self.pushButton_cancelComment.setGeometry(QtCore.QRect(280, 230, 111, 41))
        self.pushButton_cancelComment.setObjectName("pushButton_cancelComment")
        self.pushButton_cancelComment.clicked.connect(self.cancel_addComment)
        self.pushButton_cancelComment.setText("Cancel")
        self.comment = ""

    def comment_clicked(self):
        # If the user enters a login name and clicks "login"
        if self.lineEdit_comment.text():
            #Saves the name of the user on the line edit
            self.comment = self.lineEdit_comment.text()

            #Creates the time stamp for when the use signs in
            # mm/dd/YY H:M
            timeStamp = datetime.now().strftime("%m/%d/%Y %H:%M")

            #Opens the log.txt file and appends the username to it and closes it
            f = open('log.txt','a') #append
            f.write("<" + timeStamp + "> User added comment \"" + self.comment + "\"\n")
            f.close()

            #Clears the line edit and closes the window
            self.lineEdit_comment.clear()
            self.done(1)

        # If the user does not enter a login name and clicks "Done"
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Please enter a comment before clicking done.")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def cancel_addComment(self):
        #Clears the line edit and closes the window
        self.lineEdit_comment.clear()
        self.done(1)