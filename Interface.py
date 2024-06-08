import json

import numpy as np
import time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

from Config import CONFIG
import Repository as REPO

# Instruments
from Instruments_Libraries.Photron import PhotronCamera  # IP address: 192.168.0.10
import Instruments_Libraries.Firefly_LW_2024 as Firefly  # Laser IP address: 192.168.1.231; Host computer IP address: 192.168.1.187
from Instruments_Libraries.ConexCC import ConexCC


class Worker_Initial(QThread):
    def __init__(self, window):
        self.window = window
        super().__init__()
    def run(self):
        #if CONFIG['DEBUG']:
            #return
        starting_wave = self.window.Wavenumber.value()
        frames = int(self.window.NumberOfFrames.value())
        new_x, new_y = REPO.mirror_correction(starting_wave)

        try:
            self.window.conex1.move_absolute(new_x)
        except:
            print("Movement skipped for x")
        try:
            self.window.conex2.move_absolute(new_x)
        except:
            print("Movement skipped for y")

        current_wl = round(json.loads(self.window.ff3.wavelength_status())['message']['parameters']['current_wavelength'][0])
        self.window.ff3.go_to_wavelength(starting_wave)

        while abs(current_wl - starting_wave) > 1:
            current_wl = round(json.loads(self.window.ff3.wavelength_status())['message']['parameters']['current_wavelength'][0])

        image = self.window.camera.returnFinalImage_Linda(frames, starting_wave, Mod=True, Flip=True, x1=0, x2=0, y1=CONFIG['IMAGE_SIZE'], y2=CONFIG['IMAGE_SIZE'])

        self.window.Initial_Axes.imshow(image, cmap='bwr')
        self.window.Initial_Canvas.draw()

class Worker_Live(QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window
    def run(self):
        for i in range(5):
            time.sleep(1)

class Worker_Hyper(QThread):
    def __init__(self, window):
        """

        :type window: MainWindow
        """
        super().__init__()
        self.window = window
    def run(self):
        self.window.HyperProgress.setValue(1)

        xmin, xmax, ymin, ymax = (0, 0, 0, 0)
        if self.window.PictureArea is None :
            squareSize = self.window.SquareSize
            xmin = int((CONFIG['IMAGE_SIZE'] - squareSize) / 2)
            xmax = int((CONFIG['IMAGE_SIZE'] + squareSize) / 2)
            ymin = int((CONFIG['IMAGE_SIZE'] - squareSize) / 2)
            ymax = int((CONFIG['IMAGE_SIZE'] + squareSize) / 2)


        array_depth = int((self.window.WavenumberMax.value() - self.window.WavenumberMin.value()) / self.window.Step.currentData())
        array_size = xmax - xmin


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(CONFIG['WINDOW_TITLE'])
        self.StopHyper = False
        self.PictureArea = None
        self.Worker_Initial = Worker_Initial(self)
        self.Worker_Live = Worker_Live(self)
        self.Worker_Hyper = Worker_Hyper(self)

        if CONFIG['DEBUG'] is False:
            # PHOTRON CAMERA
            self.camera = PhotronCamera()
            REPO.setup_camera(self.camera)
            # FIREFLY
            self.ff3 = Firefly.Firefly_LW_2024(sock=None)
            # CONEX
            self.conex1 = ConexCC(com_port='COM3', velocity=0.5)  # Link to Newport motor 1
            self.conex2 = ConexCC(com_port='COM7', velocity=0.5)  # Link to Newport motor 2

        # region MAIN LAYOUT
        MainWidget = QWidget()
        MainWidget_Layout = QGridLayout()

        # region SETTINGS
        Settings_Box = QGroupBox("Settings")
        Settings_Layout = QVBoxLayout()

        # region INITIAL IMAGE SETTINGS
        InitialImage_Box = QGroupBox("Initial Image")
        InitialImage_Layout = QGridLayout()

        self.Wavenumber = QDoubleSpinBox()
        self.Wavenumber.setMinimum(1040)
        self.Wavenumber.setMaximum(1840)
        self.Wavenumber.setValue(1450)
        self.Wavenumber.setDecimals(0)
        self.Wavenumber.setSingleStep(1)
        self.Wavenumber.setStyleSheet("border-radius : 15; border : 1px solid white; background-color : #F2DB74;color:black")

        self.NumberOfFrames = QDoubleSpinBox()
        self.NumberOfFrames.setMinimum(1)
        self.NumberOfFrames.setMaximum(1000000)
        self.NumberOfFrames.setValue(5000)
        self.NumberOfFrames.setDecimals(0)
        self.NumberOfFrames.setSingleStep(1)
        self.NumberOfFrames.setStyleSheet("border-radius : 15; border : 1px solid white; background-color : #F2DB74;color:black")

        self.Btn_InitialImage = QPushButton('Acquire Initial Image')

        self.Shutterspeed = QComboBox()
        for speed in CONFIG['SHUTTERSPEED_OPTIONS_NS']:
            self.Shutterspeed.addItem(f"{speed} ns", speed)
        self.Shutterspeed.setCurrentIndex(1)

        InitialImage_Layout.addWidget(QLabel("Wavenumber (cm-1)"), 0, 0)
        InitialImage_Layout.addWidget(self.Wavenumber, 1, 0)
        InitialImage_Layout.addWidget(QLabel("Number of frames"), 0, 1)
        InitialImage_Layout.addWidget(self.NumberOfFrames, 1, 1)
        InitialImage_Layout.addWidget(self.Btn_InitialImage, 2, 0, 1, 2)
        InitialImage_Layout.addWidget(self.Shutterspeed, 3, 0, 1, 2)

        InitialImage_Box.setLayout(InitialImage_Layout)
        # endregion

        # region LIVE IMAGE SETTINGS
        Live_Box = QGroupBox("Live Imaging")
        Live_Layout = QGridLayout()

        self.Btn_StartLive = QPushButton("Save Cube (npy)")
        self.Btn_StopLive = QPushButton("Save Cube (npy)")

        Live_Layout.addWidget(self.Btn_StartLive, 0, 0)
        Live_Layout.addWidget(self.Btn_StopLive, 0, 1)

        Live_Box.setLayout(Live_Layout)
        # endregion

        # region REGION OF INTEREST
        RegionOfInterest_Box = QGroupBox("Region Of Interest")
        RegionOfInterest_Layout = QGridLayout()

        self.SquareSize = QComboBox()
        for size in CONFIG['SQUARE_SIZES']:
            self.SquareSize.addItem(f"{size}x{size}", size)
        self.SquareSize.setCurrentIndex(1)

        RegionOfInterest_Layout.addWidget(self.SquareSize, 0, 0)

        RegionOfInterest_Box.setLayout(RegionOfInterest_Layout)
        # endregion

        # region HYPERSPECTRAL
        Hyperspectral_Box = QGroupBox("Hyperspectral")
        Hyperspectral_Layout = QGridLayout()

        self.HyperCheck = QCheckBox('On')

        self.Step = QComboBox()
        for step in CONFIG['HYPER_STEPS']:
            self.Step.addItem(f"{step}", step)
        self.Step.setCurrentIndex(1)

        self.WavenumberMin = QDoubleSpinBox()
        self.WavenumberMin.setMinimum(1042)  # do not go below 1041 for firefly LW laser
        self.WavenumberMin.setMaximum(1840)  # do not go above 1840 for firefly LW laser
        self.WavenumberMin.setValue(1042)
        self.WavenumberMin.setDecimals(0)
        self.WavenumberMin.setSingleStep(1)

        self.WavenumberMax = QDoubleSpinBox()
        self.WavenumberMax.setMinimum(1042)  # do not go below 1041 for firefly LW laser
        self.WavenumberMax.setMaximum(1840)  # do not go above 1840 for firefly LW laser
        self.WavenumberMax.setValue(1840)
        self.WavenumberMax.setDecimals(0)
        self.WavenumberMax.setSingleStep(1)

        self.HyperProgress = QProgressBar(self)
        self.HyperProgress.setValue(0)

        self.Btn_HyperStart = QPushButton("Start")
        self.Btn_HyperStop = QPushButton("Stop")

        Hyperspectral_Layout.addWidget(QLabel("Step (cm-1)"), 0, 1)
        Hyperspectral_Layout.addWidget(self.HyperCheck, 1, 0)
        Hyperspectral_Layout.addWidget(self.Step, 1, 1)
        Hyperspectral_Layout.addWidget(QLabel("Min. Wavenumber (cm-1)"), 2, 0)
        Hyperspectral_Layout.addWidget(self.WavenumberMin, 3, 0)
        Hyperspectral_Layout.addWidget(QLabel("Max. Wavenumber (cm-1)"), 2, 1)
        Hyperspectral_Layout.addWidget(self.WavenumberMax, 3, 1)
        Hyperspectral_Layout.addWidget(self.HyperProgress, 4, 0, 1, 2)
        Hyperspectral_Layout.addWidget(self.Btn_HyperStart, 5, 0)
        Hyperspectral_Layout.addWidget(self.Btn_HyperStop, 5, 1)

        Hyperspectral_Box.setLayout(Hyperspectral_Layout)
        # endregion

        # region SAVE DATA
        Data_Box = QGroupBox("Save Data")
        Data_Layout = QGridLayout()

        self.SaveInitialTxt_Name = QLineEdit('FileName')
        self.Btn_SaveInitialTxt = QPushButton("Save Image (txt)")
        self.SaveCubeNpy_Name = QLineEdit('FileName')
        self.Btn_SaveCubeNpy = QPushButton("Save Cube (npy)")
        self.SaveCubeTxt_Name = QLineEdit('FileName')
        self.Btn_SaveCubeTxt = QPushButton("Save Cube (txt)")

        Data_Layout.addWidget(self.SaveInitialTxt_Name, 0, 0)
        Data_Layout.addWidget(self.SaveCubeNpy_Name, 0, 1)
        Data_Layout.addWidget(self.SaveCubeTxt_Name, 0, 2)
        Data_Layout.addWidget(self.Btn_SaveInitialTxt, 1, 0)
        Data_Layout.addWidget(self.Btn_SaveCubeNpy, 1, 1)
        Data_Layout.addWidget(self.Btn_SaveCubeTxt, 1, 2)

        Data_Box.setLayout(Data_Layout)
        # endregion

        Settings_Layout.addWidget(InitialImage_Box)
        Settings_Layout.addWidget(RegionOfInterest_Box)
        Settings_Layout.addWidget(Hyperspectral_Box)
        Settings_Layout.addWidget(Data_Box)

        Settings_Box.setLayout(Settings_Layout)
        # endregion

        # region PLOTS
        Plots_Box = QGroupBox("Data")
        Plots_Layout = QHBoxLayout()

        # region INITIAL IMAGE
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.canvas.mpl_connect('button_press_event', lambda event: REPO.drawSquareOnPlot(event, self))
        self.Initial_Canvas = FigureCanvasQTAgg(fig)
        self.Initial_Axes = fig.add_subplot(111)
        self.Initial_Axes.imshow(np.random.random((512, 512)), cmap='bwr')
        self.Initial_Axes.tick_params(axis='both', direction='in', labelsize=CONFIG['PLOT_TICKERSIZE'])
        self.Initial_Axes.set_xlabel('Pixels', fontsize=CONFIG['PLOT_LABELSIZE'])
        self.Initial_Axes.set_ylabel('Pixels', fontsize=CONFIG['PLOT_LABELSIZE'])
        self.Initial_Axes.set_title("Initial Image", fontsize=CONFIG['PLOT_TITLESIZE'])
        self.Initial_Canvas.draw()
        # endregion

        # region LIVE IMAGE
        fig = Figure(figsize=(5, 4), dpi=100)
        self.Live_Canvas = FigureCanvasQTAgg(fig)
        self.Live_Axes = fig.add_subplot(111)
        self.Live_Axes.imshow(np.random.random((512, 512)), cmap='bwr')
        self.Live_Axes.tick_params(axis='both', direction='in', labelsize=CONFIG['PLOT_TICKERSIZE'])
        self.Live_Axes.set_xlabel('Pixels', fontsize=CONFIG['PLOT_LABELSIZE'])
        self.Live_Axes.set_ylabel('Pixels', fontsize=CONFIG['PLOT_LABELSIZE'])
        self.Live_Axes.set_title("Live Image", fontsize=CONFIG['PLOT_TITLESIZE'])
        self.Live_Canvas.draw()
        # endregion

        # region HYPER IMAGE
        fig = Figure(figsize=(5, 4), dpi=100)
        self.Hyper_Canvas = FigureCanvasQTAgg(fig)
        self.Hyper_Axes = fig.add_subplot(111)
        self.Hyper_Axes.imshow(np.random.random((512, 512)), cmap='bwr')
        self.Hyper_Axes.tick_params(axis='both', direction='in', labelsize=CONFIG['PLOT_TICKERSIZE'])
        self.Hyper_Axes.set_xlabel('Pixels', fontsize=CONFIG['PLOT_LABELSIZE'])
        self.Hyper_Axes.set_ylabel('Pixels', fontsize=CONFIG['PLOT_LABELSIZE'])
        self.Hyper_Axes.set_title("Hyperspectral", fontsize=CONFIG['PLOT_TITLESIZE'])
        self.Hyper_Canvas.draw()
        # endregion

        Plots_Layout.addWidget(self.Initial_Canvas)
        Plots_Layout.addWidget(self.Live_Canvas)
        Plots_Layout.addWidget(self.Hyper_Canvas)


        Plots_Box.setLayout(Plots_Layout)
        # endregion

        MainWidget_Layout.addWidget(Settings_Box, 0, 0)
        MainWidget_Layout.addWidget(Plots_Box, 0, 1)
        # endregion

        # Set main widget
        MainWidget.setLayout(MainWidget_Layout)
        self.setCentralWidget(MainWidget)
        self.resize(CONFIG['INTERFACE_WIDTH'], CONFIG['INTERFACE_HEIGHT'])

        # region SIGNALS
        self.Btn_InitialImage.clicked.connect(lambda: REPO.getInitialImage(self))
        self.Btn_StartLive.clicked.connect(lambda: REPO.getLiveImage(self))
        self.Btn_HyperStart.clicked.connect(lambda: REPO.getHyperCube(self))
        # endregion




app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
