# Form implementation generated from reading ui file 'Tutorial.ui'
#
# Perfectly Aligned & Spaced Version – With Proper Justification
# Created by: PyQt6 UI code generator 6.4.2
#

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 640)

        # ===== MAIN BACKGROUND =====
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 940, 640))
        self.widget.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff,
                    stop:0.4 #cbf7ff,
                    stop:1 #a6ecf7
                );
            }
        """)
        self.widget.setObjectName("widget")

        # ===== MAIN CONTAINER =====
        self.mainwidget = QtWidgets.QWidget(parent=self.widget)
        self.mainwidget.setGeometry(QtCore.QRect(0, 0, 940, 640))
        self.mainwidget.setObjectName("mainwidget")

        # ===== TOP BAR =====
        self.label_upperhome = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_upperhome.setGeometry(QtCore.QRect(0, 0, 940, 60))
        self.label_upperhome.setStyleSheet("background-color: #031b3d;")
        self.label_upperhome.setText("")
        self.label_upperhome.setObjectName("label_upperhome")

        self.label_smalllogo = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_smalllogo.setGeometry(QtCore.QRect(10, 0, 50, 60))
        self.label_smalllogo.setStyleSheet("""
            background-color: #031b3d;
            border-image: url("C:/Users/USER/Documents/system_90/nagao_backend/ENTREPREDICT_Icon_Option_1_-_Circuit-Graph_E-removebg-preview.png");
        """)
        self.label_smalllogo.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_smalllogo.setText("")
        self.label_smalllogo.setObjectName("label_smalllogo")

        # ===== TITLE =====
        self.text_title = QtWidgets.QTextEdit(parent=self.mainwidget)
        self.text_title.setGeometry(QtCore.QRect(70, 15, 200, 40))
        self.text_title.setReadOnly(True)
        self.text_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_title.setStyleSheet("""
            QTextEdit {
                font-family: "Montserrat ExtraBold";
                font-size: 16pt;
                font-weight: 600;
                color: white;
                background-color: #031b3d;
                border: none;
            }
        """)
        self.text_title.setObjectName("text_title")

        # ===== LABEL STYLE =====
        label_style = """
            color: #031b3d;
            font-weight: 700;
            font-size: 15px;
            background: transparent;
            text-shadow: 0px 0px 6px #00ffff;
        """

        # ===== LABELS =====
        self.label_home = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_home.setGeometry(QtCore.QRect(30, 80, 160, 25))
        self.label_home.setStyleSheet(label_style)
        self.label_home.setObjectName("label_home")

        self.label_stats = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_stats.setGeometry(QtCore.QRect(30, 190, 160, 25))
        self.label_stats.setStyleSheet(label_style)
        self.label_stats.setObjectName("label_stats")

        self.label_predict = QtWidgets.QLabel(parent=self.mainwidget)
        self.label_predict.setGeometry(QtCore.QRect(30, 300, 180, 25))
        self.label_predict.setStyleSheet(label_style)
        self.label_predict.setObjectName("label_predict")

        # ===== TEXT STYLE =====
        text_style = """
            font-family: "Poppins";
            font-size: 11pt;
            font-weight: 500;
            color: #002B5B;
            background-color: transparent;
            border: none;
        """

        # ===== HOME DESCRIPTION =====
        self.home_des = QtWidgets.QTextEdit(parent=self.mainwidget)
        self.home_des.setGeometry(QtCore.QRect(30, 110, 550, 60))
        self.home_des.setReadOnly(True)
        self.home_des.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        self.home_des.setStyleSheet(text_style)
        self.home_des.setObjectName("home_des")

        # ===== STATISTICS DESCRIPTION =====
        self.statistics_des = QtWidgets.QTextEdit(parent=self.mainwidget)
        self.statistics_des.setGeometry(QtCore.QRect(30, 220, 550, 60))
        self.statistics_des.setReadOnly(True)
        self.statistics_des.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        self.statistics_des.setStyleSheet(text_style)
        self.statistics_des.setObjectName("statistics_des")

        # ===== PREDICTION DESCRIPTION 1 =====
        self.prediction_des1 = QtWidgets.QTextEdit(parent=self.mainwidget)
        self.prediction_des1.setGeometry(QtCore.QRect(30, 330, 550, 100))
        self.prediction_des1.setReadOnly(True)
        self.prediction_des1.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        self.prediction_des1.setStyleSheet(text_style)
        self.prediction_des1.setObjectName("prediction_des1")

        # ===== PREDICTION DESCRIPTION 2 =====
        self.prediction_des2 = QtWidgets.QTextEdit(parent=self.mainwidget)
        self.prediction_des2.setGeometry(QtCore.QRect(30, 420, 550, 140))
        self.prediction_des2.setReadOnly(True)
        self.prediction_des2.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        self.prediction_des2.setStyleSheet(text_style)
        self.prediction_des2.setObjectName("prediction_des2")

        # ===== FINAL SETUP =====
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # ===== TRANSLATE TEXTS =====
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Tutorial"))

        self.text_title.setPlainText(_translate("Form", "HOW TO USE"))
        self.label_home.setText(_translate("Form", "HOME TAB:"))
        self.label_stats.setText(_translate("Form", "STATISTICS TAB:"))
        self.label_predict.setText(_translate("Form", "PREDICTION TAB:"))

        self.home_des.setPlainText(_translate("Form",
            "On the Home page, you can see your latest business result and some helpful tips."
        ))

        self.statistics_des.setPlainText(_translate("Form",
            "In the Stats tab, upload a file with expense, income, and liabilities to see a graph of your financial data."
        ))

        self.prediction_des1.setPlainText(_translate("Form",
            "Users can drag and drop a CSV or Excel file that includes seven key financial data: "
            "Total Assets, Total Liabilities, Total Equity, Net Income, Operating Income, "
            "Current Assets, and Current Liabilities. The system automatically reads and fills "
            "these values, or users can type them manually."
        ))

        self.prediction_des2.setPlainText(_translate("Form",
            "If the Starting Date is left empty, the system predicts only the current business status. "
            "But if a date is entered, the system analyzes all financial records that were previously "
            "entered during and after that date, predicting both the current and future performance "
            "of the business. After clicking 'Predict,' the result shows whether the business is "
            "successful or at risk (bankrupt) based on the analysis."
        ))


# ===== RUN APP =====
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
