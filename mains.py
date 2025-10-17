import sqlite3, os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import re
import joblib
from datetime import datetime
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QPoint, Qt, QSortFilterProxyModel, QEvent, QTimer
from PyQt6.QtWidgets import QVBoxLayout, QTableView, QComboBox, QStyledItemDelegate, QGraphicsDropShadowEffect, QMessageBox, QInputDialog, QHeaderView, QAbstractItemView
from PyQt6.QtGui import QColor, QStandardItemModel, QStandardItem
from ENTREPREDICT import Ui_Form
from CREATE import Ui_Form as Ui_CreateForm
from Final import Ui_Form as FinalInterfaceForm  # Welcome UI import
from reportPopUp import Ui_Form as ReportPopUpForm

#DataNeeded_Prediction = ['totalassets', 'totalliabilities', 'totalequity', 'netincome', 'operatingincome', 'currentassets', 'currentliabilities']
#DataNeeded_Graph = ['expense', 'income', 'liabilities']
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

def safe_filename(name: str) -> str:
    """Convert a name to a safe filename for DB."""
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name.strip())

def init_prediction_db(username: str) -> str:
    db_name = f"prediction_{safe_filename(username)}.db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, 
            status TEXT,
            probability REAL,
            tips_1 TEXT,
            tips_2 TEXT,
            tips_3 TEXT,
            tips_4 TEXT,
            tips_5 TEXT
        )
    """)
    conn.commit()
    conn.close()
    return db_name


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
        self.center_on_screen()    
        # Connect create button
        self.ui.pushButton_login.clicked.connect(self.create_account)
        print("✅ Create Account page loaded!")

    def center_on_screen(self):
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

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

        self.center_on_screen()
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

        # Connect signals$
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

    def center_on_screen(self):
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())
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
        self.ui = FinalInterfaceForm()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Welcome - {username}")
        self.username = username

        self.center_on_screen()

        # Initialize per-user DB
        self.prediction_db_name = init_prediction_db(self.username)

        self.load_latest_prediction()
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_widget)
        
        # Display username if label exists^
        if hasattr(self.ui, "label_username"):
            self.ui.label_username.setText(self.username)

        self.button_widget_map = {
            self.ui.homePushButton: self.ui.home_widget,
            
            self.ui.statsPushButton: self.ui.stats_widget,
            self.ui.predictionPushButton: self.ui.prediction_widget,
            
        }
        # Store default styles to restore later
        self.default_styles = {btn: btn.styleSheet() for btn in self.button_widget_map.keys()}
        self.button_original_pos = {btn: btn.pos() for btn in self.button_widget_map.keys()}
        self.active_button = None

        # Connect nav buttons
        for btn, widget in self.button_widget_map.items():
            btn.clicked.connect(lambda checked=False, b=btn, w=widget: self.handle_nav(b, w))

        # Logout
        if hasattr(self.ui, "logOutPushButton"):
            self.ui.logOutPushButton.clicked.connect(self.handle_logout)

        # Modernize inventory table UI
        
        if hasattr(self.ui, "predictButton"):
            self.ui.predictButton.clicked.connect(self.handle_prediction)
        
                # --- CSV Drag & Drop for Prediction Inputs ---
        if hasattr(self.ui, "csvLabelDropPredict"):
            self.ui.csvLabelDropPredict.setAcceptDrops(True)
            self.ui.csvLabelDropPredict.setText("Drag and Drop Prediction CSV Here")
            self.ui.csvLabelDropPredict.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            # Attach event handlers dynamically
            self.ui.csvLabelDropPredict.dragEnterEvent = self.dragEnterEvent
            self.ui.csvLabelDropPredict.dropEvent = self.dropEvent

        # Columns to extract (normalized for comparison)
        self.DataNeeded_Prediction = [
            'totalassets', 'totalliabilities', 'totalequity',
            'netincome', 'operatingincome', 'currentassets', 'currentliabilities'
        ]

                # --- CSV Drag & Drop for Graph Data ---
        if hasattr(self.ui, "csvLabelDropStats"):
            self.ui.csvLabelDropStats.setAcceptDrops(True)
            self.ui.csvLabelDropStats.setText("Drag CSV File Here")
            self.ui.csvLabelDropStats.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            

            self.ui.csvLabelDropStats.dragEnterEvent = self.dragEnterEvent
            self.ui.csvLabelDropStats.dropEvent = self.dropEventGraph

        self.DataNeeded_Graph = ['expense', 'income', 'liabilities']

        # Initialize DB for storing graph data
        self.init_graph_db()
        self.load_graph_files()

        # Connect graph button
        if hasattr(self.ui, "graphPushButton"):
            self.ui.graphPushButton.clicked.connect(self.display_graph)

    def center_on_screen(self):
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


    def load_graph_files(self):
        """Load previously saved CSV filenames into the combo box."""
        if not hasattr(self.ui, "statsComboBox"):
            return

        conn = sqlite3.connect(self.graph_db)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT filename FROM graph_data WHERE username = ?", (self.username,))
        files = [row[0] for row in cur.fetchall()]
        conn.close()

        self.ui.statsComboBox.clear()
        self.ui.statsComboBox.addItems(files)

    def init_graph_db(self):
        import sqlite3
        self.graph_db = f"{self.username}_graph_data.db"
        conn = sqlite3.connect(self.graph_db)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS graph_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                filename TEXT,
                expense REAL,
                netincome REAL,
                liabilities REAL
            )
        """)
        conn.commit()
        conn.close()
        return self.graph_db

    def dropEventGraph(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".csv"):
                self.process_graph_csv(file_path)
            else:
                self.ui.csvLabelDropStats.setText("❌ Invalid file! Please drop a .csv file.")
    
    def process_graph_csv(self, file_path: str):
        
        try:
            df = pd.read_csv(file_path)
            headers = list(df.columns)

            # Clean headers
            header_map = {self.clean_header(h): h for h in headers}

            # Needed data (allow "net income" column)
            DataNeeded_Graph = ['expense', 'netincome', 'liabilities']

            # Match headers
            matched = {}
            for needed in DataNeeded_Graph:
                for cleaned, original in header_map.items():
                    if cleaned == needed:
                        matched[needed] = original
                        break

            if not matched:
                self.ui.csvLabelDropStats.setText("⚠️ No matching columns found.")
                return

            row = df.iloc[0] if not df.empty else {}

            # Helper for safety
            def safe_get(key):
                if key in matched:
                    val = row.get(matched[key], None)
                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        return "N/A"
                return "N/A"

            expense = safe_get('expense')
            netincome = safe_get('netincome')
            liabilities = safe_get('liabilities')

            # Convert "N/A" to 0 for DB
            def to_num(v): return 0 if v == "N/A" else v

            conn = sqlite3.connect(self.graph_db)
            cur = conn.cursor()

            # ✅ Map netincome → income if your DB still uses 'income' column
            cur.execute("""
                INSERT INTO graph_data (username, filename, expense, netincome, liabilities)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.username,
                os.path.basename(file_path),
                to_num(expense),
                to_num(netincome),  # notice this maps netincome → income
                to_num(liabilities)
            ))
            conn.commit()
            conn.close()

            self.load_graph_files()
            self.ui.csvLabelDropStats.setText(f"✅ Saved: {os.path.basename(file_path)}")

        except Exception as e:
            self.ui.csvLabelDropStats.setText(f"⚠️ Error loading CSV: {e}")

    def display_graph(self):
        selected_file = self.ui.statsComboBox.currentText()
        if not selected_file:
            self.ui.csvLabelDropStats.setText("⚠️ Select a file from the combo box.")
            return

        conn = sqlite3.connect(self.graph_db)
        cur = conn.cursor()
        cur.execute("""
            SELECT expense, netincome, liabilities 
            FROM graph_data
            WHERE username = ? AND filename = ?
        """, (self.username, selected_file))
        result = cur.fetchone()
        conn.close()

        if not result:
            self.ui.csvLabelDropStats.setText("⚠️ No data found for that file.")
            return

        expense, netincome, liabilities = result  # 👈 changed here

        # Convert safely to numeric
        def safe_value(v):
            if v is None:
                return 0
            try:
                return float(v)
            except (ValueError, TypeError):
                return 0

        expense_val = safe_value(expense)
        netincome_val = safe_value(netincome)
        liabilities_val = safe_value(liabilities)

        categories = ['Expense', 'Net Income', 'Liabilities']  # 👈 label changed
        values = [expense_val, netincome_val, liabilities_val]


        # Labels shown *inside* bars
        def label_text(v):
            if v is None or v == 0:
                return "N/A"
            return str(v)

        display_texts = [label_text(expense), label_text(netincome), label_text(liabilities)]

        # --- Colors (gray for missing) ---
        colors = []
        for v in [expense, netincome, liabilities]:
            if v is None or v == 0 or v == "N/A":
                colors.append('#B0BEC5')  # gray for N/A
            else:
                colors.append('#66bb6a' if v == netincome else '#ef5350' if v == expense else '#42a5f5')

        # --- Ensure layout exists ---
        layout = self.ui.graphFrame.layout()
        if layout is None:
            layout = QtWidgets.QVBoxLayout(self.ui.graphFrame)
            self.ui.graphFrame.setLayout(layout)

        # Clear old graph
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # --- Create Matplotlib Figure ---
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        bars = ax.bar(categories, values, color=colors)

        for bar, value, color in zip(bars, values, colors):
            height = bar.get_height()

            # Handle invalid or missing values safely
            if not isinstance(value, (int, float)):
                value = 0
            if value is None:
                value = 0

            # Determine text color for contrast
            text_color = "black" if color == '#B0BEC5' else "white"

            # Display logic
            if value == 0:
                # Show 0 above the bar
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + (max(values) * 0.05 if max(values) > 0 else 0.2),
                    "0",
                    ha='center',
                    va='bottom',
                    fontsize=11,
                    fontweight='bold',
                    color='black'  # always black for visibility
                )
            else:
                # Show value inside the bar
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height / 2,
                    f"{value:.2f}".rstrip('0').rstrip('.'),  # clean numeric formatting
                    ha='center',
                    va='center',
                    fontsize=11,
                    fontweight='bold',
                    color=text_color
                )
   
        ax.set_xlabel("Business Data", fontsize=12, fontweight='bold')
        ax.set_ylabel("Value", fontsize=12, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.tight_layout()

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def clean_header(self, header_name: str) -> str:
        return re.sub(r'[^a-z0-9]', '', header_name.lower())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".csv"):
                self.process_csv(file_path)
            else:
                self.ui.csvLabelDropPredict.setText("❌ Invalid file! Please drop a .csv file.")

    def process_csv(self, file_path: str):
        import pandas as pd
        import os

        try:
            df = pd.read_csv(file_path)
            headers = list(df.columns)

            # Clean headers
            header_map = {self.clean_header(h): h for h in headers}

            # Match headers to needed ones
            matched = {}
            for needed in self.DataNeeded_Prediction:
                for cleaned, original in header_map.items():
                    if cleaned == needed:
                        matched[needed] = original
                        break

            if not matched:
                self.ui.csvLabelDropPredict.setText("⚠️ No matching columns found.")
                return

            # Use the first row (assuming it's the latest/only entry)
            row = df.iloc[0]

            # Fill each QLineEdit if available
            def set_if_exists(attr, value):
                if hasattr(self.ui, attr):
                    getattr(self.ui, attr).setText(str(value))

            # Assign values
            set_if_exists("totalAssetsQLine", row.get(matched.get("totalassets", ""), ""))
            set_if_exists("totalLiabilitiesQLine", row.get(matched.get("totalliabilities", ""), ""))
            set_if_exists("totalEquityQLine", row.get(matched.get("totalequity", ""), ""))
            set_if_exists("netIncomeQLine", row.get(matched.get("netincome", ""), ""))
            set_if_exists("operatingIncomeQLine", row.get(matched.get("operatingincome", ""), ""))
            set_if_exists("currentAssetsQLine", row.get(matched.get("currentassets", ""), ""))
            set_if_exists("currentLiabilitiesQLine", row.get(matched.get("currentliabilities", ""), ""))

            # Update label
            self.ui.csvLabelDropPredict.setText(f"✅ Loaded: {os.path.basename(file_path)}")

        except Exception as e:
            self.ui.csvLabelDropPredict.setText(f"⚠️ Error loading CSV: {e}")

    # ----------------------
    # Load latest prediction for home widget
    # ----------------------
    def load_latest_prediction(self):
        """Load the latest prediction and its 5 tips from the user's database."""
        try:
            conn = sqlite3.connect(self.prediction_db_name)
            cur = conn.cursor()

            # Get the most recent prediction (with tips)
            cur.execute("""
                SELECT date, status, probability, tips_1, tips_2, tips_3, tips_4, tips_5
                FROM predictions
                ORDER BY id DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            conn.close()

            # If no record found
            if not row:
                if hasattr(self.ui, "label_last"):
                    self.ui.label_last.setText("No previous prediction.")
                return

            # Unpack the data
            date, status, probability, tip1, tip2, tip3, tip4, tip5 = row

            # Display prediction info
            if hasattr(self.ui, "label_last"):
                self.ui.label_last.setText(f"Last Prediction: {date}")

            if hasattr(self.ui, "label_predicted"):
                self.ui.label_predicted.setText(status)
                if status.lower() == "bankrupt !":
                    self.ui.label_predicted.setStyleSheet("""
                        #label_predicted {
                            font-size: 24pt;      
                            font-weight: bold;
                            color: #eb152e;       
                            background: transparent;
                        }
                    """)
                else:
                    self.ui.label_predicted.setStyleSheet("""
                        #label_predicted {
                            font-size: 24pt;      
                            font-weight: bold;
                            color: #14e314;       
                            background: transparent;
                        }
                    """)

            if hasattr(self.ui, "label_confidence"):
                self.ui.label_confidence.setText(f"{probability}")

            # Display saved tips (if labels exist)
            tips_labels = [
                getattr(self.ui, f"tipsLabelH_{i}", None)
                for i in range(1, 6)
            ]
            saved_tips = [f"• {tip1}", f"• {tip2}", f"• {tip3}", f"• {tip4}", f"• {tip5}"]

            for label, tip in zip(tips_labels, saved_tips):
                if label is not None:
                    label.setText(tip if tip else "—")

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load previous prediction:\n{e}")



    # ----------------------
    # Prediction Tips
    # ----------------------
    def generate_tips(self, ratios, status_text):
        """Generate up to 15 short business tips based on computed ratios."""
        tips = []

        # --- Liquidity (Current Ratio) ---
        current_ratio = ratios["Current Ratio"]
        if current_ratio < 1.0:
            tips.append("Low liquidity: Add more cash or reduce short-term debts.")
        elif 1.0 <= current_ratio <= 3.0:
            tips.append("Good liquidity: Balance looks fine — keep it steady.")
        else:
            tips.append("High liquidity: Too much idle cash — use it to grow.")

        # --- Debt (Debt-to-Equity Ratio) ---
        debt_to_equity = ratios["Debt ratio %"] / (100 - ratios["Debt ratio %"] + 1e-6)
        if debt_to_equity > 2.0:
            tips.append("High debt: Pay down loans to lower risk.")
        elif 0.5 <= debt_to_equity <= 2.0:
            tips.append("Balanced debt: Debt level is healthy — maintain it.")
        else:
            tips.append("Low debt: Safe, but small loans could help growth.")

        # --- Profitability (ROA and ROE) ---
        roa = ratios["ROA(A) before interest and % after tax"]
        roe = ratios["Net Income to Stockholder's Equity"]

        if roa < 0.05:
            tips.append("Low ROA: Use assets better to raise profit.")
        else:
            tips.append("Good ROA: Assets are producing solid profit.")

        if roe < 0.10:
            tips.append("Low ROE: Grow sales or reduce costs.")
        elif roe > 0.15:
            tips.append("High ROE: Great return — keep it up.")
        else:
            tips.append("Balanced ROE: Earnings are steady — maintain performance.")

        # --- Operations (Operating Margin using Operating/Net Income ratio as proxy) ---
        op_margin = ratios["ROA(C) before interest and depreciation before interest"]
        if op_margin < 0.05:
            tips.append("Low margin: Cut costs or boost income.")
        elif 0.05 <= op_margin <= 0.20:
            tips.append("Good margin: Operations running well.")
        else:
            tips.append("High margin: Excellent — keep improving.")

        # --- Overall Health (based on combined strength) ---
        strong = sum([
            current_ratio >= 1.0,
            0.5 <= debt_to_equity <= 2.0,
            roa >= 0.05,
            roe >= 0.10,
            op_margin >= 0.05
        ])

        if strong >= 4:
            tips.append("🌟 Strong overall: Business is solid — keep growing.")
        elif strong >= 2:
            tips.append("⚠️ Weak areas: Focus on lowering debt and raising profit.")
        else:
            tips.append("❗ Unstable: Review all key financial areas.")

        # --- Ensure 15 tips total (duplicate general reminders if fewer) ---
        while len(tips) < 15:
            tips.append("💡 Keep reviewing finances monthly to stay stable.")

        return tips[:15]




    # ----------------------
    # Prediction
    # ----------------------
    def compute_ratios(self, raw):
        """Compute financial ratios from raw inputs."""
        data = {}
        data["ROA(C) before interest and depreciation before interest"] = raw["Operating_Income"] / raw["Total_Assets"]
        data["ROA(A) before interest and % after tax"] = raw["Net_Income"] / raw["Total_Assets"]
        data["Net Income to Stockholder's Equity"] = raw["Net_Income"] / raw["Total_Equity"]
        data["Current Ratio"] = raw["Current_Assets"] / raw["Current_Liabilities"]
        data["Quick Ratio"] = (raw["Current_Assets"] - (raw["Current_Assets"] * 0.3)) / raw["Current_Liabilities"]
        data["Debt ratio %"] = (raw["Total_Liabilities"] / raw["Total_Assets"]) * 100
        data["Interest Coverage Ratio (Interest expense to EBIT)"] = raw["Operating_Income"] / (0.1 * raw["Total_Liabilities"])
        return pd.DataFrame([data])
    
    def handle_prediction(self):
        try:
            raw_input = {
                "Total_Assets": float(self.ui.totalAssetsQLine.text()),
                "Total_Liabilities": float(self.ui.totalLiabilitiesQLine.text()),
                "Total_Equity": float(self.ui.totalEquityQLine.text()),
                "Net_Income": float(self.ui.netIncomeQLine.text()),
                "Operating_Income": float(self.ui.operatingIncomeQLine.text()),
                "Current_Assets": float(self.ui.currentAssetsQLine.text()),
                "Current_Liabilities": float(self.ui.currentLiabilitiesQLine.text())
            }
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values in all fields.")
            return

        # 1️⃣ Compute ratios
        df_input = self.compute_ratios(raw_input)
        ratios = df_input.iloc[0].to_dict()

        # 2️⃣ Load model
        model = joblib.load("bankruptcy_Simple.pkl")
        df_input = df_input[model.feature_names_in_]

        # 3️⃣ Predict
        prediction = model.predict(df_input)[0]
        proba = model.predict_proba(df_input)[0]
        prob_bankrupt = proba[1] * 100
        prob_healthy = proba[0] * 100
        limiter = 45.0

        # 4️⃣ Determine status
        if prob_bankrupt > limiter:
            status_text = "Bankrupt !"
            self.ui.result_label.setStyleSheet("""
                #result_label {
                    color: red; font-weight: 900; font-size: 22px;
                    text-shadow: 0px 0px 6px #ff4d4d;
                }
            """)
            probability = f"Confidence: {prob_bankrupt:.2f}%"
            message_text = "⚠️ Your Business is at\nrisk for bankruptcy"
        else:
            status_text = "Healthy !"
            self.ui.result_label.setStyleSheet("""
                #result_label {
                    color: green; font-weight: 900; font-size: 22px;
                    text-shadow: 0px 0px 6px #00ff99;
                }
            """)
            probability = f"Confidence: {prob_healthy:.2f}%"
            message_text = "✅ Your business seems healthy,\nkeep it up!"

        # 5️⃣ Generate financial tips (based on ratios and status)
        tips = self.generate_tips(ratios, status_text)

        # Ensure exactly 5 tips (padding if fewer)
        tips = (tips + [""] * 5)[:5]

        # 6️⃣ Update UI
        self.ui.result_label.setText(status_text)
        self.ui.percentage_label.setText(probability)
        self.ui.message_label.setText(message_text)

        for i, tip in enumerate(tips, start=1):
            label = getattr(self.ui, f"tipsLabel_{i}", None)
            if label:
                label.setText(f"• {tip}")

        # 7️⃣ Save prediction + tips to database
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = sqlite3.connect(self.prediction_db_name)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO predictions (
                    date, status, probability,
                    tips_1, tips_2, tips_3, tips_4, tips_5
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                current_time, status_text, probability,
                tips[0], tips[1], tips[2], tips[3], tips[4]
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to insert prediction data:\n{e}")



    # --- HANDLE NAVIGATION ---
    def handle_nav(self, button, widget):
        # Restore previous button's position and style
        if self.active_button and self.active_button != button:
            self.active_button.move(self.button_original_pos[self.active_button])
            self.restore_default_style(self.active_button)

        # Highlight current button
        self.highlight_button(button)
        self.active_button = button

        # Shift current button slightly left
        offset = -10  # move left by 10 pixels
        button.move(self.button_original_pos[button].x() + offset,
                    self.button_original_pos[button].y())

        # Switch stacked widget page
        if hasattr(self.ui, "stackedWidget"):
            self.ui.stackedWidget.setCurrentWidget(widget)
            print(f"📄 Switched to: {widget.objectName()}")


    # --- HIGHLIGHT ACTIVE BUTTON ---
    def highlight_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0078D4, stop:1 #00B4DB
                );
                color: white;
                font-weight: bold;
                border-radius: 10px;
            }
        """)

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(25)
        glow.setColor(QColor("#00B4DB"))
        glow.setOffset(0, 0)
        button.setGraphicsEffect(glow)

    # --- RESTORE ORIGINAL STYLE ---
    def restore_default_style(self, button):
        original = self.default_styles.get(button, "")
        button.setStyleSheet(original)
        button.setGraphicsEffect(None)

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
