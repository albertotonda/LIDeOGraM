class QtConnector:
    def __init__(self,vwApp,cntrApp):
        self.vwApp=vwApp
        self.cntrApp=cntrApp
        self.vwApp.buttonAjtCntrt.clicked.connect(self.cntrApp.clickAjContrainte)
        self.vwApp.eqTableGUI.itemClicked.connect(self.cntrApp.tableClicked)
        self.vwApp.adjThreshold_slider.valueChanged.connect(self.cntrApp.SliderMoved)
        self.vwApp.comprFitCmplx_slider.valueChanged.connect(self.cntrApp.SliderMoved)
        self.vwApp.buttonModGlobal.clicked.connect(self.cntrApp.clickModGlobal)
        self.vwApp.buttonOptUgp3.clicked.connect(self.cntrApp.clickOptmuGP)
        self.vwApp.networkGUI.fig.canvas.mpl_connect('button_press_event', self.cntrApp.onClick)
        self.vwApp.closeEvent = self.cntrApp.closeEvent