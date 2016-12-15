import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QProxyStyle, QFrame,
                             QWidget, QHBoxLayout)
from PyQt5.QtCore import QSize, QRect, Qt, QPointF
from PyQt5.QtGui import QPainter
from epygraph import AGraph

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Basic Drawing')
        self.cf = centralFrame()
        self.setCentralWidget(self.cf)
        self.hujLayout = QHBoxLayout()
        huj = hujFrame()
        bduk = bdukFrame()
        self.hujLayout.addWidget(huj)
        self.hujLayout.addWidget(bduk)
        self.cf.setLayout(self.hujLayout)


class centralFrame(QFrame):  # QWidget
    def __init__(self, parent=None):
        super(centralFrame, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)

    def sizeHint(self):
        return QSize(1000, 600)

    def paintEvent(self, event):
        print('centralFrame PaintEvent()', event.rect())
        super(centralFrame, self).paintEvent(event)


class hujFrame(QFrame):  # QWidget
    def __init__(self, parent=None):
        super(hujFrame, self).__init__(parent)
        # self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.graph = AGraph()

    def paintEvent(self, event):
        painter = QPainter()
        painter.save()
        painter.begin(self)
        pen = painter.pen()
        vport = painter.viewport()
        print('hujFrame painter.viewport()', vport)
        painter.drawRect(vport.adjusted(0, 0, -pen.width(), -pen.width()))
        # draw kvadratick in physical coordinates
        # painter.drawRect(0, 0, 100, 100)
        painter.drawLine(vport.topLeft(), vport.bottomRight())
        painter.drawLine(vport.bottomLeft(), vport.topRight())
        print(painter.device().physicalDpiX())
        print(painter.device().physicalDpiY())
        print(painter.device().logicalDpiX())
        print(painter.device().logicalDpiY())
        scaleDpi = 96.0/72.0
        painter.drawRect(self.graph.boundingBox['LLx']*scaleDpi, self.graph.boundingBox['LLy']*scaleDpi,
                         self.graph.boundingBox['URx']*scaleDpi, self.graph.boundingBox['URy']*scaleDpi)

        scale = 65
        for node in self.graph.nodesGeom:
            x = node['centerX']
            y = self.graph.boundingBox['URy'] - node['centerY']
            rx = (node['width']/2) * scale
            ry = (node['height']/2) * scale
            painter.drawEllipse(QPointF(x, y), rx, ry)

        # font = painter.font()
        # font.setPixelSize(56)
        # painter.setFont(font)
        # rectangle = QRect(0, 0, 100, 50)
        # boundingRect = painter.drawText(rectangle, 0, self.tr("Hello"))
        # pen.setStyle(Qt.DotLine)
        # painter.setPen(pen)
        # painter.drawRect(
        #     boundingRect.adjusted(0, 0, -pen.width(), -pen.width()))
        # pen.setStyle(Qt.DashLine)
        # painter.setPen(pen)
        # painter.drawRect(rectangle.adjusted(0, 0, -pen.width(), -pen.width()))
        painter.restore()
        painter.end()
        del painter
        super(hujFrame, self).paintEvent(event)

    def sizeHint(self):
        return QSize(700, 500)


class bdukFrame(QFrame):  # QWidget
    def __init__(self, parent=None):
        super(bdukFrame, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)

    def paintEvent(self, event):
        # print('bdukFrame PaintEvent()', event.rect())
        super(bdukFrame, self).paintEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())