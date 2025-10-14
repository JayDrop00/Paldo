import sqlite3, os
import pandas as pd
import joblib
from datetime import datetime
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QPoint, Qt, QSortFilterProxyModel, QEvent, QTimer
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QMessageBox, QInputDialog, QHeaderView, QAbstractItemView
from PyQt6.QtGui import QColor
from ENTREPREDICT import Ui_Form
from CREATE import Ui_Form as Ui_CreateForm
from FinalInterface import Ui_Form as FinalInterfaceForm  # Welcome UI import



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

# -----------------------------
# Per-user inventory DB
# -----------------------------
def init_inventory_db(username: str) -> str:
    """Ensure inventory DB exists per user, return DB path."""
    db_name = f"inventory_{safe_filename(username)}.db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            original_price REAL,
            retail_price REAL,
            stocks INTEGER
        )
    """)
    conn.commit()
    conn.close()
    return db_name

def init_prediction_db(username: str) -> str:
    db_name = f"prediction_{safe_filename(username)}.db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, 
            status TEXT,
            probability REAL
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

        # Initialize per-user DB
        self.db_name = init_inventory_db(self.username)
        self.setup_inventory_model()
        self.prediction_db_name = init_prediction_db(self.username)

        self.load_latest_prediction()
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_widget)
        

        # Display username if label exists^
        if hasattr(self.ui, "label_username"):
            self.ui.label_username.setText(self.username)

        
        self.button_widget_map = {
            self.ui.homePushButton: self.ui.home_widget,
            self.ui.inventoryPushButton: self.ui.inventory_widget,
            self.ui.salesPushButton: self.ui.sales_widget,
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
        self.setup_inventory_table_ui()

        if hasattr(self.ui, "predictButton"):
            self.ui.predictButton.clicked.connect(self.handle_prediction)

    

    # ----------------------
    # Load latest prediction for home widget
    # ----------------------
    def load_latest_prediction(self):
        """Load the latest prediction from the user's prediction database."""
        try:
            conn = sqlite3.connect(self.prediction_db_name)
            cur = conn.cursor()

            # Get the most recent prediction (by latest id or date)
            cur.execute("""
                SELECT date, status, probability 
                FROM predictions 
                ORDER BY id DESC 
                LIMIT 1
            """)
            row = cur.fetchone()
            conn.close()

            # If no prediction record exists
            if not row:
                if hasattr(self.ui, "label_last"):
                    self.ui.label_last.setText("No previous prediction.")
                return

            # Otherwise, unpack the data
            date, status, probability = row

            # Update labels if they exist in the UI
            if hasattr(self.ui, "label_last"):
                self.ui.label_last.setText(f"Last Prediction: {date}")
            if hasattr(self.ui, "label_predicted"):
                self.ui.label_predicted.setText(f"Status: {status}")
                if status.lower() == "bankrupt !":
                    self.ui.label_predicted.setStyleSheet('''#label_predicted {
                    font-size: 36pt;      
                    font-weight: bold;
                    color: #eb152e;       
                    background: transparent;
                    }
                    ''')
                else:
                    self.ui.label_predicted.setStyleSheet('''#label_predicted {
                    font-size: 36pt;      
                    font-weight: bold;
                    color: #14e314;       
                    background: transparent;
                    }
                    ''')


            if hasattr(self.ui, "label_confidence"):
                self.ui.label_confidence.setText(f"{probability}")

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load previous prediction:\n{e}")




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
            # 1️⃣ Get numeric values from input fields
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
            return  # ⛔ Stop immediately if invalid

        # 2️⃣ Compute ratios
        df_input = self.compute_ratios(raw_input)

        # 3️⃣ Load model
        model = joblib.load("bankruptcy_Simple.pkl")

        # 4️⃣ Ensure same order as training
        df_input = df_input[model.feature_names_in_]

        # 5️⃣ Make prediction
        prediction = model.predict(df_input)[0]
        proba = model.predict_proba(df_input)[0]
        prob_bankrupt = proba[1] * 100
        prob_healthy = proba[0] * 100
        limiter = 45.0

        # 6️⃣ Show results on labels
        if prob_bankrupt > limiter:
            status_text = "Bankrupt !"
            self.ui.result_label.setStyleSheet("""
                #result_label {
                    color: red;
                    font-weight: 900;
                    font-size: 22px;
                    background: transparent;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                    border: none;
                    text-shadow: 0px 0px 6px #ff4d4d; /* red glow */
                }
            """)
            probability = (f"Confidence: {prob_bankrupt}%")
            message_text = "⚠️ Your Business is at\n risk for bankruptcy"
        else:
            status_text = "Healthy !"
            self.ui.result_label.setStyleSheet("""
                #result_label {
                    color: green;
                    font-weight: 900;
                    font-size: 22px;
                    background: transparent;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                    border: none;
                    text-shadow: 0px 0px 6px #00ff99; /* green glow */
                }
            """)
            probability = (f"Confidence: {prob_healthy:.2f}%")
            message_text = "✅ Your business seems healthy,\n keep it up!"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    

        # Update UI labels (make sure they exist in your .ui)
        self.ui.result_label.setText(status_text)
        self.ui.percentage_label.setText(probability)
        self.ui.message_label.setText(message_text)

        try:
            conn = sqlite3.connect(self.prediction_db_name)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO predictions (date, status, probability)
                VALUES (?, ?, ?)
            """, (current_time, status_text, probability))
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to insert prediction data:\n{e}")
            return

            
    


    # -------------------------
    # Inventory DB + QSqlTableModel
    # -------------------------
    def setup_inventory_model(self):
        """Setup QSqlTableModel and proxy for inventory."""
        # Remove previous connection if exists
        if QSqlDatabase.contains("inventory_conn"):
            QSqlDatabase.removeDatabase("inventory_conn")

        self.db = QSqlDatabase.addDatabase("QSQLITE", "inventory_conn")
        self.db.setDatabaseName(self.db_name)
        if not self.db.open():
            QMessageBox.critical(self, "DB Error", self.db.lastError().text())
            return

        # Table model
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("inventory")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()
        # Set headers
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Product Name")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Original Price")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Retail Price")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Stocks")

        # Proxy model for search
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(1)  # Product Name

        # Connect model auto-save
        self.model.dataChanged.connect(self.save_edits)

    # -------------------------
    # Inventory Table UI
    # -------------------------
    def setup_inventory_table_ui(self):
        table = getattr(self.ui, "table_inventory", None)
        if table is None:
            return

        table.setModel(self.proxy)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setSortingEnabled(True)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table.setColumnHidden(0, True)  # Hide ID column
        # Modern style
        table.setStyleSheet("""
            QTableView {
                border: 2px solid #031b3d;
                border-radius: 1px;
                gridline-color: #cfd6dc;
                selection-background-color: #4a90e2;
                selection-color: white;
                background: white;
                alternate-background-color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #e9eff6;
                padding: 6px;
                border: 1px solid #cfd6dc;
                font-weight: 600;
                color: #333;
            }
        """)

        # Connect search bar
        search_bar = getattr(self.ui, "lineEdit_search", None)
        if search_bar:
            search_bar.textChanged.connect(self.proxy.setFilterFixedString)

        # Connect add/delete buttons
        add_btn = getattr(self.ui, "addbutton", None)
        delete_btn = getattr(self.ui, "deletebutton", None)
        if add_btn:
            add_btn.clicked.connect(self.add_product)
        if delete_btn:
            delete_btn.clicked.connect(self.delete_product)

    # -------------------------
    # Add product
    # -------------------------
    def add_product(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Add Product", "Enter Product Name:")
        if not ok or not name.strip():
            return
        name = name.strip()

        orig_price, ok = QtWidgets.QInputDialog.getDouble(self, "Add Product", "Original Price:", 0, 0)
        if not ok:
            return

        retail_price, ok = QtWidgets.QInputDialog.getDouble(self, "Add Product", "Retail Price:", 0, 0)
        if not ok:
            return

        stocks, ok = QtWidgets.QInputDialog.getInt(self, "Add Product", "Stock Quantity:", 0, 0)
        if not ok:
            return

        # Insert record
        record = self.model.record()
        record.setValue("name", name)
        record.setValue("original_price", orig_price)
        record.setValue("retail_price", retail_price)
        record.setValue("stocks", stocks)

        if not self.model.insertRecord(-1, record):
            QMessageBox.warning(self, "Error", "Failed to add product.")
            return
        if not self.model.submitAll():
            QMessageBox.warning(self, "Error", self.model.lastError().text())
            self.model.revertAll()
            return

        self.model.select()

    # -------------------------
    # Delete product
    # -------------------------
    def delete_product(self):
        table = getattr(self.ui, "table_inventory", None)
        if table is None:
            return

        index = table.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Delete", "Select a product to delete.")
            return

        source_index = self.proxy.mapToSource(index)
        row = source_index.row()
        confirm = QMessageBox.question(self, "Delete", "Are you sure you want to delete this product?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.model.removeRow(row)
            if not self.model.submitAll():
                QMessageBox.warning(self, "Error", self.model.lastError().text())
                self.model.revertAll()
                return
            self.model.select()

    # -------------------------
    # Auto-save edits
    # -------------------------
    def save_edits(self):
        if not self.model.submitAll():
            QMessageBox.warning(self, "Error", self.model.lastError().text())
            self.model.revertAll()
        else:
            self.model.select()


    def setup_modern_inventory_table(self):
        table = getattr(self.ui, "table_inventory", None)
        if table is None:
            return

        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setSortingEnabled(True)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setHighlightSections(False)

        table.setStyleSheet("""
            QTableView {
                border: 1px solid #d0d7de;
                border-radius: 8px;
                gridline-color: #cfd6dc;
                selection-background-color: #4a90e2;
                selection-color: white;
                background: white;
                alternate-background-color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #e9eff6;
                padding: 6px;
                border: 1px solid #cfd6dc;
                font-weight: 600;
                color: #333;
            }
        """)

        

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
