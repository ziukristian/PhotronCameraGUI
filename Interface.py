import json
import numpy as np
import time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from Config import CONFIG
import Repository as REPO

# Instruments
from Instruments_Libraries.Photron import PhotronCamera  # IP address: 192.168.0.10
import \
    Instruments_Libraries.Firefly_LW_2024 as Firefly  # Laser IP address: 192.168.1.231; Host computer IP address: 192.168.1.187
from Instruments_Libraries.ConexCC import ConexCC

log = REPO.log
PHOTRONCAMERA = PhotronCamera()


class Worker_Initial(QThread):
    def __init__(self, window):
        """

        :type window: MainWindow
        """
        self.window = window
        super().__init__()

    def run(self):
        log(f'Taking initial image ON {self.window.Wavenumber.value()} ({int(self.window.NumberOfFrames.value())} FRAMES) ({CONFIG['IMAGE_SIZE']}x{CONFIG['IMAGE_SIZE']} SIZE)...')

        if CONFIG['INSTRUMENTS_MISSING']:
            return

        self.window.Btn_InitialImage.setEnabled(False)
        image = REPO.take_image(self.window, self.window.Wavenumber.value(), int(self.window.NumberOfFrames.value()), 0,
                                CONFIG['IMAGE_SIZE'], 0, CONFIG['IMAGE_SIZE'])

        self.window.InitialImage = image
        self.window.Initial_Axes.imshow(image, cmap='bwr')
        self.window.Initial_Canvas.draw()
        log('Initial image taken')
        self.window.Btn_InitialImage.setEnabled(True)


class Worker_Live(QThread):
    def __init__(self, window):
        """

        :type window: MainWindow
        """
        super().__init__()
        self.window = window

    def run(self):
        log('LIVE IMAGING STARTED...')
        if CONFIG['INSTRUMENTS_MISSING']:
            return
        self.window.Btn_StartLive.setEnabled(False)
        self.window.Btn_StopLive.setEnabled(True)

        while self.window.StopLive is False:
            image = self.window.camera.getLiveImage_Mod(bufferSize=(512, 512), Flip=True, x1=0, x2=CONFIG['IMAGE_SIZE'], y1=0, y2=CONFIG['IMAGE_SIZE'])
            self.window.LiveImage = image
            self.window.Live_Axes.imshow(image, cmap='bwr')
            self.window.Live_Canvas.draw()

        self.window.StopLive = False
        self.window.Btn_StartLive.setEnabled(True)
        self.window.Btn_StopLive.setEnabled(False)


class Worker_Hyper(QThread):
    def __init__(self, window):
        """

        :type window: MainWindow
        """
        super().__init__()
        self.window = window

    def run(self):
        wavenumber_start = int(self.window.WavenumberMin.value())
        wavenumber_stop = int(self.window.WavenumberMax.value())
        step = self.window.Step.currentData()
        log(f'Starting hyperspectral imaging FROM {wavenumber_start} TO {wavenumber_stop} ({step} STEP)...')

        if CONFIG['INSTRUMENTS_MISSING']:
            return

        self.window.Btn_HyperStop.setEnabled(True)
        self.window.Btn_HyperStart.setEnabled(False)
        xmin, xmax, ymin, ymax = (0, 0, 0, 0)
        if self.window.PictureArea is None:
            log('Area not selected, setting it to center of image')
            squareSize = self.window.SquareSize.currentData()
            xmin = int((CONFIG['IMAGE_SIZE'] - squareSize) / 2)
            xmax = int((CONFIG['IMAGE_SIZE'] + squareSize) / 2)
            ymin = int((CONFIG['IMAGE_SIZE'] - squareSize) / 2)
            ymax = int((CONFIG['IMAGE_SIZE'] + squareSize) / 2)
            REPO.drawPatch(self.window, xmin, ymin)
        else:
            xmin, xmax, ymin, ymax = self.window.PictureArea
            log(f'Selected area (xmin,xmax,ymin,ymax) = {xmin, xmax, ymin, ymax}')

        if self.window.HyperCheck.isChecked():
            log('Hyperspectral is checked')
            self.window.HyperProgress.setMinimum(wavenumber_start)
            self.window.HyperProgress.setMaximum(wavenumber_stop)
            self.window.HyperProgress.setValue(wavenumber_start + 1)

            array_depth = int((self.window.WavenumberMax.value() - self.window.WavenumberMin.value()) / step)
            array_size = xmax - xmin
            self.window.HyperCube = np.empty([array_depth + 1, array_size, array_size], int)
            # [0] means tuning inactive, [1] means still tuning
            ff3_tuning_active = bytes("[1]", 'UTF-8')
            current_wl = REPO.preciseRound(json.loads(self.window.ff3.wavelength_status())[
                                   'message']['parameters']['current_wavelength'][0])
            # move Msquared laser to specified wavelength
            self.window.ff3.go_to_wavelength(wavenumber_start)
            # while current_wl = wavenumber_start - 1:
            while current_wl != wavenumber_start:
                current_wl = REPO.preciseRound(json.loads(self.window.ff3.wavelength_status())[
                                       'message']['parameters']['current_wavelength'][0])
            log(f'Wavelength {wavenumber_start}f reached')
            i = 0
            for pos in range(wavenumber_start, wavenumber_stop, step):
                log(f'Getting image for wavelength {pos}')
                if self.window.StopHyper:
                    log('Hyperspectral imaging manually stopped')
                    break
                current_wl = REPO.preciseRound(json.loads(self.window.ff3.wavelength_status())[
                                       'message']['parameters']['current_wavelength'][0])
                # move Msquared laser to specified wavelength
                self.window.ff3.go_to_wavelength(pos)
                while abs(current_wl - wavenumber_start) > 1:
                    current_wl = REPO.preciseRound(json.loads(self.window.ff3.wavelength_status())[
                                           'message']['parameters']['current_wavelength'][0])

                # MIRROR CORRECTION
                new_x, new_y = REPO.mirror_correction(pos)
                try:
                    self.window.conex1.move_absolute(new_x)
                except:
                    print("Movement skipped for x")
                try:
                    self.window.conex2.move_absolute(new_y)
                except:
                    print("Movement skipped for y")

                image = self.window.camera.returnFinalImage_Linda(
                    int(self.window.NumberOfFrames.value()), 0, Mod=True, Flip=True, x1=xmin, x2=xmax, y1=ymin, y2=ymax)
                # add data to hyperspectral data cube
                self.window.HyperCube[i, :, :] = image

                self.window.HyperProgress.setValue(pos + step)
                i = i + 1
            self.window.Hyper_Axes.imshow(self.window.HyperCube[0, :, :], cmap='bwr')
            self.window.Hyper_Canvas.draw()
            self.window.HyperProgress.reset()
        else:
            log('Hyperspectral is not checked, requesting single image')
            image = REPO.take_image(self.window, wavenumber_start,
                                    int(self.window.NumberOfFrames.value()), xmin, xmax, ymin, ymax)
            self.window.Hyper_Axes.imshow(image, cmap='bwr')
            self.window.Hyper_Canvas.draw()

        self.window.StopHyper = False
        self.window.Btn_HyperStop.setEnabled(False)
        self.window.Btn_HyperStart.setEnabled(True)
        log('Hyperspectral imaging finished')



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(CONFIG['WINDOW_TITLE'])
        self.setWindowIcon(QIcon(CONFIG['ICON_PATH']))
        self.StopHyper = False
        self.StopLive = False
        self.PictureArea = None
        self.InitialImage = None
        self.LiveImage = None
        self.HyperCube = None
        self.Worker_Initial = Worker_Initial(self)
        self.Worker_Live = Worker_Live(self)
        self.Worker_Hyper = Worker_Hyper(self)

        if CONFIG['INSTRUMENTS_MISSING'] is False:
            # PHOTRON CAMERA
            self.camera = PHOTRONCAMERA
            self.camera.getCurrentRecordSpeed()
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
        self.Wavenumber.setStyleSheet(
            "border-radius : 15; border : 1px solid white; background-color : #F2DB74;color:black")

        self.NumberOfFrames = QDoubleSpinBox()
        self.NumberOfFrames.setMinimum(1)
        self.NumberOfFrames.setMaximum(1000000)
        self.NumberOfFrames.setValue(5000)
        self.NumberOfFrames.setDecimals(0)
        self.NumberOfFrames.setSingleStep(1)
        self.NumberOfFrames.setStyleSheet(
            "border-radius : 15; border : 1px solid white; background-color : #F2DB74;color:black")

        self.Shutterspeed = QComboBox()
        for speed in CONFIG['SHUTTERSPEED_OPTIONS_NS']:
            self.Shutterspeed.addItem(f"{speed} ns", speed)
        self.Shutterspeed.setCurrentIndex(1)

        self.Btn_InitialImage = QPushButton('Acquire Initial Image')

        InitialImage_Layout.addWidget(QLabel("Wavenumber (cm-1)"), 0, 0)
        InitialImage_Layout.addWidget(self.Wavenumber, 1, 0)
        InitialImage_Layout.addWidget(QLabel("Number of frames"), 0, 1)
        InitialImage_Layout.addWidget(self.NumberOfFrames, 1, 1)
        InitialImage_Layout.addWidget(self.Shutterspeed, 2, 0, 1, 2)
        InitialImage_Layout.addWidget(self.Btn_InitialImage, 3, 0, 1, 2)

        InitialImage_Box.setLayout(InitialImage_Layout)
        # endregion

        # region LIVE IMAGE SETTINGS
        Live_Box = QGroupBox("Live Imaging")
        Live_Layout = QGridLayout()

        self.Btn_StartLive = QPushButton("Start")

        self.Btn_StopLive = QPushButton("Stop")
        self.Btn_StopLive.setEnabled(False)

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
        self.Step.setEnabled(False)

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
        self.WavenumberMax.setEnabled(False)

        self.HyperProgress = QProgressBar(self)
        self.HyperProgress.setValue(0)

        self.Btn_HyperStart = QPushButton("Start")
        self.Btn_HyperStop = QPushButton("Stop")
        self.Btn_HyperStop.setEnabled(False)

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
        self.SaveLiveImageTxt_Name = QLineEdit('FileName')
        self.Btn_SaveLiveImageTxt = QPushButton("Save Live Image (txt)")

        Data_Layout.addWidget(self.SaveInitialTxt_Name, 0, 0)
        Data_Layout.addWidget(self.SaveLiveImageTxt_Name, 0, 1)
        Data_Layout.addWidget(self.SaveCubeNpy_Name, 0, 2)
        Data_Layout.addWidget(self.SaveCubeTxt_Name, 0, 3)
        Data_Layout.addWidget(self.Btn_SaveInitialTxt, 1, 0)
        Data_Layout.addWidget(self.Btn_SaveLiveImageTxt, 1, 1)
        Data_Layout.addWidget(self.Btn_SaveCubeNpy, 1, 2)
        Data_Layout.addWidget(self.Btn_SaveCubeTxt, 1, 3)


        Data_Box.setLayout(Data_Layout)
        # endregion

        Settings_Layout.addWidget(InitialImage_Box)
        Settings_Layout.addWidget(Live_Box)
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
        self.Btn_StopLive.clicked.connect(lambda: REPO.stopLiveImage(self))
        self.Btn_HyperStart.clicked.connect(lambda: REPO.getHyperCube(self))
        self.Btn_HyperStop.clicked.connect(lambda: REPO.stopHyperCube(self))
        self.Btn_SaveInitialTxt.clicked.connect(lambda: REPO.saveDataTxt(self, self.InitialImage, 'InitialImages', self.SaveInitialTxt_Name.text()))
        self.Btn_SaveLiveImageTxt.clicked.connect(lambda: REPO.saveDataTxt(self, self.LiveImage, 'LiveImages', self.SaveLiveImageTxt_Name.text()))
        self.Btn_SaveCubeNpy.clicked.connect(lambda: REPO.saveDataNpy(self, self.HyperCube, 'wIR-PHI_spectra', self.SaveCubeTxt_Name.text()))
        self.Btn_SaveCubeTxt.clicked.connect(lambda: REPO.saveCubeTxt(self, self.HyperCube, 'wIR-PHI_spectra', self.SaveCubeNpy_Name.text()))



        self.SquareSize.currentIndexChanged.connect(lambda: REPO.resetSquareOnPlot(self))
        self.Shutterspeed.currentIndexChanged.connect(lambda: REPO.updateShutterspeed(self))
        self.HyperCheck.stateChanged.connect(lambda: REPO.hyperCheckChanged(self))
        # endregion

    def closeEvent(self, event):
        if CONFIG['INSTRUMENTS_MISSING']:
            return event.accept()
        print('CLOSE')
        self.camera.closeCamera()  # Disconnect Photron camera
        self.conex1.close()  # Disconnect Newport mirror1
        self.conex2.close()  # Disconnect Newport mirror2
        event.accept() # Close window

try:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
except:
    print('ERROR, CLOSING APPLICATION...')
    PHOTRONCAMERA.closeCamera()  # Disconnect Photron camera
    conex1 = ConexCC(com_port='COM3', velocity=0.5)  # Link to Newport motor 1
    conex2 = ConexCC(com_port='COM7', velocity=0.5)  # Link to Newport motor 2
    conex1.close()  # Disconnect Newport mirror1
    conex2.close()
