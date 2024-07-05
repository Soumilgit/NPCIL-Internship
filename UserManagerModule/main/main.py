
from shared import UserManager


import sys
from PyQt5.QtWidgets import QDialog, QInputDialog, QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class User:
    id_counter = 0

    def __init__(self, username, password):
        self.id = User.id_counter
        User.id_counter += 1
        self.username = username
        self.password = password

    def __str__(self):
        return f"ID: {self.id}, Username: {self.username}, Password: {self.password}"

class UserManager:
    def __init__(self):
        self.users_list = []

    def add_user(self, username, password):
        user = User(username, password)
        self.users_list.append(user)
        print(f"Added user: {user}")

    def get_user_by_username(self, username):
        return next((u for u in self.users_list if u.username == username), None)

    def edit_user(self, username, new_password):
        user_to_edit = self.get_user_by_username(username)
        if user_to_edit:
            index = self.users_list.index(user_to_edit)
            user_to_edit.password = new_password
            print(f"Updated user: {username} with new password: {new_password}")
        else:
            print(f"User {username} not found.")

class UserManagerDialog(QDialog):
    def __init__(self,  parent=None):
        super(UserManagerDialog, self).__init__()  
        self.setWindowTitle("User Manager")

        self.user_manager = parent

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(lambda: self.add_user())

        self.edit_user_button = QPushButton("Edit User")
        self.edit_user_button.clicked.connect(lambda: self.edit_user())

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.add_user_button)
        layout.addWidget(self.edit_user_button)

        self.setLayout(layout)

    def add_user(self):
        username, okPressed = QInputDialog.getText(self, "Add User","Enter username:", QLineEdit.Normal, "")
        if okPressed and username != '':
            password, okPressed = QInputDialog.getText(self, "Add User","Enter password:", QLineEdit.Normal, "")
            if okPressed and password != '':
                self.user_manager.add_user(username, password)
                self.close()

    def edit_user(self):
        username, okPressed = QInputDialog.getText(self, "Edit User","Enter username of user to edit:", QLineEdit.Normal, "")
        if okPressed and username != '':
            user_to_edit = self.user_manager.get_user_by_username(username)
            if user_to_edit:
                dialog = EditUserDialog(user_to_edit, self)
                dialog.exec_()
            else:
                QMessageBox.critical(self, "Error", "User not found.")

class EditUserDialog(QDialog):
    def __init__(self, user_to_edit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit User")
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(user_to_edit.username)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(lambda: self.parent().user_manager.update_user(user_to_edit.username, self.password_input.text()))

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        layout = QVBoxLayout()
        greeting = QLabel("Welcome to the User Management Application.")
        layout.addWidget(greeting)
        self.setLayout(layout)

        self.user_manager = UserManager()
        self.user_manager_dialog = UserManagerDialog(self.user_manager, self)
        self.user_manager_dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
