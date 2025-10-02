from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QCategoryAxis
from PyQt6.QtCore import Qt
from tryss import Ui_Form   # import your converted UI

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Lock size and center window
        self.lock_and_center_window()

        # Map labels to stacked widget pages
        self.page_map = {
            self.ui.homeLabel: 0,
            self.ui.inventoryLabel: 1,
            self.ui.salesReportLabel: 2,
            self.ui.predictionLabel: 3
        }

        # Connect labels to page switching
        for label, index in self.page_map.items():
            label.mousePressEvent = lambda e, i=index: self.switch_page(i)

        # Initialize first active page
        self.switch_page(0)

        # Insert graph inside salesReportWidget.graphWidget
        self.init_graph()

    def lock_and_center_window(self):
        """Lock window size and center it on screen."""
        # Lock size based on the designed UI size
        self.setFixedSize(self.size())

        # Center window
        screen = QGuiApplication.primaryScreen().availableGeometry()
        center = screen.center()
        frame = self.frameGeometry()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def init_graph(self):
        """Create and embed a multi-line chart into graphWidget."""

        # Income data
        income_series = QLineSeries()
        income_series.setName("Income")
        income_values = [5000, 7000, 8500, 6000, 9000, 10000]
        for i, y in enumerate(income_values):
            income_series.append(i, y)

        # Revenue data
        revenue_series = QLineSeries()
        revenue_series.setName("Revenue")
        revenue_values = [3000, 6000, 7500, 5000, 8000, 9500]
        for i, y in enumerate(revenue_values):
            revenue_series.append(i, y)

        # Create chart
        chart = QChart()
        chart.addSeries(income_series)
        chart.addSeries(revenue_series)
        chart.setTitle("Monthly Income vs Revenue")

        # X-axis: Months
        axis_x = QCategoryAxis()
        axis_x.setTitleText("Month")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        for i, m in enumerate(months):
            axis_x.append(m, i)
        axis_x.setRange(0, len(months) - 1)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        # Y-axis: Peso values
        axis_y = QCategoryAxis()
        axis_y.setTitleText("Amount (₱)")
        step = 2000
        max_val = 12000
        for v in range(0, max_val + step, step):
            axis_y.append(f"₱{v}", v)
        axis_y.setRange(0, max_val)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        # Attach both series
        income_series.attachAxis(axis_x)
        income_series.attachAxis(axis_y)
        revenue_series.attachAxis(axis_x)
        revenue_series.attachAxis(axis_y)

        # Legend setup
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)

        # Chart view
        chart_view = QChartView(chart)

        # Put chart inside graphWidget
        layout = QVBoxLayout(self.ui.graphWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(chart_view)

    def switch_page(self, index: int):
        """Switch stackedWidget page and update label background."""
        self.ui.stackedWidget.setCurrentIndex(index)

        # Reset all labels
        for label in self.page_map.keys():
            label.setStyleSheet("color: rgb(50, 50, 120); background: none;")
            font = label.font()
            font.setBold(True)
            label.setFont(font)

        # Highlight active label
        active_label = list(self.page_map.keys())[index]
        active_label.setStyleSheet("color: white; background: rgb(50, 50, 120);")
        font = active_label.font()
        font.setBold(True)
        active_label.setFont(font)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    