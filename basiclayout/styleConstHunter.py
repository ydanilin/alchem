import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle

def enumerateStil(stil):
    output = {'SH_': {},
              'PE_': {},
              'PM_': {}}

    f = open('styleconst.txt')
    content = f.read().splitlines()
    f.close()

    for elem in content:
        prefix = elem[:3]
        if prefix in output.keys():
            try:
                value = eval('QStyle.' + elem)
            except:
                value = None
            output[prefix][value] = elem

    f = open('puk.json', 'w')
    json.dump(output, f)
    f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stil = app.style()
    enumerateStil(stil)
    win = QMainWindow()
    win.show()
    sys.exit(app.exec_())
