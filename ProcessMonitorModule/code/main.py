
from shared import UserManager



import sys
import os
import datetime
import psutil
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QInputDialog, QApplication, QButtonGroup, QRadioButton, QWidget, QMessageBox,QVBoxLayout,QLabel,QLineEdit,QPushButton



StopTime = ['2024-05-17 18:00:05.122148', '2024-05-17 18:40:10.146448', '2024-05-17 18:40:05.122148']
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
    def __init__(self, parent=None):
        super(UserManagerDialog, self).__init__(parent)
        self.setWindowTitle("User Manager")
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)

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
        self.tableWidget.setColumnWidth(7, 100)
        self.tableWidget.setRowHeight(7, 1000)
        self.tableWidget.setColumnWidth(8, 100)
        self.tableWidget.setRowHeight(8, 1000)

        self.main_layout = QVBoxLayout()

        self.user_manager = UserManager()

        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")


        self.open_user_manager_button = QPushButton("Open User Manager")
        self.open_user_manager_button.clicked.connect(self.open_user_manager)

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.open_user_manager_button)



        self.loaddata()

        self.setLayout(self.main_layout)

    def open_user_manager(self):
        user_manager_dialog = UserManagerDialog(self)  
        user_manager_dialog.show()



    def loaddata(self):
        processes = [
            {"SerialNo": "1", "PName": "Process CommunicationModule", "RunningStatus": "Not Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "47", "MemoryUse%": "26", "NoOfOpenFiles": "2", "StartOrStopTime": "StopTime:"+StopTime[0]},
            {"SerialNo": "2", "PName": "Process CommunicationModule", "RunningStatus": "Not Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "37", "MemoryUse%": "36", "NoOfOpenFiles": "3", "StartOrStopTime": "StopTime:"+StopTime[1]},
            {"SerialNo": "3", "PName": "Process CommandController", "RunningStatus": "Not Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "27", "MemoryUse%": "46", "NoOfOpenFiles": "4", "StartOrStopTime":"StopTime:"+ StopTime[2]},
            {"SerialNo": "4", "PName": "Process CommunicationModule", "RunningStatus": "Running", "StartBtn": "START", "KillBtn": "KILL", "CPUUse%": "87", "MemoryUse%": "56", "NoOfOpenFiles": "6", "StartOrStopTime": "StartTime:"+StartTime[0]}
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
            start_btn.setEnabled(str(process["RunningStatus"]) == "Not Running")
            kill_btn = QtWidgets.QPushButton(kill_btn_text)
            kill_btn.clicked.connect(lambda _, btn=kill_btn: self.kill_process(btn))
            kill_btn.setDisabled(str(process["RunningStatus"]) == "Running")
            kill_btn.setDisabled(str(process["RunningStatus"]) == "Not Running")


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

    '''def usermanagermodule(self):
        userm=setUserManager'''


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setWindowTitle("Process Monitor Module")
    widget.setFixedHeight(210)
    widget.setFixedWidth(1210)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
