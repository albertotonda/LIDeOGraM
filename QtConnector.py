class QtConnector:
    def __init__(self):
        #TODO !
        self.buttonAjtCntrt.clicked.connect(self.clickAjContrainte)
        self.table.itemClicked.connect(self.tableClicked)
        self.ts_slider.valueChanged.connect(self.SliderMoved)
        self.ds_slider.valueChanged.connect(self.SliderMoved)
        self.buttonModGlobal.clicked.connect(self.clickModGlobal)
        self.buttonOptUgp3.clicked.connect(self.clickOptmuGP)
        self.RFG.fig.canvas.mpl_connect('button_press_event', self.onClick)