# TODO Connecte les "clics" et les fonctions correspondantes
class QtConnector:
    def __init__(self,vwApp,cntrApp):
        self.vwApp=vwApp
        self.cntrApp=cntrApp
        self.vwApp.eqTableGUI.itemClicked.connect(self.cntrApp.eqTableClicked)
        self.vwApp.adjThreshold_slider.valueChanged.connect(self.cntrApp.SliderMoved)
        self.vwApp.networkGUI.fig.canvas.mpl_connect('button_press_event', self.cntrApp.onClick)
        self.vwApp.networkGUI.fig.canvas.mpl_connect('motion_notify_event',self.cntrApp.onMove3)
        self.vwApp.incMatGUI.itemClicked.connect(self.cntrApp.incMatClicked)
        self.vwApp.closeEvent = self.cntrApp.closeEvent