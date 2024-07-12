
from shared import UserManager,create_connection, select_user




import sys
import os
import datetime
import psutil
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QInputDialog, QApplication, QButtonGroup, QRadioButton, QWidget, QMessageBox,QVBoxLayout,QLabel,QLineEdit,QPushButton



StopTime = ['2024-05-17 18:00:05.122148', '2024-05-17 18:40:10.146448']
StartTime = ['2024-05-17 17:40:05.123456 ']

class User:
    id_counter = 0

    def __init__(self, username, password):
        self.id = User.id_counter
        User.id_counter += 1
        self.username = username
        self.password = password

    def __str__(self):
        return f"ID: {self.id}, Username: {self.username}, Password: {self.password}"


class UserManagerDialog(QDialog):
    def __init__(self,  parent=None):

            super(UserManagerDialog , self).__init__(parent)
            self.user_manager = parent.user_manager
            #self.user_manager.user_authenticated_signal.connect(self.enable_buttons)
            self.setWindowTitle("User Manager")

            #self.user_manager = parent

            layout = QVBoxLayout()

            self.username_label = QLabel("Username:")
            self.username_input = QLineEdit()
            self.password_label = QLabel("Password:")
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)

            self.add_user_button = QPushButton("Add User")
            self.add_user_button.clicked.connect(lambda: self.add_user())



            layout.addWidget(self.username_label)
            layout.addWidget(self.username_input)
            layout.addWidget(self.password_label)
            layout.addWidget(self.password_input)
            layout.addWidget(self.add_user_button)


            self.setLayout(layout)

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = User(username, password)
        print(f"Added user: {user}")
        self.close()

    '''def enable_buttons(self, username):
        if username in self.user_manager.authenticated_users:
            self.add_user_button.setEnabled(True)
            self.edit_user_button.setEnabled(True)
        else:
            self.add_user_button.setEnabled(False)
            self.edit_user_button.setEnabled(False)'''



class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("table.ui", self)




        self.process_states = {}
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setRowHeight(0, 1000)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setRowHeight(1, 1000)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setRowHeight(2, 1000)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setRowHeight(3, 1000)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setRowHeight(4, 1000)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setRowHeight(5, 1000)
        self.tableWidget.setColumnWidth(6, 100)
        self.tableWidget.setRowHeight(6, 1000)
        self.tableWidget.setColumnWidth(7, 150)
        self.tableWidget.setRowHeight(7, 1000)
        self.tableWidget.setColumnWidth(8, 300)
        self.tableWidget.setRowHeight(8, 1000)

        self.setWindowTitle("Main Application Window")
        self.main_layout = QVBoxLayout()


        self.setLayout(self.main_layout)
        self.user_manager = UserManager()

        self.user_manager = UserManager()



        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")


        self.open_user_manager_button = QPushButton("Open User Manager")
        self.open_user_manager_button.clicked.connect(self.open_user_manager)

        self.main_layout.addStretch(50)
        self.main_layout.addWidget(self.open_user_manager_button)

        self.main_layout.addStretch(1)


        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.main_layout.addWidget(self.login_button)



        self.loaddata()

        self.setLayout(self.main_layout)

    def open_user_manager(self):
        user_manager_dialog = UserManagerDialog(self)
        user_manager_dialog.show()



    def loaddata(self):
        processes = [
            {"SerialNo": "1", "PName": "Process CommunicationModule", "RunningStatus": "Not Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "47", "MemoryUse%": "26", "NoOfOpenFiles": "2", "StartOrStopTime": "StopTime:"+StopTime[0]},
            {"SerialNo": "2", "PName": "Process CommunicationModule", "RunningStatus": "Not Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "37", "MemoryUse%": "36", "NoOfOpenFiles": "3", "StartOrStopTime": "StopTime:"+StopTime[1]},
            {"SerialNo": "3", "PName": "Process CommandController", "RunningStatus": "Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "27", "MemoryUse%": "46", "NoOfOpenFiles": "4", "StartOrStopTime":"StartTime:"+ StopTime[0]},

        ]
        row = 0
        self.tableWidget.setRowCount(len(processes))
        for process in processes:
            serial_no_item = QtWidgets.QTableWidgetItem(str(process["SerialNo"]))
            pname_item = QtWidgets.QTableWidgetItem(str(process["PName"]))
            running_status_item = QtWidgets.QTableWidgetItem(str(process["RunningStatus"]))
            if str(process["RunningStatus"]) == "Not Running":
                running_status_item.setBackground(Qt.red)
            else:
                running_status_item.setBackground(Qt.green)
            start_btn_text = f"{process['StartBtn']} "
            kill_btn_text = f"{process['KillBtn']}"
            start_btn = QtWidgets.QPushButton(start_btn_text)
            start_btn.clicked.connect(lambda _, btn=start_btn: self.start_process(btn))

            kill_btn = QtWidgets.QPushButton(kill_btn_text)
            kill_btn.clicked.connect(lambda _, btn=kill_btn: self.kill_process(btn))

            start_btn.setDisabled(True)
            kill_btn.setDisabled(True)



            if str(process["RunningStatus"]) == "Not Running":
                start_btn.setDisabled(False)
            elif str(process["RunningStatus"]) == "Running":
                kill_btn.setDisabled(False)

            cpu_use_per_item = QtWidgets.QTableWidgetItem(str(process["CPUUse%"]))
            memory_use_per_item = QtWidgets.QTableWidgetItem(str(process["MemoryUse%"]))
            no_of_open_files_item = QtWidgets.QTableWidgetItem(str(process["NoOfOpenFiles"]))
            time_item = QtWidgets.QTableWidgetItem(str(process["StartOrStopTime"]))
            self.tableWidget.setItem(row, 0, serial_no_item)
            self.tableWidget.setItem(row, 1, pname_item)
            self.tableWidget.setItem(row, 2, running_status_item)
            self.tableWidget.setCellWidget(row, 3, start_btn)
            self.tableWidget.setCellWidget(row, 4, kill_btn)

            self.tableWidget.setItem(row, 5, cpu_use_per_item)
            self.tableWidget.setItem(row, 6, memory_use_per_item)
            self.tableWidget.setItem(row, 7, no_of_open_files_item)
            self.tableWidget.setItem(row, 8, time_item)
            row += 1

    def handle_login(self):
           username, okPressed = QInputDialog.getText(self, "Login","Enter username:", QLineEdit.Normal, "")
           if okPressed and username != '':
               password, okPressed = QInputDialog.getText(self, "Login","Enter password:", QLineEdit.Normal, "")
               if okPressed and password != '':
                   connection = create_connection()
                   user_data = select_user(connection, username, password)
                   if user_data:
                       self.user_manager_dialog = UserManagerDialog(self)
                       self.user_manager_dialog.show()
                       for i in range(self.tableWidget.rowCount()):
                            running_status = self.tableWidget.item(i, 2).text()
                            start_btn = self.tableWidget.cellWidget(i, 3)
                            kill_btn = self.tableWidget.cellWidget(i, 4)
                            if running_status == "Not Running":
                                start_btn.setEnabled(True)
                                kill_btn.setDisabled(True)
                            elif running_status == "Running":
                                start_btn.setDisabled(True)
                                kill_btn.setEnabled(True)
                   else:
                       QMessageBox.critical(self, "Error", "Invalid credentials.")
                   connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setWindowTitle("Process Monitor Module")
    widget.setFixedHeight(212)
    widget.setFixedWidth(1132)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
