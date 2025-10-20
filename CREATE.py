# Form implementation generated from reading ui file 'CREATE.ui'
# Created by: PyQt6 UI code generator 6.4.2

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(QtCore.QObject):  # 👈 inherits QObject to allow eventFilter
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(941, 631)
        self.mainwidget2 = QtWidgets.QWidget(parent=Form)
        self.mainwidget2.setGeometry(QtCore.QRect(0, 0, 941, 631))
        self.mainwidget2.setStyleSheet("QWidget {\n"
"    background-color: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0, x2:1, y2:1,\n"
"        stop:0 #ffffff,\n"
"        stop:0.4 #cbf7ff,\n"
"        stop:1 #a6ecf7\n"
"    );\n"
"}")
        self.mainwidget2.setObjectName("mainwidget2")
        self.mainwidget = QtWidgets.QWidget(parent=self.mainwidget2)
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

        self.label_logo = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_logo.setGeometry(QtCore.QRect(70, 150, 311, 331))
        self.label_logo.setStyleSheet("#label_logo{\n"
"border-image: url(\"C:/Users/USER/Documents/system_90/nagao_backend/ENTREPREDICT_Icon_Option_1_-_Circuit-Graph_E-removebg-preview.png\");\n"
"border-radius: 25px;\n"
"background:none;\n"
"}")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")

        self.label_smalllogo = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_smalllogo.setGeometry(QtCore.QRect(10, 0, 51, 61))
        self.label_smalllogo.setStyleSheet("#label_smalllogo{\n"
"border-image: url(\"C:/Users/USER/Documents/system_90/nagao_backend/ENTREPREDICT_Icon_Option_1_-_Circuit-Graph_E-removebg-preview.png\");\n"
"}")
        self.label_smalllogo.setText("")
        self.label_smalllogo.setObjectName("label_smalllogo")

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

        self.frameCreate = QtWidgets.QFrame(parent=self.mainwidget)
        self.frameCreate.setGeometry(QtCore.QRect(470, 130, 370, 400))
        self.frameCreate.setStyleSheet("#frameCreate {\n"
"    background-color: rgba(255, 255, 255, 30);\n"
"    border: 2px solid #00bfa6;\n"
"    border-radius: 15px;\n"
"}")
        self.frameCreate.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameCreate.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameCreate.setObjectName("frameCreate")

        self.label_login_title = QtWidgets.QLabel(parent=self.frameCreate)
        self.label_login_title.setGeometry(QtCore.QRect(100, 40, 191, 31))
        self.label_login_title.setStyleSheet("#label_login_title {\n"
"    font-family: \"Segoe UI Semibold\";\n"
"    font-size: 20pt;\n"
"    color: #001F3F;\n"
"    background: transparent;\n"
"}")
        self.label_login_title.setObjectName("label_login_title")

        self.lineEdit_fullnameCreate = QtWidgets.QLineEdit(parent=self.frameCreate)
        self.lineEdit_fullnameCreate.setGeometry(QtCore.QRect(60, 110, 251, 31))
        self.lineEdit_fullnameCreate.setStyleSheet("#lineEdit_fullnameCreate {\n"
"    border: 1px solid #00bfa6;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    background: rgba(255, 255, 255, 120);\n"
"    color: #002B5B;\n"
"}")
        self.lineEdit_fullnameCreate.setObjectName("lineEdit_fullnameCreate")

        self.lineEdit_usernameCreate = QtWidgets.QLineEdit(parent=self.frameCreate)
        self.lineEdit_usernameCreate.setGeometry(QtCore.QRect(60, 160, 251, 31))
        self.lineEdit_usernameCreate.setStyleSheet("#lineEdit_usernameCreate {\n"
"    border: 1px solid #00bfa6;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    background: rgba(255, 255, 255, 120);\n"
"    color: #002B5B;\n"
"}")
        self.lineEdit_usernameCreate.setObjectName("lineEdit_usernameCreate")

        self.lineEdit_passwordCreate = QtWidgets.QLineEdit(parent=self.frameCreate)
        self.lineEdit_passwordCreate.setGeometry(QtCore.QRect(60, 210, 251, 31))
        self.lineEdit_passwordCreate.setStyleSheet("#lineEdit_passwordCreate {\n"
"    border: 1px solid #00bfa6;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    background: rgba(255, 255, 255, 120);\n"
"    color: #002B5B;\n"
"}")
        self.lineEdit_passwordCreate.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_passwordCreate.setObjectName("lineEdit_passwordCreate")

        self.toolButton_eyeCreate = QtWidgets.QToolButton(parent=self.frameCreate)
        self.toolButton_eyeCreate.setGeometry(QtCore.QRect(280, 210, 21, 31))
        self.toolButton_eyeCreate.setStyleSheet("#toolButton_eyeCreate {\n"
"    background: transparent;\n"
"    border: none;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/view.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_eyeCreate.setIcon(icon)
        self.toolButton_eyeCreate.setObjectName("toolButton_eyeCreate")

        self.lineEdit_confirmpasswordCreate = QtWidgets.QLineEdit(parent=self.frameCreate)
        self.lineEdit_confirmpasswordCreate.setGeometry(QtCore.QRect(60, 260, 251, 31))
        self.lineEdit_confirmpasswordCreate.setStyleSheet("#lineEdit_confirmpasswordCreate {\n"
"    border: 1px solid #00bfa6;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    background: rgba(255, 255, 255, 120);\n"
"    color: #002B5B;\n"
"}")
        self.lineEdit_confirmpasswordCreate.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_confirmpasswordCreate.setObjectName("lineEdit_confirmpasswordCreate")

        self.toolButton_eye_confirmCreate = QtWidgets.QToolButton(parent=self.frameCreate)
        self.toolButton_eye_confirmCreate.setGeometry(QtCore.QRect(280, 260, 21, 31))
        self.toolButton_eye_confirmCreate.setStyleSheet("#toolButton_eye_confirmCreate {\n"
"    background: transparent;\n"
"    border: none;\n"
"}")
        self.toolButton_eye_confirmCreate.setIcon(icon)
        self.toolButton_eye_confirmCreate.setObjectName("toolButton_eye_confirmCreate")

        self.pushButton_login = QtWidgets.QPushButton(parent=self.frameCreate)
        self.pushButton_login.setGeometry(QtCore.QRect(60, 320, 241, 41))
        self.pushButton_login.setStyleSheet("#pushButton_login {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #00bfa5, stop:1 #1de9b6);\n"
"    border: none;\n"
"    border-radius: 20px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"}")
        self.pushButton_login.setObjectName("pushButton_login")

        self.label_upperhome.raise_()
        self.label_logo.raise_()
        self.label_smalllogo.raise_()
        self.plainTextEdit_Entrep.raise_()
        self.frameCreate.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # --- Placeholder behavior setup ---
        self.placeholders = {
            self.lineEdit_fullnameCreate: "FULLNAME",
            self.lineEdit_usernameCreate: "USERNAME",
            self.lineEdit_passwordCreate: "PASSWORD",
            self.lineEdit_confirmpasswordCreate: "PASSWORD",
        }
        for lineEdit, text in self.placeholders.items():
            lineEdit.setPlaceholderText(text)
            lineEdit.installEventFilter(self)

    def eventFilter(self, obj, event):
        # remove text on focus, restore if empty on focus out
        if obj in self.placeholders:
            if event.type() == QtCore.QEvent.Type.FocusIn:
                if obj.text() == self.placeholders[obj]:
                    obj.clear()
            elif event.type() == QtCore.QEvent.Type.FocusOut:
                if not obj.text():
                    obj.setText(self.placeholders[obj])
        return super().eventFilter(obj, event)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.plainTextEdit_Entrep.setPlainText(_translate("Form", "ENTREPREDICT"))
        self.label_login_title.setText(_translate("Form", "Create Account"))
        self.pushButton_login.setText(_translate("Form", "Create"))
        self.toolButton_eyeCreate.setText(_translate("Form", "..."))
        self.toolButton_eye_confirmCreate.setText(_translate("Form", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
