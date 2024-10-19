import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QScreen, QPixmap

class SelectAreaWidget(QWidget):
    EDGE_SIZE = 20  # 边缘拖拽区域的大小
    BUFFER_SIZE = 20  # 增加额外的缓冲区域

    def __init__(self):
        super().__init__()
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.rect = QRect()
        self.is_drawing = False
        self.is_moving = False
        self.drag_edge = None
        self.drag_start_pos = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)#窗口始终在其他页面上方
        self.setAttribute(Qt.WA_TranslucentBackground)#设置背景透明
        self.showFullScreen() # 让绘制窗口占满全屏

        # 初始化虚线框位置
        self.init_default_rect()

    #绘制矩形，获取屏幕后做相关调整
    def init_default_rect(self):
        screen_rect = QApplication.primaryScreen().geometry()
        center_x = screen_rect.width() // 4
        center_y = screen_rect.height() // 4
        width = screen_rect.width() // 2
        height = screen_rect.height() // 2
        self.rect = QRect(center_x, center_y, width, height)
        self.update()

    #鼠标按下的事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            if self.is_on_edge(pos):
                self.drag_edge = self.get_edge(pos)
                self.is_drawing = True
                self.start_point = pos
                self.end_point = pos
            elif self.rect.contains(pos):
                self.is_moving = True
                self.drag_start_pos = pos - self.rect.topLeft()
            self.update()

    #鼠标移动事件
    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.is_drawing:
            if self.drag_edge:
                self.adjust_rect(pos)
            else:
                self.end_point = pos
                self.rect = QRect(self.start_point, self.end_point).normalized()
            self.update()
        elif self.is_moving:
            self.rect.moveTo(pos - self.drag_start_pos)
            self.update()

    #鼠标释放事件
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_drawing = False
            self.is_moving = False
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.DashLine))
        painter.drawRect(self.rect)

    #判断鼠标是否落在边缘或者缓冲区上
    def is_on_edge(self, pos):
        rect = self.rect
        extended_rect = rect.adjusted(-self.BUFFER_SIZE, -self.BUFFER_SIZE, self.BUFFER_SIZE, self.BUFFER_SIZE)
        return (abs(pos.x() - rect.left()) < self.EDGE_SIZE and
                (abs(pos.y() - rect.top()) < self.EDGE_SIZE or
                 abs(pos.y() - rect.bottom()) < self.EDGE_SIZE)) or \
            (abs(pos.x() - rect.right()) < self.EDGE_SIZE and
             (abs(pos.y() - rect.top()) < self.EDGE_SIZE or
              abs(pos.y() - rect.bottom()) < self.EDGE_SIZE)) or \
            (abs(pos.y() - rect.top()) < self.EDGE_SIZE and
             abs(pos.x() - rect.left()) < self.EDGE_SIZE) or \
            (abs(pos.y() - rect.bottom()) < self.EDGE_SIZE and
             abs(pos.x() - rect.left()) < self.EDGE_SIZE) or \
            extended_rect.contains(pos)

    #获取点击区域的是那个边缘
    def get_edge(self, pos):
        rect = self.rect
        if abs(pos.x() - rect.left()) < self.EDGE_SIZE:
            if abs(pos.y() - rect.top()) < self.EDGE_SIZE:
                return 'top-left'
            elif abs(pos.y() - rect.bottom()) < self.EDGE_SIZE:
                return 'bottom-left'
            else:
                return 'left'
        elif abs(pos.x() - rect.right()) < self.EDGE_SIZE:
            if abs(pos.y() - rect.top()) < self.EDGE_SIZE:
                return 'top-right'
            elif abs(pos.y() - rect.bottom()) < self.EDGE_SIZE:
                return 'bottom-right'
            else:
                return 'right'
        elif abs(pos.y() - rect.top()) < self.EDGE_SIZE:
            return 'top'
        elif abs(pos.y() - rect.bottom()) < self.EDGE_SIZE:
            return 'bottom'
        return None

    #调整矩形
    def adjust_rect(self, pos):
        rect = self.rect
        if self.drag_edge == 'top-left':
            rect.setTopLeft(pos)
        elif self.drag_edge == 'top-right':
            rect.setTopRight(pos)
        elif self.drag_edge == 'bottom-left':
            rect.setBottomLeft(pos)
        elif self.drag_edge == 'bottom-right':
            rect.setBottomRight(pos)
        elif self.drag_edge == 'left':
            rect.setLeft(pos.x())
        elif self.drag_edge == 'right':
            rect.setRight(pos.x())
        elif self.drag_edge == 'top':
            rect.setTop(pos.y())
        elif self.drag_edge == 'bottom':
            rect.setBottom(pos.y())
        self.rect = rect.normalized()

    def get_selection_rect(self):
        return self.rect

if __name__ == '__main__':
    app = QApplication(sys.argv)
    select_area = SelectAreaWidget()
    select_area.show()
    sys.exit(app.exec_())
