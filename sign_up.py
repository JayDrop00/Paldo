# Modern themed Sign In Form in PyQt6
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtWidgets

class Ui_SignIn(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 650)
        Dialog.setStyleSheet("background-color: #dde1e7;")  # soft background

        # ---- Card ----
        self.card = QtWidgets.QFrame(parent=Dialog)
        self.card.setGeometry(QtCore.QRect(50, 50, 400, 550))
        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
            }
        """)

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.card.setGraphicsEffect(shadow)

        # ---- Logo ----
        self.logo = QtWidgets.QLabel(parent=self.card)
        self.logo.setGeometry(QtCore.QRect(0, 20, self.card.width(), 150))
        pixmap = QtGui.QPixmap(r"C:/Users/USER/Documents/pyqt/final_logo1.png")
        scaled_pixmap = pixmap.scaled(200, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                      QtCore.Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(scaled_pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ---- Title ----
        self.label = QtWidgets.QLabel(parent=self.card)
        self.label.setGeometry(QtCore.QRect(30, 150, 340, 50))
        self.label.setStyleSheet("""
        color: black;
        font-size: 28px;
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
            """)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setText("CREATE ACCOUNT")

        # ---- Username ----
        self.username = QtWidgets.QLineEdit(parent=self.card)
        self.username.setGeometry(QtCore.QRect(40, 210, 320, 45))
        self.username.setStyleSheet(self._input_style())
        self.username.setPlaceholderText("Username")

        # ---- Password ----
        self.password = QtWidgets.QLineEdit(parent=self.card)
        self.password.setGeometry(QtCore.QRect(40, 270, 320, 45))
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(self._input_style())
        self.password.setPlaceholderText("Password")

        # ---- Confirm Password ----
        self.confirm_password = QtWidgets.QLineEdit(parent=self.card)
        self.confirm_password.setGeometry(QtCore.QRect(40, 330, 320, 45))
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password.setStyleSheet(self._input_style())
        self.confirm_password.setPlaceholderText("Confirm Password")

        # ---- Sign In Button ----
        self.signup_btn = QtWidgets.QPushButton(parent=self.card)
        self.signup_btn.setGeometry(QtCore.QRect(40, 400, 320, 50))
        self.signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        self.signup_btn.setText("SIGN UP")

        # ---- Already have account ----
        self.login_redirect = QtWidgets.QPushButton(parent=self.card)
        self.login_redirect.setGeometry(QtCore.QRect(100, 470, 200, 30))
        self.login_redirect.setStyleSheet("""
            QPushButton {
                color: #4a90e2;
                font-size: 12px;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.login_redirect.setText("Already have an account? Log in")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def _input_style(self):
        return """
            QLineEdit {
                border: none;
                border-radius: 20px;
                padding-left: 15px;
                font-size: 14px;
                background-color: #f0f0f0;
                color: black;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                border: 2px solid #4a90e2;
            }
        """

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sign In"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_SignIn()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
