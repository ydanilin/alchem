from epygraph import *


class Translator:
    def __init__(self):
        self.epygraph = Epygraph()
        self.gdata = {}

    def getBoundingBox(self):
        bbox = self.gdata['bbox'].split(',')
        gcoords = [float(i) for i in bbox]
        print(gcoords)

    def redraw(self):
        self.gdata = self.epygraph.redraw()


if __name__ == '__main__':
    T = Translator()
    T.redraw()
    T.getBoundingBox()
