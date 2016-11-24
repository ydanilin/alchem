#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui



class RenderArea(QtGui.QWidget):
    points = QtGui.QPolygon([
        QtCore.QPoint(10, 80),
        QtCore.QPoint(20, 10),
        QtCore.QPoint(80, 30),
        QtCore.QPoint(90, 70)
    ])

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.antialiased = False
        self.transformed = False

        self.setBackgroundRole(QtGui.QPalette.Base)

    def minimumSizeHint(self):
        return QtCore.QSize(600, 900)

    def sizeHint(self):
        return QtCore.QSize(600, 900)


    def paintEvent(self, event):
        #rect = QtCore.QRect(10, 20, 80, 60)

        path = QtGui.QPainterPath()
        path.moveTo(20, 80)
        path.lineTo(20, 30)
        path.moveTo(40, 90)
        path.lineTo(40, 10)
        #path.cubicTo(80, 0, 50, 50, 80, 80)

        #startAngle = 30 * 16
        #arcLength = 120 * 16

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        painter.drawPath(path)
        painter.end()


IdRole = QtCore.Qt.UserRole

class Window(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.renderArea = RenderArea()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.renderArea, 0, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Basic Drawing"))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
