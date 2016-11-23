from epygraph import *


class Translator:
    def __init__(self):
        self.epygraph = Epygraph()
        self.gdata = {}

    def getBoundingBox(self):
        attrs = self.gdata['gattrs']
        print(attrs[''])

    def redraw(self):
        self.gdata = self.epygraph.redraw()
        print(self.gdata)
        self.getBoundingBox()


if __name__ == '__main__':
    T = Translator()
    T.redraw()
