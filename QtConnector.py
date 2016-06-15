# TODO Connecte les "clics" et les fonctions correspondantes
class QtConnector:
    def __init__(self,vwApp,cntrApp):
        self.vwApp=vwApp
        self.cntrApp=cntrApp
        self.vwApp.eqTableGUI.itemClicked.connect(self.cntrApp.tableClicked)
        self.vwApp.adjThreshold_slider.valueChanged.connect(self.cntrApp.SliderMoved)
        self.vwApp.comprFitCmplx_slider.valueChanged.connect(self.cntrApp.SliderMoved)
        self.vwApp.buttonShowModGlobal.clicked.connect(self.cntrApp.clickShowModGlobal)
        self.vwApp.buttonHideModGlobal.clicked.connect(self.cntrApp.clickHideModGlobal)
        self.vwApp.buttonOptUgp3.clicked.connect(self.cntrApp.clickOptmuGP)
        self.vwApp.buttonRemoveLink.clicked.connect(self.cntrApp.clickRemoveLink)
        self.vwApp.buttonReinstateLink.clicked.connect(self.cntrApp.clickReinstateLink)
        self.vwApp.buttonHelp.clicked.connect(self.cntrApp.clickHelp)
        self.vwApp.networkGUI.fig.canvas.mpl_connect('button_press_event', self.cntrApp.onClick)
        self.vwApp.closeEvent = self.cntrApp.closeEvent