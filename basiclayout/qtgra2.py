import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QProxyStyle, QFrame,
                             QWidget, QHBoxLayout, QGraphicsScene,
                             QGraphicsView, QSizePolicy, QGraphicsEllipseItem,
                             QGraphicsTextItem, QMenu)
from PyQt5.QtCore import QSize, QRect, Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor
from epygraph import AGraph


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.graph = AGraph()
        self.setWindowTitle('Basic Drawing')
        self.cf = centralFrame()
        self.hujLayout = QHBoxLayout()
        sc = QGraphicsScene()
        self.drawScene(sc)
        self.huj = hujFrame(sc)
        bduk = bdukFrame()
        self.hujLayout.addWidget(self.huj)
        self.hujLayout.addWidget(bduk)
        self.cf.setLayout(self.hujLayout)
        self.setCentralWidget(self.cf)

    def drawScene(self, scene):
        scaleDpi = 101.0 / 72.0  # (true res for 344x193 mm, 1366x768) / 72
        LLx = self.graph.boundingBox['LLx']
        LLy = self.graph.boundingBox['LLx']
        URx = self.graph.boundingBox['URx']
        URy = self.graph.boundingBox['URy']
        scene.addRect(LLx * scaleDpi, LLy * scaleDpi,
                         URx * scaleDpi, URy * scaleDpi)
        scale = 96  # maybe this is because GV uses 96 dpi and operates in inches
        for node in self.graph.nodesPtr:
            ng = self.graph.nodeGeometry(node)
            x = ng['centerX'] * scaleDpi
            y = (self.graph.boundingBox['URy'] - ng['centerY']) * scaleDpi
            rx = (ng['width'] / 2) * scale
            ry = (ng['height'] / 2) * scale
            el = NodeShape(x-rx, y-ry, 2*rx, 2*ry)
            label = self.graph.nodeLabel(node)
            lbl = QGraphicsTextItem(self.tr(label), el)
            # TODO: text positioniong
            lbl.setAcceptHoverEvents(False)
            # TODO: try to make child.event()
            lbl.setPos(x, y)
            scene.addItem(el)

        for edge in self.graph.edgesGeom:
            # TODO: edges hover
            spl = edge[0]
            if not spl['sflag']:
                start = spl['points'][0]
            else:
                start = spl['sarrowtip']
            if not spl['eflag']:
                end = spl['points'][-1]
            else:
                end = spl['earrowtip']
            x1 = start['x'] * scaleDpi
            y1 = (self.graph.boundingBox['URy'] - start['y']) * scaleDpi
            x2 = end['x'] * scaleDpi
            y2 = (self.graph.boundingBox['URy'] - end['y']) * scaleDpi
            scene.addLine(x1, y1, x2, y2)


class centralFrame(QFrame):  # QWidget
    def __init__(self, parent=None):
        super(centralFrame, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)

    # def sizeHint(self):
    #     return QSize(1200, 800)


class hujFrame(QGraphicsView):
    def __init__(self, parent=None):
        super(hujFrame, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def sizeHint(self):
        return QSize(660, 540)


class bdukFrame(QFrame):  # QWidget
    def __init__(self, parent=None):
        super(bdukFrame, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def sizeHint(self):
        return QSize(260, 540)


class NodeShape(QGraphicsEllipseItem):
    def __init__(self, x, y, width, height):
        super(NodeShape, self).__init__(x, y, width, height)
        self.setAcceptHoverEvents(True)
        self.oldpen = None
        self.oldTextColor = None

    def hoverEnterEvent(self, event):
        color = QColor('red')
        self.oldpen = self.pen()
        self.setPen(QPen(color))
        for child in self.childItems():
            # I know this is shitty solution, we will crash if children are
            # not of text type...
            self.oldTextColor = child.defaultTextColor()
            child.setDefaultTextColor(color)

    def hoverLeaveEvent(self, event):
        if self.oldpen:
            self.setPen(self.oldpen)
        if self.oldTextColor:
            for child in self.childItems():
                child.setDefaultTextColor(self.oldTextColor)

    def contextMenuEvent(self, event):
        # http://www.qtcentre.org/threads/5187-Popup-menu-for-a-QGraphicsItem
        # if use asynchronous call, ALWAYS pass a parent - event.widget()
        # to menu constructor, otherwise the menu will be destroyed immediately
        # as having zero reference
        menu = QMenu('Node', event.widget())
        menu.addAction(event.widget().tr('Add child node here'))
        menu.addAction(event.widget().tr('Delete subtree'))
        menu.popup(event.screenPos())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
