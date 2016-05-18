#-*- coding: utf-8
import random
import numpy as np
from numpy import genfromtxt


class RFGraph_Model:

    def __init__(self):
        self.pos=self.pos_graph()
        self.adj_simple = genfromtxt('data/adj_simple_withMol.csv', delimiter=',')
        self.adj_cmplx = genfromtxt('data/adj_cmplx_withMol.csv', delimiter=',')
        self.adj_fit = genfromtxt('data/adj_fit_withMol.csv', delimiter=',')
        self.adj_contr = genfromtxt('data/adj_contraintes_withMol.csv', delimiter=',')
        self.varnames = genfromtxt('data/varnames_withMol.csv', dtype='str', delimiter=',')
        self.nbeq = genfromtxt('data/nbeq_withMol.csv', delimiter=',')
        self.equacolPOf = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv', 'float', delimiter=',')
        self.equacolPOs = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv', 'str', delimiter=',')
        self.equacolOf = genfromtxt('data/equa_with_col_Parent_withMol.csv', 'float', delimiter=',')
        self.equacolOs = genfromtxt('data/equa_with_col_Parent_withMol.csv', 'str', delimiter=',')
        self.dataset_cell_popS = genfromtxt('data/dataset_cell_pop.csv', 'str', delimiter=',')
        self.dataset_mol_cellS = genfromtxt('data/dataset_mol_cell.csv', 'str', delimiter=',')
        self.dataset_cell_popF = genfromtxt('data/dataset_cell_pop.csv', 'float', delimiter=',')
        self.dataset_mol_cellF = genfromtxt('data/dataset_mol_cell.csv', 'float', delimiter=',')

        self.showGlobalModel = False
        self.lastNodeClicked = ""
        self.last_clicked = None
        self.mode_cntrt = False
        self.cntrt_FirstClick = ''
        self.cntrt_SecondClick = ''
        self.forbidden_edge = []
        self.curr_tabl=[]
        self.adjThresholdVal=0.5
        self.comprFitCmplxVal=0.5
        self.opt_params= []
        self.clicked_line=-1
        self.old_color=[]


        # Charge la base de données d'équations à afficher après chargement
        # TODO: Base de données d'équations à changer
        self.data = []
        for i in range(len(self.equacolPOs)):
            self.data.append(self.equacolPOs[i, np.ix_([0, 1, 4])][0])


    def pos_graph(self):
        pos = {}
        pos['Age'] = np.array([0.66, 15.0 / 15.0])
        pos['Temperature'] = np.array([0.33, 15.0 / 15.0])
        pos['AMACBIOSYNTH'] = np.array([random.random() * 0.1 + 0.05,14.0/15.0])
        pos['BIOSYNTH_CARRIERS'] = np.array([random.random() * 0.1 + 0.25,14.0/15.0])
        pos['CELLENVELOPE'] = np.array([random.random() * 0.1 + 0.45,14.0/15.0])
        pos['CELLPROCESSES'] = np.array([random.random() * 0.1 + 0.65,14.0/15.0])
        pos['CENTRINTMETABO'] = np.array([random.random() * 0.1 + 0.85,14.0/15.0])
        pos['ENMETABO'] = np.array([random.random() * 0.1 + 0.05,13.0/15.0])
        pos['FATTYACIDMETABO'] = np.array([random.random() * 0.1 + 0.25,13.0/15.0])
        pos['Hypoprot'] = np.array([random.random() * 0.1 + 0.45,13.0/15.0])
        pos['OTHERCAT'] = np.array([random.random() * 0.1 + 0.65,13.0/15.0])
        pos['PURINES'] = np.array([random.random() * 0.1 + 0.85,13.0/15.0])
        pos['REGULFUN'] = np.array([random.random() * 0.1 + 0.05,12.0/15.0])
        pos['REPLICATION'] = np.array([random.random() * 0.1 + 0.25,12.0/15.0])
        pos['TRANSCRIPTION'] = np.array([random.random() * 0.1 + 0.45,12.0/15.0])
        pos['TRANSLATION'] = np.array([random.random() * 0.1 + 0.65,12.0/15.0])
        pos['TRANSPORTPROTEINS'] = np.array([random.random() * 0.1 + 0.85,12.0/15.0])
        pos['UFA'] = np.array([1 / 4.0, 11.0 / 15.0])
        pos['SFA'] = np.array([2 / 4.0, 11.0 / 15.0])
        pos['CFA'] = np.array([3 / 4.0, 11.0 / 15.0])
        pos['Anisotropie'] = np.array([random.random() * 0.15 + 0.05, 10.0 / 15.0])
        pos['UFAdivSFA'] = np.array([random.random() * 0.15 + 0.3, 10.0 / 15.0])
        pos['CFAdivSFA'] = np.array([random.random() * 0.15 + 0.55, 10.0 / 15.0])
        pos['CFAdivUFA'] = np.array([random.random() * 0.15 + 0.8, 10.0 / 15.0])
        pos['UFCcentri'] = np.array([random.random() * 0.15 + 0.05, 9.0 / 15.0])
        pos['tpH07centri'] = np.array([random.random() * 0.15 + 0.3, 9.0 / 15.0])
        pos['tpH07scentri'] = np.array([random.random() * 0.15 + 0.55, 9.0 / 15.0])
        pos['tpH07spe2centri'] = np.array([random.random() * 0.15 + 0.85, 9.0 / 15.0])
        pos['UFCcong'] = np.array([random.random() * 0.15 + 0.05, 8.0 / 15.0])
        pos['tpH07cong'] = np.array([random.random() * 0.15 + 0.3, 8.0 / 15.0])
        pos['tpH07scong'] = np.array([random.random() * 0.15 + 0.55, 8.0 / 15.0])
        pos['tpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 8.0 / 15.0])
        pos['dUFCcong'] = np.array([random.random() * 0.15 + 0.05, 7.0 / 15.0])
        pos['dtpH07cong'] = np.array([random.random() * 0.15 + 0.3, 7.0 / 15.0])
        pos['dtpH07scong'] = np.array([random.random() * 0.15 + 0.55, 7.0 / 15.0])
        pos['dtpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 7.0 / 15.0])
        pos['UFClyo'] = np.array([random.random() * 0.15 + 0.05, 6.0 / 15.0])
        pos['TpH07lyo'] = np.array([random.random() * 0.15 + 0.2, 6.0 / 15.0])
        pos['tpH07slyo'] = np.array([random.random() * 0.15 + 0.55, 6.0 / 15.0])
        pos['tpH07spe2lyo'] = np.array([random.random() * 0.15 + 0.8, 6.0 / 15.0])
        pos['dUFCdes'] = np.array([random.random() * 0.15 + 0.05, 5.0 / 15.0])
        pos['dtpH07des'] = np.array([random.random() * 0.15 + 0.3, 5.0 / 15.0])
        pos['dtpH07sdes'] = np.array([random.random() * 0.15 + 0.55, 5.0 / 15.0])
        pos['dtpH07spe2des'] = np.array([random.random() * 0.15 + 0.8, 5.0 / 15.0])
        pos['dtUFClyo'] = np.array([random.random() * 0.15 + 0.05, 4.0 / 15.0])
        pos['dtpH07lyo'] = np.array([random.random() * 0.15 + 0.3, 4.0 / 15.0])
        pos['dtpH07slyo'] = np.array([random.random() * 0.15 + 0.55, 4.0 / 15.0])
        pos['dtpH07spe2lyo'] = np.array([random.random() * 0.15 + 0.8, 4.0 / 15.0])
        pos['UFCsto3'] = np.array([random.random() * 0.15 + 0.05, 3.0 / 15.0])
        pos['tpH07sto3'] = np.array([random.random() * 0.15 + 0.3, 3.0 / 15.0])
        pos['tpH07ssto3'] = np.array([random.random() * 0.15 + 0.55, 3.0 / 15.0])
        pos['tpH07spe2sto3'] = np.array([random.random() * 0.15 + 0.8, 3.0 / 15.0])
        pos['dUFCsto3'] = np.array([random.random() * 0.15 + 0.05, 2.0 / 15.0])
        pos['dtpH07sto3'] = np.array([random.random() * 0.15 + 0.3, 2.0 / 15.0])
        pos['dtpH07ssto3'] = np.array([random.random() * 0.15 + 0.55, 2.0 / 15.0])
        pos['dtpH07spe2sto3'] = np.array([random.random() * 0.15 + 0.8, 2.0 / 15.0])
        pos['dUFCtot'] = np.array([random.random() * 0.15 + 0.05, 1.0 / 15.0])
        pos['dtpH07tot'] = np.array([random.random() * 0.15 + 0.3, 1.0 / 15.0])
        pos['dtpH07stot'] = np.array([random.random() * 0.15 + 0.55, 1.0 / 15.0])
        pos['dtpH07spe2tot'] = np.array([random.random() * 0.15 + 0.8, 1.0 / 15.0])
        return pos
