# Form implementation generated from reading ui file 'ENTREPREDICT.ui'
#
# Modified: Added clear-on-click + input validation (no UI design changes)
# Created by: PyQt6 UI code generator 6.4.2

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(938, 631)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("background: qlineargradient(\n"
"    spread:pad,\n"
"    x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #A6EFFF,\n"
"    stop:1 #E0FBFF\n"
");\n"
"\n"
"")
        self.mainwidget = QtWidgets.QWidget(parent=Form)
        self.mainwidget.setEnabled(True)
        self.mainwidget.setGeometry(QtCore.QRect(0, 0, 941, 631))
        self.mainwidget.setStyleSheet("#label_phrase{\n"
"    font-family: \"Open Sans Light\";\n"
"    font-size: 12pt;\n"
"    font-weight: 300;\n"
"    color: #002B5B;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"")
        self.mainwidget.setObjectName("mainwidget")
        self.label_logo = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_logo.setGeometry(QtCore.QRect(609, 140, 311, 331))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(150)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setStyleSheet("#label_logo{\n"
"border-image: url(\"C:/Users/USER/Documents/system_90/nagao_backend/ENTREPREDICT_Icon_Option_1_-_Circuit-Graph_E-removebg-preview.png\");\n"
"border-radius: 25px;\n"
"background:none;\n"
"}")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.pushButton = QtWidgets.QPushButton(parent=self.mainwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 390, 161, 41))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #00d4ff, stop:1 #00bfa6);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 15px;\n"
"    font-family: \"Segoe UI Semibold\";\n"
"    font-size: 16pt;\n"
"    padding: 8px 24px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #00e6cc;\n"
"    border: 2px solid white;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #00997a;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label_smalllogo = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_smalllogo.setGeometry(QtCore.QRect(10, 0, 51, 61))
        self.label_smalllogo.setStyleSheet("#label_smalllogo{\n"
"background-color:#031b3d;\n"
"border-image: url(\"C:/Users/USER/Documents/system_90/nagao_backend/ENTREPREDICT_Icon_Option_1_-_Circuit-Graph_E-removebg-preview.png\");\n"
"}")
        self.label_smalllogo.setText("")
        self.label_smalllogo.setObjectName("label_smalllogo")
        self.label_welcome = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_welcome.setGeometry(QtCore.QRect(60, 210, 511, 81))
        self.label_welcome.setStyleSheet("#label_welcome {\n"
"    font-family: \"Segoe UI Semibold\";\n"
"    font-size: 34pt;\n"
"    font-weight: 600;\n"
"    color: #001F3F;\n"
"    border:none;\n"
"background:transparent;\n"
"}")
        self.label_welcome.setObjectName("label_welcome")
        self.label_phrase = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_phrase.setGeometry(QtCore.QRect(80, 350, 281, 21))
        self.label_phrase.setStyleSheet("#label_phrase{\n"
"font-family:\"Lato Regular\";\n"
"}")
        self.label_phrase.setObjectName("label_phrase")
        self.label_entrep = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_entrep.setGeometry(QtCore.QRect(70, 280, 581, 61))
        self.label_entrep.setStyleSheet("#label_entrep {\n"
"    font-family: \"Exo 2 ExtraBold\";\n"
"    font-size: 50pt;\n"
"    font-weight: 800;\n"
"    color: #001F3F;\n"
"    border:none;\n"
"background:transparent;\n"
"}")
        self.label_entrep.setObjectName("label_entrep")
        self.label_upperhome = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_upperhome.setGeometry(QtCore.QRect(0, 0, 941, 61))
        self.label_upperhome.setStyleSheet("#label_upperhome{\n"
"background-color:#031b3d;\n"
"}")
        self.label_upperhome.setText("")
        self.label_upperhome.setObjectName("label_upperhome")
        self.plainTextEdit_Entrep = QtWidgets.QPlainTextEdit(parent=self.mainwidget)
        self.plainTextEdit_Entrep.setGeometry(QtCore.QRect(70, 20, 191, 41))
        self.plainTextEdit_Entrep.setStyleSheet("#plainTextEdit_Entrep{\n"
" font-family: \"Montserrat ExtraBold\";\n"
"    font-size: 16pt;\n"
"font-weight: 600;\n"
"color:white;\n"
"background-color:#031b3d;\n"
"border:none;\n"
"}")
        self.plainTextEdit_Entrep.setObjectName("plainTextEdit_Entrep")
        self.frame = QtWidgets.QFrame(parent=self.mainwidget)
        self.frame.setGeometry(QtCore.QRect(470, 130, 370, 400))
        self.frame.setStyleSheet("#frame {\n"
"    background-color: rgba(255, 255, 255, 30);\n"
"    border: 2px solid #00bfa6;\n"
"    border-radius: 15px;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.label_login_title = QtWidgets.QLabel(parent=self.frame)
        self.label_login_title.setGeometry(QtCore.QRect(140, 40, 101, 31))
        self.label_login_title.setStyleSheet("#label_login_title {\n"
"    font-family: \"Segoe UI Semibold\";\n"
"    font-size: 20pt;\n"
"    color: #001F3F;\n"
"    background: transparent;\n"
"    border: none;\n"
"}")
        self.label_login_title.setObjectName("label_login_title")
        self.lineEdit_username = QtWidgets.QLineEdit(parent=self.frame)
        self.lineEdit_username.setGeometry(QtCore.QRect(60, 110, 251, 31))
        self.lineEdit_username.setStyleSheet("#lineEdit_username {\n"
"    border: 1px solid #00bfa6;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    background: rgba(255, 255, 255, 120);\n"
"    color: #002B5B;\n"
"}")
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_password = QtWidgets.QLineEdit(parent=self.frame)
        self.lineEdit_password.setGeometry(QtCore.QRect(60, 160, 251, 31))
        self.lineEdit_password.setStyleSheet("#lineEdit_password {\n"
"    border: 1px solid #00bfa6;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    background: rgba(255, 255, 255, 120);\n"
"    color: #002B5B;\n"
"}")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.pushButton_login = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_login.setGeometry(QtCore.QRect(70, 240, 241, 41))
        self.pushButton_login.setStyleSheet("#pushButton_login {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #00bfa5, stop:1 #1de9b6);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    padding: 8px 16px;\n"
"}\n"
"#pushButton_login:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #1de9b6, stop:1 #a7ffeb);\n"
"}\n"
"#pushButton_login:pressed {\n"
"    background-color: #009e89;\n"
"}")
        self.pushButton_login.setObjectName("pushButton_login")
        self.label_create_account = QtWidgets.QLabel(parent=self.frame)
        self.label_create_account.setGeometry(QtCore.QRect(200, 320, 101, 20))
        self.label_create_account.setStyleSheet("#label_create_account {\n"
"    color: #00e6ac;\n"
"    font-size: 10pt;\n"
"    font-weight: 400;\n"
"    background: transparent;\n"
"    text-decoration: underline;\n"
"}")
        self.label_create_account.setObjectName("label_create_account")
        self.label_noAccount = QtWidgets.QLabel(parent=self.frame)
        self.label_noAccount.setGeometry(QtCore.QRect(50, 320, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        self.label_noAccount.setFont(font)
        self.label_noAccount.setStyleSheet("QLabel {\n"
"    color: #333;\n"
"    font-family: \"Segoe UI\";\n"
"    background: transparent;\n"
"}")
        self.label_noAccount.setObjectName("label_noAccount")
        self.toolButton_eye = QtWidgets.QToolButton(parent=self.frame)
        self.toolButton_eye.setGeometry(QtCore.QRect(280, 160, 21, 31))
        self.toolButton_eye.setStyleSheet("#toolButton_eye {\n"
"    background: transparent;\n"
"    border: none;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/view.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_eye.setIcon(icon)
        self.toolButton_eye.setObjectName("toolButton_eye")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # -------- FUNCTION: Clear-on-click behavior --------
        self.lineEdit_username.installEventFilter(Form)
        self.lineEdit_password.installEventFilter(Form)
        Form.eventFilter = self.eventFilter  # attach filter to form

        # -------- CONNECT LOGIN BUTTON --------
        self.pushButton_login.clicked.connect(self.handle_login)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.FocusIn:
            if obj.objectName() == "lineEdit_username" and obj.text() == "USERNAME":
                obj.clear()
            elif obj.objectName() == "lineEdit_password" and obj.text() == "PASSWORD":
                obj.clear()
        elif event.type() == QtCore.QEvent.Type.FocusOut:
            if obj.objectName() == "lineEdit_username" and obj.text() == "":
                obj.setText("USERNAME")
            elif obj.objectName() == "lineEdit_password" and obj.text() == "":
                obj.setText("PASSWORD")
        return False

    # -------- VALIDATION: Login input check --------
    def handle_login(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()

        if not username or not password or username == "USERNAME" or password == "PASSWORD":
            QtWidgets.QMessageBox.warning(None, "Input Error", "Please enter both username and password before logging in.")
            return

        # Placeholder for real login validation
        QtWidgets.QMessageBox.information(None, "Login", f"Welcome {username}! (Add DB validation here)")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Get Started"))
        self.label_welcome.setText(_translate("Form", " WELCOME TO "))
        self.label_phrase.setText(_translate("Form", "See the Future of Your Business Today."))
        self.label_entrep.setText(_translate("Form", "ENTREPREDICT"))
        self.plainTextEdit_Entrep.setPlainText(_translate("Form", "ENTREPREDICT"))
        self.label_login_title.setText(_translate("Form", "LOG IN"))
        self.lineEdit_username.setText(_translate("Form", "USERNAME"))
        self.lineEdit_password.setText(_translate("Form", "PASSWORD"))
        self.pushButton_login.setText(_translate("Form", "Login"))
        self.label_create_account.setText(_translate("Form", "Create Account"))
        self.label_noAccount.setText(_translate("Form", "Don\'t have an account?"))
        self.toolButton_eye.setText(_translate("Form", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
