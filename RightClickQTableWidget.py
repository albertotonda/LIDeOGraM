from PyQt4.QtGui import *

class RightClickQTableWidget(QTableWidget):

    button=-1
    def __init__(self):
        print("init RightClickQTableWidget")
        super(RightClickQTableWidget, self).__init__()


    def mousePressEvent(self, *args, **kwargs):
       self.button = args[0]
       super(RightClickQTableWidget, self).mousePressEvent(args[0])



