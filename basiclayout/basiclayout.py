import sys
from PyQt5.QtWidgets import (QDialog, QMainWindow, QTextEdit, QApplication,
                             QDialogButtonBox, QVBoxLayout, QMenuBar, QMenu,
                             QGroupBox, QHBoxLayout, QGridLayout, QPushButton,
                             QLabel, QLineEdit, QFormLayout, QComboBox,
                             QSpinBox)


class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.NumGridRows = 3
        self.NumButtons = 4
        self.menuBar = self.createMenu()
        self.horizontalGroupBox = self.createHorizontalGroupBox()
        self.gridGroupBox = self.createGridGroupBox()
        self.formGroupBox = self.createFormGroupBox()
        self.bigEditor = QTextEdit()
        self.bigEditor.setPlainText(self.tr("This widget takes up all the "
                                    "remaining space in the top-level layout."))
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                          | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setMenuBar(self.menuBar)
        self.mainLayout.addWidget(self.horizontalGroupBox)
        self.mainLayout.addWidget(self.gridGroupBox)
        self.mainLayout.addWidget(self.formGroupBox)
        self.mainLayout.addWidget(self.bigEditor)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle(self.tr("Basic Layouts"))

    def createMenu(self):
        menuBar = QMenuBar()
        fileMenu = QMenu(self.tr("&File"), self)
        exitAction = fileMenu.addAction(self.tr("E&xit"))
        menuBar.addMenu(fileMenu)
        exitAction.triggered.connect(self.accept)
        return menuBar

    def createHorizontalGroupBox(self):
        horizontalGroupBox = QGroupBox(self.tr("Horizontal layout"))
        layout = QHBoxLayout()
        for i in range(self.NumButtons):
            button = QPushButton(self.tr("Button " + str(i + 1)))
            layout.addWidget(button)
        horizontalGroupBox.setLayout(layout)
        return horizontalGroupBox

    def createGridGroupBox(self):
        gridGroupBox = QGroupBox(self.tr("Grid layout"))
        layout = QGridLayout()
        label1 = QLabel(self.tr("Line 1"))
        label2 = QLabel(self.tr("Line 2"))
        label3 = QLabel(self.tr("Line 3"))
        lineEdit1 = QLineEdit()
        lineEdit2 = QLineEdit()
        lineEdit3 = QLineEdit()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(lineEdit1, 0, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(lineEdit2, 2, 1)
        layout.addWidget(label3, 3, 0)
        layout.addWidget(lineEdit3, 3, 1)
        # for i in range(self.NumGridRows):
        #     label = QLabel(self.tr("Line " + str(i + 1)))
        #     lineEdit = QLineEdit()
        #     layout.addWidget(label, i + 1, 0)
        #     layout.addWidget(lineEdit, i + 1, 1)
        smallEditor = QTextEdit()
        puk = smallEditor.sizeHint()
        smallEditor.setPlainText(self.tr("This widget takes up about two "
                                         "thirds of the grid layout."))
        layout.addWidget(smallEditor, 0, 2, 4, 1)
        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        gridGroupBox.setLayout(layout)
        return gridGroupBox

    def createFormGroupBox(self):
        formGroupBox = QGroupBox(self.tr("Form layout"))
        layout = QFormLayout()
        layout.addRow(QLabel(self.tr("Line 1:")), QLineEdit())
        layout.addRow(QLabel(self.tr("Line 2, long text:")), QComboBox())
        layout.addRow(QLabel(self.tr("Line 3:")), QSpinBox())
        formGroupBox.setLayout(layout)
        return formGroupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
