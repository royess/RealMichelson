import sys, os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QFormLayout, QPushButton, QLineEdit, QInputDialog

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from simulation import MichelsonSimulation
from visual import showPattern

progname = os.path.basename(sys.argv[0])

'''
    Illustrition for interface:

    ------------------------
    |                      |
    |       Screen         |
    |                      |
    ------------------------
    |       Control        |
    |        Panel         |
    ------------------------

    Here, the "screen" part is for display of the interference pattern on the screen,
    the "control panel" part is for controlling components.
'''

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
                                   
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class ScreenCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, *args, **kwargs):
        self.is_colored = True

        #initialize a simulation
        self.simulation = MichelsonSimulation()
        self.simulation.initialMirrorG([0, 0, 0], [-1, 1, 0])
        self.simulation.initialMirrorM1([0, 100, 0], [0, -1, 0])
        self.simulation.initialMirrorM2([100, 0, 0], [-1, 1e-3, 0])
        self.simulation.insertSource([-20, 0, 0], 635)
        self.simulation.changeToNonlocal()

        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        showPattern(self.axes, self.simulation, self.is_colored)
    
    def changeLocality(self, text):
        if text=='local' and self.simulation.islocalInterference==False:
            self.simulation.islocalInterference = True
            self.simulation.changeToLocal()
            self.axes.cla()
            showPattern(self.axes, self.simulation, self.is_colored)
            self.draw()
        elif text=='nonlocal' and self.simulation.islocalInterference==True:
            self.simulation.islocalInterference = False
            self.simulation.changeToNonlocal()
            self.axes.cla()
            showPattern(self.axes, self.simulation, self.is_colored)
            self.draw()   

    def changeColor(self, text):
        if text=='colored' and self.is_colored==False:
            self.is_colored = True 
            self.axes.cla()
            showPattern(self.axes, self.simulation, self.is_colored)
            self.draw()
        elif text=='mono' and self.is_colored==True:
            self.is_colored = False
            self.axes.cla()
            showPattern(self.axes, self.simulation, self.is_colored)
            self.draw()

    def changeSource(self, text):
        wavelenth = int(text)
        self.axes.cla()
        self.simulation.clearSource()
        self.simulation.insertSource([-20, 0, 0], wavelenth)
        showPattern(self.axes, self.simulation, self.is_colored)
        self.draw()

    def changeM1(self, text):
        y = float(text)
        self.simulation.setMirrorM1([0,y,0])
        self.axes.cla()
        showPattern(self.axes, self.simulation, self.is_colored)
        self.draw()

    def changeM2(self, text):
        ny = float(text) # small angle approx.
        self.simulation.setMirrorM2([-1,ny,0])
        self.axes.cla()
        showPattern(self.axes, self.simulation, self.is_colored)
        self.draw()



class InputdialogDemo(QWidget):
    def __init__(self,parent=None):

        super(InputdialogDemo,self).__init__(parent)
        layout=QFormLayout()

        self.btn_loc=QPushButton("Locality?")
        self.btn_loc.clicked.connect(self.getLoc)
        self.le_loc=QLineEdit()
        self.le_loc.setText('nonlocal')
        layout.addRow(self.btn_loc,self.le_loc)

        self.btn_color=QPushButton("Colored or mono. screen?")
        self.btn_color.clicked.connect(self.getColor)
        self.le_color=QLineEdit()
        self.le_color.setText('colored')
        layout.addRow(self.btn_color,self.le_color)

        self.btn_spec=QPushButton("Wavelenth in nm?")
        self.btn_spec.clicked.connect(self.getSpec)
        self.le_spec=QLineEdit()
        self.le_spec.setText('635')
        layout.addRow(self.btn_spec,self.le_spec)

        self.btn_M1=QPushButton("M1 location:")
        self.btn_M1.clicked.connect(self.getM1)
        self.le_M1=QLineEdit()
        self.le_M1.setText('100')
        layout.addRow(self.btn_M1,self.le_M1)

        self.btn_M2=QPushButton("M2 angle:")
        self.btn_M2.clicked.connect(self.getM2)
        self.le_M2=QLineEdit()
        self.le_M2.setText('1e-3')
        layout.addRow(self.btn_M2,self.le_M2)

        self.setLayout(layout)
        self.setWindowTitle("Input Dialog例子")

    def getLoc(self):
        items = ("local","nonlocal")
        item, ok = QInputDialog.getItem(self,"select Input dialog","Interference type?",items,0,False)
        if ok and item:
            self.le_loc.setText(item)

    def getColor(self):
        items=("colored","mono")
        item, ok = QInputDialog.getItem(self,"select Input dialog","Interference type?",items,0,False)
        if ok and item:
            self.le_color.setText(item)

    def getM1(self):
        text, ok = QInputDialog.getText(self,'Text Input Dialog','M1 location?')
        if ok:
            self.le_M1.setText(str(text))
        
    def getM2(self):
        text, ok = QInputDialog.getText(self,'Text Input Dialog','M2 angle?')
        if ok:
            self.le_M2.setText(str(text))

    def getSpec(self):
        text, ok = QInputDialog.getText(self,"Text Input Dialog","Wavelength?")
        if ok:
            self.le_spec.setText(str(text))


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = ScreenCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)

        idd = InputdialogDemo()
        l.addWidget(idd)

        idd.le_loc.textChanged.connect(sc.changeLocality)
        idd.le_color.textChanged.connect(sc.changeColor)
        idd.le_spec.textChanged.connect(sc.changeSource)
        idd.le_M1.textChanged.connect(sc.changeM1)
        idd.le_M2.textChanged.connect(sc.changeM2)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """GUI for RealMichelson."""
                                )

if __name__=='__main__':
    qApp = QtWidgets.QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())
    #qApp.exec_()