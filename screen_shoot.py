import os
import asyncio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QBuffer
from PIL import Image, ImageChops
from io import BytesIO
from screenshoot_frame import SelectAreaWidget
import sys
from ocr_api.get_tran import GET_TRAN

class ScreenCapture:
    def __init__(self):
        # 在类内部实例化 SelectAreaWidget
        self.select_area_widget = SelectAreaWidget()
        self.screenshot_path = './picture/pict.jpg'
        self.get_tran = GET_TRAN()
        self.translate = ""#翻译文本

    # 截取框内的内容，不保存为文件，直接返回QPixmap
    async def capture_screen(self):
        rect = self.select_area_widget.get_selection_rect()
        screen = QApplication.primaryScreen()
        if not screen:
            print("无法获取屏幕信息")
            return None

        # 使用PyQt5的QScreen来截图，返回 QPixmap
        screenshot = screen.grabWindow(0, rect.left(), rect.top(), rect.width(), rect.height())
        return screenshot

    # 将 QPixmap 转换为 PIL Image 对象
    def pixmap_to_pil(self, pixmap):
        buffer = QBuffer()  # 使用 QBuffer
        buffer.open(QBuffer.ReadWrite)  # 打开为读写模式
        pixmap.save(buffer, format="JPEG")  # 保存到 QBuffer
        buffer.seek(0)  # 重置缓冲区位置
        return Image.open(BytesIO(buffer.data()))  # 使用 BytesIO 读取数据

    # 比较截取的图片和已有的图片是否相同
    async def compare_images(self, screenshot_pixmap):
        if not os.path.exists(self.screenshot_path):
            return False

        # 将 QPixmap 转换为 PIL Image
        screenshot_image = self.pixmap_to_pil(screenshot_pixmap)

        # 加载已有图片
        existing_image = Image.open(self.screenshot_path)

        # 比较两张图片
        diff = ImageChops.difference(screenshot_image, existing_image)
        return not diff.getbbox()  # 如果没有差异，返回True，否则返回False

    # 执行图片捕获和比较操作
    async def process_capture(self):
        # 截取屏幕内容
        screenshot_pixmap = await self.capture_screen()
        if screenshot_pixmap is None:
            return

        # 比较图片，如果不同则覆盖原图并执行API请求
        if not await self.compare_images(screenshot_pixmap):
            # 将截图保存为 .jpg 并覆盖
            screenshot_pixmap.save(self.screenshot_path, 'jpg')
            await self.gt_tran()

    # 调用ocr函数
    async def gt_tran(self):
        print("图片已更改，调用ocr")
        self.translate = await self.get_tran.ocr_api()  # 模拟异步API调用


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建 ScreenCapture 实例（内部自动实例化 SelectAreaWidget）
    screen_capture = ScreenCapture()


    # 定义一个异步任务，用来运行截图和图片比较
    async def run_test():
        await screen_capture.process_capture()


    # 使用 asyncio 运行异步任务
    asyncio.run(run_test())

    sys.exit(app.exec_())