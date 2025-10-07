from PyQt6 import QtCore, QtWidgets, QtGui
from ENTREPREDICT import Ui_Form


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

        # Hide login form initially
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

        # Move logo to left
        logo_anim = QtCore.QPropertyAnimation(self.logo, b"pos")
        logo_anim.setDuration(1000)
        logo_anim.setStartValue(self.logo.pos())
        logo_anim.setEndValue(QtCore.QPoint(100, self.logo.pos().y()))
        logo_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)

        # Fade out welcome, entrep, phrase, button
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

        # Fade + slide in login frame
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

    # --- Button actions ---
    def login_action(self):
        print("🖱 Login button clicked!")
        self.glow_effect(self.login_button, "#00e6cc")

    def create_account_action(self):
        print("🖱 Create Account clicked!")
        self.glow_effect(self.create_account_label, "#00e6cc")

    # --- Glow animation that bypasses stylesheet ---
    def glow_effect(self, widget, color="#00ffff"):
        """Make any widget glow temporarily when clicked."""
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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
