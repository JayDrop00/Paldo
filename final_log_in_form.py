# Modern themed Login Form in PyQt6 + SQLite Login
from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 650)
        Dialog.setStyleSheet("background-color: #dde1e7;")

        # ---- Card ----
        self.card = QtWidgets.QFrame(parent=Dialog)
        self.card.setGeometry(QtCore.QRect(50, 50, 400, 550))
        self.card.setStyleSheet("QFrame { background: white; border-radius: 20px; }")

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.card.setGraphicsEffect(shadow)

        # ---- Logo ----
        self.logo = QtWidgets.QLabel(parent=self.card)
        self.logo.setGeometry(QtCore.QRect(0, 20, self.card.width(), 200))
        pixmap = QtGui.QPixmap(r"C:/Users/USER/Documents/pyqt/final_logo1.png")
        scaled_pixmap = pixmap.scaled(380, 180, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                      QtCore.Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(scaled_pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ---- Title ----
        self.label = QtWidgets.QLabel(parent=self.card)
        self.label.setGeometry(QtCore.QRect(30, 140, 340, 50))
        self.label.setStyleSheet("""
        color: black;
        font-size: 32px;
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
            """)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # ---- Username ----
        self.username = QtWidgets.QLineEdit(parent=self.card)
        self.username.setGeometry(QtCore.QRect(40, 210, 320, 45))
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet(self._input_style())

        # ---- Password ----
        self.password = QtWidgets.QLineEdit(parent=self.card)
        self.password.setGeometry(QtCore.QRect(40, 270, 320, 45))
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(self._input_style())

        # ---- Login Button ----
        self.pushButton = QtWidgets.QPushButton(parent=self.card)
        self.pushButton.setGeometry(QtCore.QRect(40, 330, 320, 50))
        self.pushButton.setStyleSheet("""
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
        self.pushButton.setText("LOG IN")
        self.pushButton.clicked.connect(self.check_login)  # ✅ connect to login function

        # ---- Forgot Password ----
        self.forgot_password = QtWidgets.QPushButton(parent=self.card)
        self.forgot_password.setGeometry(QtCore.QRect(80, 400, 120, 30))
        self.forgot_password.setStyleSheet(self._link_style())
        self.forgot_password.setText("Forgot Password?")

        # ---- Sign Up ----
        self.signup = QtWidgets.QPushButton(parent=self.card)
        self.signup.setGeometry(QtCore.QRect(210, 400, 120, 30))
        self.signup.setStyleSheet(self._link_style())
        self.signup.setText("Sign Up Here")

        # ---- Message (feedback) ----
        self.message = QtWidgets.QLabel(parent=self.card)
        self.message.setGeometry(QtCore.QRect(40, 470, 320, 40))
        self.message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.message.setStyleSheet("color: red; font-size: 12px;")

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

    def _link_style(self):
        return """
            QPushButton {
                color: #4a90e2;
                font-size: 12px;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.label.setText(_translate("Dialog", "WELCOME"))

    # ---- LOGIN FUNCTION ----
    def check_login(self):
        uname = self.username.text()
        pword = self.password.text()

        if uname == "" or pword == "":
            self.message.setText("⚠ Please enter username and password")
            return

        try:
            conn = sqlite3.connect("mydatabase.db")  # ✅ connect to your DB
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pword))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.message.setStyleSheet("color: green; font-size: 12px;")
                self.message.setText("✅ Login successful!")
            else:
                self.message.setStyleSheet("color: red; font-size: 12px;")
                self.message.setText("❌ Invalid username or password")
        except Exception as e:
            self.message.setText(f"DB Error: {e}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
