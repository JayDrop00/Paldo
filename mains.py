import sqlite3
from PyQt6 import QtCore, QtWidgets, QtGui
from ENTREPREDICT import Ui_Form
from CREATE import Ui_Form as Ui_CreateForm
from WELCOME import Ui_Form as Ui_WelcomeForm  # Welcome UI import


# --- DATABASE SETUP ---
def init_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# --- CREATE ACCOUNT WINDOW ---
class CreateAccountWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CreateForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Create Account")
        try:
            self.ui.frameCreate.setEnabled(True)
        except Exception:
            pass

        # Connect create button
        self.ui.pushButton_login.clicked.connect(self.create_account)
        print("✅ Create Account page loaded!")

    def create_account(self):
        fullname = self.ui.lineEdit_fullnameCreate.text().strip()
        username = self.ui.lineEdit_usernameCreate.text().strip()
        password = self.ui.lineEdit_passwordCreate.text().strip()
        confirm = self.ui.lineEdit_confirmpasswordCreate.text().strip()

        if not fullname or not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill out all fields.")
            return

        if password != confirm:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)",
                           (fullname, username, password))
            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(self, "Success", "Account created successfully!")
            print(f"🧾 Account Created for: {fullname} ({username})")
            self.close()
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Error", "Username already exists!")


# --- MAIN LOGIN WINDOW ---
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Get widget references
        self.logo = self.findChild(QtWidgets.QLabel, "label_logo")
        self.welcome = self.findChild(QtWidgets.QLabel, "label_welcome")
        self.entrep = self.findChild(QtWidgets.QLabel, "label_entrep")
        self.phrase = self.findChild(QtWidgets.QLabel, "label_phrase")
        self.button = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.frame = self.findChild(QtWidgets.QFrame, "frame")
        self.login_button = self.findChild(QtWidgets.QPushButton, "pushButton_login")
        self.create_account_label = self.findChild(QtWidgets.QLabel, "label_create_account")

        print("\n=== DEBUG INFO ===")
        print("Login button found:", bool(self.login_button))
        print("Create account label found:", bool(self.create_account_label))
        print("Frame found:", bool(self.frame))
        print("===============================\n")

        # Connect signals
        if self.button:
            self.button.clicked.connect(self.start_transition)

        if self.login_button:
            self.login_button.clicked.connect(self.login_action)
            print("✅ Login button connected!")

        if self.create_account_label:
            self.create_account_label.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.create_account_label.mousePressEvent = lambda event: self.create_account_action()
            print("✅ Create Account label clickable!")

        QtCore.QTimer.singleShot(100, self.hide_login_form)

    def hide_login_form(self):
        if self.frame:
            self.frame.hide()
            print("✅ Login frame hidden on start.")

    # --- Transition animation for Get Started ---
    def start_transition(self):
        print("\n[DEBUG] Get Started clicked!")
        print("[DEBUG] Starting animations...")

        if not self.logo or not self.frame:
            print("❌ Missing logo or login frame!")
            return

        logo_anim = QtCore.QPropertyAnimation(self.logo, b"pos")
        logo_anim.setDuration(1000)
        logo_anim.setStartValue(self.logo.pos())
        logo_anim.setEndValue(QtCore.QPoint(100, self.logo.pos().y()))
        logo_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)

        fade_out_group = QtCore.QParallelAnimationGroup()
        for widget in [self.welcome, self.entrep, self.phrase, self.button]:
            if widget:
                effect = QtWidgets.QGraphicsOpacityEffect(widget)
                widget.setGraphicsEffect(effect)
                anim = QtCore.QPropertyAnimation(effect, b"opacity")
                anim.setDuration(600)
                anim.setStartValue(1)
                anim.setEndValue(0)
                fade_out_group.addAnimation(anim)

        self.frame.show()
        frame_effect = QtWidgets.QGraphicsOpacityEffect(self.frame)
        self.frame.setGraphicsEffect(frame_effect)

        fade_in_frame = QtCore.QPropertyAnimation(frame_effect, b"opacity")
        fade_in_frame.setDuration(1000)
        fade_in_frame.setStartValue(0)
        fade_in_frame.setEndValue(1)

        start_x = self.width()
        end_x = self.width() - self.frame.width() - 50

        slide_in = QtCore.QPropertyAnimation(self.frame, b"pos")
        slide_in.setDuration(1000)
        slide_in.setStartValue(QtCore.QPoint(start_x, self.frame.y()))
        slide_in.setEndValue(QtCore.QPoint(end_x, self.frame.y()))
        slide_in.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

        frame_anim_group = QtCore.QParallelAnimationGroup()
        frame_anim_group.addAnimation(fade_in_frame)
        frame_anim_group.addAnimation(slide_in)

        full_anim = QtCore.QParallelAnimationGroup()
        full_anim.addAnimation(logo_anim)
        full_anim.addAnimation(fade_out_group)
        full_anim.addAnimation(frame_anim_group)

        full_anim.start()
        self.anim_group = full_anim
        print("[DEBUG] Animation started!\n")

    # --- LOGIN BUTTON ACTION ---
    def login_action(self):
        print("🖱 Login button clicked!")
        self.glow_effect(self.login_button, "#00e6cc")

        username = self.ui.lineEdit_username.text().strip() if hasattr(self.ui, 'lineEdit_username') else ""
        password = self.ui.lineEdit_password.text().strip() if hasattr(self.ui, 'lineEdit_password') else ""

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter username and password.")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QtWidgets.QMessageBox.information(self, "Success", f"Welcome, {username}!")
            # OPEN WelcomeWindow (class below)
            self.open_welcome(username)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid username or password.")

    # --- OPEN WELCOME WINDOW ---
    def open_welcome(self, username):
        # create the WelcomeWindow (defined below)
        self.welcome_window = WelcomeWindow(username)
        self.welcome_window.show()

        # close the login window
        self.close()

    # --- CREATE ACCOUNT ACTION ---
    def create_account_action(self):
        print("🖱 Create Account clicked!")
        self.glow_effect(self.create_account_label, "#00e6cc")
        self.create_window = CreateAccountWindow()
        self.create_window.show()

    # --- GLOW EFFECT ---
    def glow_effect(self, widget, color="#00ffff"):
        if not widget:
            return

        glow = QtWidgets.QGraphicsDropShadowEffect()
        glow.setBlurRadius(0)
        glow.setColor(QtGui.QColor(color))
        glow.setOffset(0, 0)
        widget.setGraphicsEffect(glow)

        anim = QtCore.QVariantAnimation()
        anim.setDuration(400)
        anim.setStartValue(0)
        anim.setEndValue(30)
        anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

        def update_glow(value):
            glow.setBlurRadius(value)
            glow.setColor(QtGui.QColor(color).lighter(150 - int(value / 2)))

        anim.valueChanged.connect(update_glow)
        anim.finished.connect(lambda: widget.setGraphicsEffect(None))
        anim.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        self._anim = anim


# --- WELCOME WINDOW (manages logout and returns to MainWindow) ---
class WelcomeWindow(QtWidgets.QWidget):
    def __init__(self, username: str):
        super().__init__()
        self.ui = Ui_WelcomeForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Welcome - Entrepredict")

        # show username if label exists
        if hasattr(self.ui, "label_username"):
            # show just the username (the header already has "Welcome!")
            self.ui.label_username.setText(username)

        # Connect logout button (object name: pushButton_6 in the WELCOME UI)
        if hasattr(self.ui, "pushButton_6"):
            self.ui.pushButton_6.clicked.connect(self.handle_logout)

        # keep a reference for re-opening main
        self._reopened_main = None

        print(f"🎉 Welcome window opened for: {username}")

    def handle_logout(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Log Out",
            "Do you want to log out?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            # Create and show a fresh MainWindow (so login logic + animations are available)
            self._reopened_main = MainWindow()
            self._reopened_main.show()
            # Close the welcome window
            self.close()


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    init_database()
    w = MainWindow()
    w.show()
    app.exec()
