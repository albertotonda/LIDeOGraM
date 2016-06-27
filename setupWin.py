#from py2exe.build_exe import py2exe
from distutils.core import setup
import py2exe
import matplotlib
import PyQt4
#import networkx
#import numpy
#import sympy
from os.path import dirname
import lib2to3
lib23_path = dirname(lib2to3.__file__)

opt = {'py2exe' : {
    'packages' : ['matplotlib','sympy','numpy','networkx','sympy','pytz'],
    'excludes': ['PyQt5', 'PySide','gtk','Gtk','gi','tkinter','lib2to3'],
    'dll_excludes' : ['libgdk-win32-2.0-0.dll','libgobject-2.0-0.dll'],
    #'include_files' : [lib23_path]
    }
}

setup( windows=[{"script": "RFGraphMain.py"}], options=opt, data_files=matplotlib.get_py2exe_datafiles(),zipfile=None )



#python setupWin.py py2exe --includes sip
