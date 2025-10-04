import sys
from PyQt6 import QtWidgets
from final_log_in_form import Ui_Dialog   # Login form UI
from sign_up import Ui_SignIn            # Sign Up form UI
from WELCOME import Ui_Dialog as UI_Welcome  # Welcome page UI
import sqlite3


# ---- Welcome Page ----
class WELCOMEPAGE(QtWidgets.QDialog, UI_Welcome):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# ---- Login Window ----
class LoginWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # connect "Sign Up Here" button to open the SignUp window
        self.signup.clicked.connect(self.open_signin)

        # connect "Login" button to check_login function
        self.pushButton.clicked.connect(self.check_login)

    def open_signin(self):
        """Open the Sign Up window and close Login window"""
        self.signin = SignInWindow()
        self.signin.show()
        self.close()

    def check_login(self):
        """Check if username + password exist in database"""
        uname = self.username.text()
        pword = self.password.text()

        if uname == "" or pword == "":
            self.message.setText("⚠ Please enter username and password")
            return

        try:
            # connect to SQLite database
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()

            # check if username & password exist
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pword))
            result = cursor.fetchone()
            conn.close()

            if result:  # ✅ login successful
                self.welcome = WELCOMEPAGE()
                self.welcome.show()
                self.close()
            else:  # ❌ no match found
                self.message.setText("❌ Invalid username or password")

        except Exception as e:
            self.message.setText(f"DB Error: {e}")


# ---- Sign Up Window ----
class SignInWindow(QtWidgets.QDialog, Ui_SignIn):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # connect "Already have account? Log in"
        self.login_redirect.clicked.connect(self.open_login)

        # connect "SIGN UP" button to save_account function
        self.signup_btn.clicked.connect(self.save_account)

    def open_login(self):
        """Go back to the Login window"""
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def save_account(self):
        """Save a new account into the database"""
        username = self.username.text()
        password = self.password.text()
        confirm = self.confirm_password.text()

        # basic validation
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required")
            return
        if password != confirm:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        # connect to SQLite DB
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()

        # make sure table exists (create if not)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)

        try:
            # insert new account
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Success", "Account created!")

            # clear input fields after success
            self.username.clear()
            self.password.clear()
            self.confirm_password.clear()
        except sqlite3.IntegrityError:
            # happens when username already exists
            QtWidgets.QMessageBox.warning(self, "Error", "Username already exists")
        finally:
            conn.close()


# ---- Main Program ----
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()   # start with Login window
    window.show()
    sys.exit(app.exec())
