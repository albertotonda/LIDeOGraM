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
        self.vwApp.networkGUI.fig.canvas.mpl_connect('motion_notify_event',self.cntrApp.onMove)
        #self.vwApp.networkGUI.fig.canvas.mpl_connect('pick_event', self.cntrApp.onPick)
        self.vwApp.closeEvent = self.cntrApp.closeEvent