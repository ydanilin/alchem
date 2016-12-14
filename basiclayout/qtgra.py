import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QProxyStyle, QFrame, QWidget, QHBoxLayout
from PyQt5.QtCore import QSize

class MoyStil(QProxyStyle):
    def __init__(self):
        super(MoyStil, self).__init__()
        f = open('puk.json')
        self.jsonDict = json.load(f)
        f.close()

    def getEnumName(self, arg, family):
        name = None
        key = str(arg)
        pmDict = self.jsonDict[family]
        if key in pmDict.keys():
            name = pmDict[key]
        return name

    def pixelMetric(self, metric, option=None, widget=None):
        size = super(MoyStil, self).pixelMetric(metric, option, widget)
        name = self.getEnumName(metric, 'PM_')
        print('pixelMetric(): metricNo {0}:{1} (value: {2}), option {3}, widget {4}'.format(
            metric, name, size, option, type(widget).__name__))
        return size

    def polish(self, arg):
        print('polish() called: arg {0}'.format(type(arg).__name__))
        if isinstance(arg, QWidget):
            print(arg.width())
        return super(MoyStil, self).polish(arg)

    def drawPrimitive(self, element, option, painter, widget):
        print('drawPrimitive() called')
        return super(MoyStil, self).drawPrimitive(element, option, painter, widget)

    def styleHint(self, hint, option, widget, returnData):
        # name = self.getEnumName(hint, 'SH_')
        # print('styleHint() called: hint {0}:{1}, option {2}, widget {3}, returnData {4}'.format(
        #     hint, name, option, type(widget).__name__, returnData))
        return super(MoyStil, self).styleHint(hint, option, widget, returnData)

    def drawControl(self, control, option, painter, widget):
        print('drawControl() called')
        return super(MoyStil, self).drawControl(control, option, painter, widget)


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
        self.setFrameStyle(QFrame.Box | QFrame.Plain)

    def paintEvent(self, event):
        print('hujFrame PaintEvent()', event.rect())
        super(hujFrame, self).paintEvent(event)

    def sizeHint(self):
        return QSize(600, 500)

class bdukFrame(QFrame):  # QWidget
    def __init__(self, parent=None):
        super(bdukFrame, self).__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)

    def paintEvent(self, event):
        print('bdukFrame PaintEvent()', event.rect())
        super(bdukFrame, self).paintEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(MoyStil())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())