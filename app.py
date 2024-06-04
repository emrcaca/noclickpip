import sys
import subprocess


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import win32gui
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
    from PyQt5.QtCore import Qt
except ModuleNotFoundError:
    install("pywin32")
    install("PyQt5")
    import win32gui
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
    from PyQt5.QtCore import Qt


class WindowController(QWidget):
    def __init__(self, window_names):
        super().__init__()
        self.window_names = window_names
        self.button_text = "Tıklamayı Devre Dışı Bırak"
        self.setWindowTitle("No Click")
        self.setFixedSize(220, 60)
        self.create_button()

    def create_button(self):
        self.button = QPushButton(self.button_text, self)
        self.button.clicked.connect(self.toggle_window)

        button_width = 150
        button_height = 30
        button_x = (self.width() - button_width) // 2
        button_y = (self.height() - button_height) // 2
        self.button.setGeometry(button_x, button_y, button_width, button_height)

    def toggle_window(self):
        if self.is_window_disabled():
            self.enable_window()
        else:
            self.disable_window()

    def disable_window(self):
        hwnd = self.find_window()
        if hwnd:
            win32gui.EnableWindow(hwnd, False)
            self.button.setText("Tıklamayı Etkinleştir")
        else:
            print("Belirtilen pencere bulunamadı.")

    def enable_window(self):
        hwnd = self.find_window()
        if hwnd:
            win32gui.EnableWindow(hwnd, True)
            self.button.setText("Tıklamayı Devre Dışı Bırak")
        else:
            print("Belirtilen pencere bulunamadı.")

    def is_window_disabled(self):
        hwnd = self.find_window()
        if hwnd:
            return not win32gui.IsWindowEnabled(hwnd)
        else:
            print("Belirtilen pencere bulunamadı.")
            return None

    def find_window(self):
        for name in self.window_names:
            hwnd = win32gui.FindWindow(None, name)
            if hwnd:
                return hwnd
        return None


if __name__ == "__main__":
    window_names = [
        "Pencere içinde pencere",
        "Pencere-içinde-pencere",
        "Resim içinde resim",
        "Resim-içinde-resim",
        "Picture in picture",
        "Picture-in-picture",
    ]
    app = QApplication(sys.argv)
    controller = WindowController(window_names)
    controller.show()
    sys.exit(app.exec_())
