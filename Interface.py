from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import sys
from Config import CONFIG
import Repository as REPO

# Instruments
from Instruments_Libraries.Photron import PhotronCamera  # IP address: 192.168.0.10
import Instruments_Libraries.Firefly_LW_2024 as Firefly  # Laser IP address: 192.168.1.231; Host computer IP address: 192.168.1.187
from Instruments_Libraries.ConexCC import ConexCC


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(CONFIG['WINDOW_TITLE'])

        if CONFIG['DEBUG'] is False:
            # PHOTRON CAMERA
            self.camera = PhotronCamera()
            REPO.setup_camera(self.camera)
            # FIREFLY
            self.ff3 = Firefly.Firefly_LW_2024(sock=None)
            # CONEX
            self.conex1 = ConexCC(com_port='COM3', velocity=0.5)  # Link to Newport motor 1
            self.conex2 = ConexCC(com_port='COM7', velocity=0.5)  # Link to Newport motor 2

        # CREATE MAIN LAYOUT
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
        self.Wavenumber.setStyleSheet("border-radius : 15; border : 1px solid white; background-color : #F2DB74")

        self.NumberOfFrames = QDoubleSpinBox()
        self.NumberOfFrames.setMinimum(1)
        self.NumberOfFrames.setMaximum(1000000)
        self.NumberOfFrames.setValue(5000)
        self.NumberOfFrames.setDecimals(0)
        self.NumberOfFrames.setSingleStep(1)
        self.NumberOfFrames.setStyleSheet("border-radius : 15; border : 1px solid white; background-color : #F2DB74")

        self.Btn_InitialImage = QPushButton('Acquire Initial Image')

        self.Shutterspeed = QComboBox()
        for speed in CONFIG['SHUTTERSPEED_OPTIONS_NS']:
            self.Shutterspeed.addItem(f"{speed} ns", speed)
        self.Shutterspeed.setCurrentIndex(1)

        InitialImage_Layout.addWidget(QLabel("Wavenumber (cm-1)"), 0, 0)
        InitialImage_Layout.addWidget(self.Wavenumber, 1, 0)
        InitialImage_Layout.addWidget(QLabel("Number of frames"), 0, 1)
        InitialImage_Layout.addWidget(self.Wavenumber, 1, 1)
        InitialImage_Layout.addWidget(self.Btn_InitialImage, 2, 0, 1, 2)
        InitialImage_Layout.addWidget(self.Shutterspeed, 3, 0, 1, 2)

        InitialImage_Box.setLayout(InitialImage_Layout)
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

        self.HyperStart = QPushButton("Start")
        self.HyperStop = QPushButton("Stop")

        Hyperspectral_Layout.addWidget(QLabel("Step (cm-1)"), 0, 1)
        Hyperspectral_Layout.addWidget(self.HyperCheck, 1, 0)
        Hyperspectral_Layout.addWidget(self.Step, 1, 1)
        Hyperspectral_Layout.addWidget(QLabel("Min. Wavenumber (cm-1)"), 2, 0)
        Hyperspectral_Layout.addWidget(self.WavenumberMin, 3, 0)
        Hyperspectral_Layout.addWidget(QLabel("Max. Wavenumber (cm-1)"), 2, 1)
        Hyperspectral_Layout.addWidget(self.WavenumberMax, 3, 1)
        Hyperspectral_Layout.addWidget(self.HyperProgress, 4, 0, 1, 2)
        Hyperspectral_Layout.addWidget(self.HyperStart, 5, 0)
        Hyperspectral_Layout.addWidget(self.HyperStop, 5, 1)

        Hyperspectral_Box.setLayout(Hyperspectral_Layout)
        # endregion

        # region SAVE DATA
        Data_Box = QGroupBox("Save Data")
        Data_Layout = QGridLayout()

        self.SaveInitialTxt = QPushButton("Save Image (txt)")
        self.SaveCubeNpy = QPushButton("Save Cube (npy)")
        self.SaveCubeTxt = QPushButton("Save Cube (txt)")

        Data_Layout.addWidget(self.SaveInitialTxt, 0, 0)
        Data_Layout.addWidget(self.SaveCubeNpy, 0, 1)
        Data_Layout.addWidget(self.SaveCubeTxt, 0, 2)

        Data_Box.setLayout(Data_Layout)
        # endregion

        Settings_Layout.addWidget(InitialImage_Box)
        Settings_Layout.addWidget(RegionOfInterest_Box)
        Settings_Layout.addWidget(Hyperspectral_Box)
        Settings_Layout.addWidget(Data_Box)

        Settings_Box.setLayout(Settings_Layout)
        # endregion

        # region PLOTS

        # endregion

        MainWidget_Layout.addWidget(Settings_Box, 0, 0)

        # Set main widget
        MainWidget.setLayout(MainWidget_Layout)
        self.setCentralWidget(MainWidget)
        self.resize(CONFIG['INTERFACE_WIDTH'], CONFIG['INTERFACE_HEIGHT'])




app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
