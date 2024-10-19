import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
from qasync import QEventLoop, asyncSlot
from screen_shoot import ScreenCapture

class CaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("截图窗口")
        self.setGeometry(100, 100, 600, 200)

        self.screen_capture = ScreenCapture()

        self.create_capture_page()

    def create_capture_page(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.capture_button = QPushButton("截图")
        self.capture_button.clicked.connect(self.take_screenshot)
        button_layout.addWidget(self.capture_button)

        self.start_button = QPushButton("持续截图")
        self.start_button.clicked.connect(self.toggle_screenshot)
        button_layout.addWidget(self.start_button)

        layout.addLayout(button_layout)

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setText("翻译结果将在这里显示")
        layout.addWidget(self.text_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.take_screenshot)
        self.timer.setInterval(1000)

    @asyncSlot()
    async def take_screenshot(self):
        await self.screen_capture.process_capture()
        result = self.screen_capture.translate
        self.text_box.setText(result)

    def toggle_screenshot(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("持续截图")
        else:
            self.timer.start()
            self.start_button.setText("停止截图")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = CaptureWindow()
    window.show()

    with loop:
        loop.run_forever()
