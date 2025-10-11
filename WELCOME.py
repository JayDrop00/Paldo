# Form implementation generated from reading ui file 'WELCOME.ui'
# Created by: PyQt6 UI code generator 6.4.2

from PyQt6 import QtCore, QtGui, QtWidgets
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(941, 631)
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(-1, -1, 941, 631))
        self.widget.setStyleSheet("QWidget {\n"
"    background-color: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0, x2:1, y2:1,\n"
"        stop:0 #ffffff,\n"
"        stop:0.4 #cbf7ff,\n"
"        stop:1 #a6ecf7\n"
"    );\n"
"}")
        self.widget.setObjectName("widget")
        self.mainwidget = QtWidgets.QWidget(parent=self.widget)
        self.mainwidget.setEnabled(True)
        self.mainwidget.setGeometry(QtCore.QRect(0, 0, 941, 631))
        self.mainwidget.setStyleSheet("#label_phrase{\n"
"    font-family: \"Open Sans Light\";\n"
"    font-size: 12pt;\n"
"    font-weight: 300;\n"
"    color: #002B5B;\n"
"    border: none;\n"
"    background: transparent;\n"
"}")
        self.mainwidget.setObjectName("mainwidget")

        # --- Sidebar and Buttons (UNCHANGED) ---
        self.frame_sidebar = QtWidgets.QFrame(parent=self.mainwidget)
        self.frame_sidebar.setGeometry(QtCore.QRect(10, 70, 161, 541))
        self.frame_sidebar.setStyleSheet("#frame_sidebar {\n"
"    background-color: #002B5B;\n"
"    border-top-right-radius: 25px;\n"
"    border-bottom-right-radius: 25px;\n"
"}")
        self.frame_sidebar.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_sidebar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_sidebar.setObjectName("frame_sidebar")

        self.pushButton_home = QtWidgets.QPushButton(parent=self.frame_sidebar)
        self.pushButton_home.setGeometry(QtCore.QRect(40, 30, 91, 31))
        self.pushButton_home.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: #00E5FF;\n"
"    border: 2px solid #00E5FF;\n"
"    border-radius: 12px;\n"
"}")
        self.pushButton_home.setObjectName("pushButton_home")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame_sidebar)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 80, 91, 31))
        self.pushButton_2.setStyleSheet(self.pushButton_home.styleSheet())
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame_sidebar)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 130, 91, 31))
        self.pushButton_3.setStyleSheet(self.pushButton_home.styleSheet())
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame_sidebar)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 180, 91, 31))
        self.pushButton_4.setStyleSheet(self.pushButton_home.styleSheet())
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame_sidebar)
        self.pushButton_5.setGeometry(QtCore.QRect(40, 230, 91, 31))
        self.pushButton_5.setStyleSheet(self.pushButton_home.styleSheet())
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.frame_sidebar)
        self.pushButton_6.setGeometry(QtCore.QRect(40, 480, 91, 31))
        self.pushButton_6.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: #00E5FF;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")

        # --- (Rest of your UI labels and frames UNCHANGED) ---
        self.label_welcome = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_welcome.setGeometry(QtCore.QRect(210, 100, 271, 41))
        self.label_welcome.setStyleSheet("#label_welcome { color: #00E5FF; font-size: 34pt; font-weight: 800; }")
        self.label_welcome.setObjectName("label_welcome")

        self.label_username = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_username.setGeometry(QtCore.QRect(450, 110, 151, 31))
        self.label_username.setStyleSheet("#label_username { color: #00B8D4; font-size: 16pt; }")
        self.label_username.setObjectName("label_username")

        # --- Connect Logout Button ---
        self.pushButton_6.clicked.connect(self.logout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def logout(self):
        """Closes this form and shows the login screen."""
        from LOGIN import Ui_Form as LoginForm  # Import your login form here
        self.window = QtWidgets.QWidget()
        self.ui = LoginForm()
        self.ui.setupUi(self.window)
        self.window.show()
        # Close the current window
        QtWidgets.QApplication.instance().activeWindow().close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "WELCOME"))
        self.pushButton_home.setText(_translate("Form", "Home"))
        self.pushButton_2.setText(_translate("Form", "Inventory"))
        self.pushButton_3.setText(_translate("Form", "Sales"))
        self.pushButton_4.setText(_translate("Form", "Prediction"))
        self.pushButton_5.setText(_translate("Form", "Income"))
        self.pushButton_6.setText(_translate("Form", "Log Out"))
        self.label_welcome.setText(_translate("Form", "Welcome!"))
        self.label_username.setText(_translate("Form", "[USERNAME]"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
