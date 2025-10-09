import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QTableView, QLineEdit, QLabel, QInputDialog,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import QSortFilterProxyModel, Qt, QEvent, QTimer


def init_db():
    """Initialize SQLite database with extended products table"""
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            original_price REAL,
            retail_price REAL,
            stocks INTEGER
        )
    """)
    conn.commit()
    conn.close()


class ProductApp(QWidget):
    def __init__(self):
        super().__init__()

        # --- Window (fixed size) ---
        self.setWindowTitle("Product Manager")
        self.setFixedSize(800, 500)

        # internal guard to suppress validation during programmatic updates
        self._suspend_validation = False

        # --- Styles ---
        self.setStyleSheet("""
            QWidget { background-color: #f5f7fa; font-family: Segoe UI, sans-serif; font-size: 13px; }
            QPushButton {
                background-color: #4a90e2; color: white; border-radius: 8px;
                padding: 8px 12px; font-weight: 600;
            }
            QPushButton:hover { background-color: #357ABD; }
            QLineEdit {
                padding: 6px 10px; border: 1px solid #d0d7de; border-radius: 8px; background: white;
            }
            QTableView {
                border: 1px solid #d0d7de; border-radius: 8px;
                gridline-color: #cfd6dc; selection-background-color: #4a90e2;
                selection-color: white; background: white; alternate-background-color: #f8fafc;
            }
            QHeaderView::section {
                background-color: #e9eff6; padding: 6px; border: 1px solid #cfd6dc; font-weight: 700;
            }
        """)

        # --- DB connect ---
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("products.db")
        if not self.db.open():
            QMessageBox.critical(self, "DB Error", self.db.lastError().text())
            sys.exit(1)

        # --- Model (source) ---
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("products")
        # Use manual submit so we control validation and commit timing
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()

        # header labels
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Product Name")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Original Price")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Retail Price")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Stocks")

        # connect validation handler to model.dataChanged so we can intercept edits
        self.model.dataChanged.connect(self.on_data_changed)

        # --- Proxy model for search filtering ---
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(1)  # filter by Product Name

        # --- Table view ---
        self.view = QTableView()
        self.view.setModel(self.proxy)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.view.verticalHeader().setVisible(False)
        self.view.setShowGrid(True)
        self.view.setColumnHidden(0, True)  # hide ID column

        # fix table size inside window
        self.view.setFixedSize(760, 340)

        # prevent horizontal scrollbar (we compute exact-fit)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Lock header resize mode to Fixed
        header = self.view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Calculate widths after the widget is shown (ensure viewport has proper width)
        QTimer.singleShot(0, self.apply_fixed_column_widths)

        # Recalculate widths when viewport resizes or scrollbar range changes
        self.view.viewport().installEventFilter(self)
        self.view.verticalScrollBar().rangeChanged.connect(lambda *args: self.apply_fixed_column_widths())

        # --- Search bar ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search product...")
        self.search_bar.setFixedWidth(260)
        # filter string must be set on proxy model; keep it simple (exact match substring)
        self.search_bar.textChanged.connect(self.proxy.setFilterFixedString)

        # --- Buttons ---
        self.btn_add = QPushButton("➕ Add Product")
        self.btn_delete = QPushButton("🗑 Delete Selected")
        self.btn_add.clicked.connect(self.add_product)
        self.btn_delete.clicked.connect(self.delete_product)

        # --- Layouts ---
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 16, 20, 16)

        # top bar (search aligned right)
        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        top_bar.addWidget(QLabel("Search:"))
        top_bar.addSpacing(6)
        top_bar.addWidget(self.search_bar)

        main_layout.addLayout(top_bar)
        main_layout.addSpacing(8)
        main_layout.addWidget(self.view, 0, Qt.AlignmentFlag.AlignCenter)

        # buttons row (centered)
        btn_bar = QHBoxLayout()
        btn_bar.addStretch(1)
        btn_bar.addWidget(self.btn_add)
        btn_bar.addSpacing(12)
        btn_bar.addWidget(self.btn_delete)
        btn_bar.addStretch(1)

        main_layout.addSpacing(10)
        main_layout.addLayout(btn_bar)

        self.setLayout(main_layout)

    def eventFilter(self, obj, ev):
        # watch viewport resize events and reapply widths
        if obj is self.view.viewport() and ev.type() == QEvent.Type.Resize:
            self.apply_fixed_column_widths()
        return super().eventFilter(obj, ev)

    def apply_fixed_column_widths(self):
        """
        Set exact fixed widths for all columns so they fill the table perfectly.
        Called after show and on viewport changes.
        """
        total = self.view.viewport().width()
        if total <= 0:
            total = 760  # fallback

        # Proportions for columns (sum ≈ 1.0). Tweak as desired.
        proportions = [0.45, 0.18, 0.18, 0.19]

        widths = [int(total * p) for p in proportions]
        # make last column absorb rounding errors
        widths[-1] = total - sum(widths[:-1])

        if any(w <= 0 for w in widths):
            widths = [350, 150, 150, 110]

        # Apply widths (column indices in the source model)
        self.view.setColumnWidth(1, widths[0])  # Product Name
        self.view.setColumnWidth(2, widths[1])  # Original Price
        self.view.setColumnWidth(3, widths[2])  # Retail Price
        self.view.setColumnWidth(4, widths[3])  # Stocks

    def refresh_table(self):
        """Reload model and reapply widths. suspend validation while doing this."""
        self._suspend_validation = True
        try:
            self.model.select()
            # reapply widths after select (allow event loop to settle)
            QTimer.singleShot(0, self.apply_fixed_column_widths)
        finally:
            self._suspend_validation = False

    def add_product(self):
        name, ok = QInputDialog.getText(self, "New Product", "Enter product name:")
        if not ok or not name.strip():
            return
        name = name.strip()

        original_price, ok = QInputDialog.getDouble(self, "New Product", "Enter original price:")
        if not ok:
            return

        retail_price, ok = QInputDialog.getDouble(self, "New Product", "Enter retail price:")
        if not ok:
            return

        stocks, ok = QInputDialog.getInt(self, "New Product", "Enter stocks:")
        if not ok:
            return

        # --- Prevent duplicate name (case-insensitive) before insert ---
        lname = name.lower()
        for row in range(self.model.rowCount()):
            existing = str(self.model.data(self.model.index(row, 1)) or "").strip().lower()
            if existing == lname:
                QMessageBox.warning(self, "Duplicate", f"Product '{name}' already exists!")
                return

        # Insert new record into model and commit
        record = self.model.record()
        record.setValue("name", name)
        record.setValue("original_price", original_price)
        record.setValue("retail_price", retail_price)
        record.setValue("stocks", stocks)

        self._suspend_validation = True
        try:
            if not self.model.insertRecord(-1, record):
                QMessageBox.critical(self, "Error", "Failed to add product (insertRecord failed).")
                return
            if not self.model.submitAll():
                QMessageBox.critical(self, "DB Error", self.model.lastError().text())
                self.model.revertAll()
                return
        finally:
            self._suspend_validation = False

        self.refresh_table()

    def delete_product(self):
        """Delete the currently selected row (map proxy -> source)"""
        idx = self.view.currentIndex()
        if not idx.isValid():
            return
        src_idx = self.proxy.mapToSource(idx)
        if not src_idx.isValid():
            return

        self._suspend_validation = True
        try:
            self.model.removeRow(src_idx.row())
            if not self.model.submitAll():
                QMessageBox.critical(self, "DB Error", self.model.lastError().text())
                self.model.revertAll()
                return
        finally:
            self._suspend_validation = False

        self.refresh_table()

    def on_data_changed(self, topLeft, bottomRight, roles):
        """
        Called when the source model data changes (an edit happened).
        Validate name duplicates and then submit changes to DB.
        """
        if self._suspend_validation:
            return

        # We'll suspend validation while we attempt to submit or revert to avoid recursion
        self._suspend_validation = True
        try:
            # Check whether name column (1) is among changed columns
            name_changed = False
            for c in range(topLeft.column(), bottomRight.column() + 1):
                if c == 1:
                    name_changed = True
                    break

            # If name changed, validate duplicates for each changed row
            if name_changed:
                for row in range(topLeft.row(), bottomRight.row() + 1):
                    idx = self.model.index(row, 1)
                    new_name = str(self.model.data(idx) or "").strip()
                    if new_name == "":
                        QMessageBox.warning(self, "Invalid Name", "Product name cannot be empty.")
                        self.model.revertAll()
                        self.refresh_table()
                        return

                    new_name_l = new_name.lower()
                    # scan other rows for duplicate (exclude current row)
                    for r in range(self.model.rowCount()):
                        if r == row:
                            continue
                        other = str(self.model.data(self.model.index(r, 1)) or "").strip().lower()
                        if other == new_name_l:
                            QMessageBox.warning(self, "Duplicate Name",
                                                f"The product name '{new_name}' already exists in the database!")
                            self.model.revertAll()
                            self.refresh_table()
                            return

            # If validation passed, try to commit the change(s)
            if not self.model.submitAll():
                QMessageBox.critical(self, "DB Error", self.model.lastError().text())
                self.model.revertAll()
                self.refresh_table()
                return

            # success — refresh view widths (in case scrollbar changed)
            QTimer.singleShot(0, self.apply_fixed_column_widths)

        finally:
            self._suspend_validation = False


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec())
