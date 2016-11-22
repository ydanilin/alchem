from epygraph import *


class Translator:
    def __init__(self):
        self.epygraph = Epygraph()

    def redraw(self):
        self.epygraph.redraw()


if __name__ == '__main__':
    T = Translator()
    T.redraw()
