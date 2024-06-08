import json
import os
import time
import numpy as np
from Config import CONFIG
from scipy.interpolate import CubicSpline
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
from datetime import datetime as dt

# Creating the splines, so they can be used by mirror_correction without recalculating
spl_x = CubicSpline(CONFIG['WAVENUMBER_CAL'], CONFIG['X_MOTOR'])
spl_y = CubicSpline(CONFIG['WAVENUMBER_CAL'], CONFIG['Y_MOTOR'])

def drawSquareOnPlot(event, window):
    """
    When InitialImage is clicked, draws a square based on event click coordinates
    :type window: Interface.MainWindow
    """
    if not event.inaxes:
        return
    x, y = int(event.xdata), int(event.ydata)

    # Calculate limits of the rectangle and data
    square_size = window.SquareSize.currentData()
    square_size_halved = square_size / 2
    x1, x2 = x - square_size_halved, x + square_size_halved
    y1, y2 = y - square_size_halved, y + square_size_halved

    # Check if the rectangle is inside the image, if not adjust the limits
    if x + square_size_halved > CONFIG['IMAGE_SIZE']:
        x1 = CONFIG['IMAGE_SIZE'] - square_size
        x2 = CONFIG['IMAGE_SIZE']
    if y + square_size_halved > CONFIG['IMAGE_SIZE']:
        y1 = CONFIG['IMAGE_SIZE'] - square_size
        y2 = CONFIG['IMAGE_SIZE']
    if x - square_size_halved < 0:
        x1 = 0
        x2 = square_size
    if y - square_size_halved < 0:
        y1 = 0
        y2 = square_size

    # Convert to int
    x1, x2 = int(x1), int(x2)  # updated x1 and x2 values after defining new ROI
    y1, y2 = int(y1), int(y2)  # updated y1 and y2 values after defining new ROI

    window.PictureArea = (x1, x2, y1, y2)

    for patch in window.Initial_Axes.patches:
        patch.remove()
    window.Initial_Axes.add_patch(
            patches.Rectangle((x1, y1), square_size, square_size, zorder=100, alpha=1, facecolor='none', edgecolor=CONFIG['SQUARE_COLOR'],
                              linewidth=2))
    window.Initial_Canvas.draw()
def drawPatch(window, x1, y1):
    """
    Draws a square on InitialImage
    :type window: Interface.MainWindow
    """
    for patch in window.Initial_Axes.patches:
        patch.remove()
    window.Initial_Axes.add_patch(
            patches.Rectangle((x1, y1), window.SquareSize.currentData(), window.SquareSize.currentData(), zorder=100, alpha=1, facecolor='none', edgecolor=CONFIG['SQUARE_COLOR'],
                              linewidth=2))
    window.Initial_Canvas.draw()
def resetSquareOnPlot(window):
    """
    Removes Squares from Initial image
    :type window: Interface.MainWindow
    """
    for patch in window.Initial_Axes.patches:
        patch.remove()
    window.PictureArea = None
    window.Initial_Canvas.draw()
def updateShutterspeed(window):
    """
    Updated Photron shutterspeed
    :type window: Interface.MainWindow
    """

    newSpeed = 500000
    match window.Shutterspeed.currentData():
        case 333:
            newSpeed = 3000000
        case 500:
            newSpeed = 2000000
        case 1000:
            newSpeed = 1000000
        case 2000:
            newSpeed = 500000
    log(f'Changing shutterspeed to {newSpeed} fps...')

    if CONFIG['INSTRUMENTS_MISSING']:
        return

    window.camera.setShutterSpeed(speed_in_fps=newSpeed)
    log('Shutterspeed updated')
# Precision delay function using time.perf_counter_ns
def delay_ns(ns, t=time.perf_counter_ns):
    n = t()
    e = n + ns
    while n < e:
        n = t()
# global preciseRounding function
def preciseRound(v):
    """
    Custom round function
    """
    iv = int(v)
    diff = v - iv
    return int(v + 1) if diff > 0.5 else iv
def mirror_correction(wavenumber):
    return float(spl_x(wavenumber)), float(spl_y(wavenumber))
def take_image(window, starting_wave, frames, x1, x2, y1, y2):
    """
    Returns an image taken from a Photron camera
    :type window: Interface.MainWindow
    """
    new_x, new_y = mirror_correction(starting_wave)

    try:
        window.conex1.move_absolute(new_x)
    except:
        print("Movement skipped for x")
    try:
        window.conex2.move_absolute(new_x)
    except:
        print("Movement skipped for y")

    current_wl = preciseRound(
        json.loads(window.ff3.wavelength_status())['message']['parameters']['current_wavelength'][0])
    window.ff3.go_to_wavelength(starting_wave)

    while abs(current_wl - starting_wave) > 1:
        current_wl = preciseRound(
            json.loads(window.ff3.wavelength_status())['message']['parameters']['current_wavelength'][0])

    image = window.camera.returnFinalImage_Linda(frames, starting_wave, Mod=True, Flip=True, x1=x1, x2=x2,
                                                      y1=y1, y2=y2)

    return image
def setup_camera(camera):
    """
    Sets up Photron camera
    :type camera: Interface.MainWindow.camera
    """
    log('Camera setup...')
    # Set external sync mode
    camera.setExternalInMode()
    # Set sync delay in μsec
    camera.setSyncInDelay(delay=CONFIG['CAMERA_SyncInDelay_μsec'])
    # 22900 Set shutter speed in fps (333 ns integration time per frame) before was 3_000_000. If the speed is set in
    # nanosec we should put 300ns. The minimum is 200ns.  1/fps
    camera.setShutterSpeed(speed_in_fps=CONFIG['CAMERA_Speed_fps'])
    # Set resolution
    camera.setResolution(size=CONFIG['CAMERA_Resolution_pixel'])
    camera.intShading()
    log('Camera setup finished')
def getInitialImage(window):
    """
    Starts WorkerInitial
    :type window: Interface.MainWindow
    """
    window.Worker_Initial.start()
def getLiveImage(window):
    """
    Starts WorkerLive
    :type window: Interface.MainWindow
    """
    window.Worker_Live.start()
def stopLiveImage(window):
    """
    Stops WorkerLive
    :type window: Interface.MainWindow
    """
    window.StopLive = True
    log('Stopping live imaging...')
def getHyperCube(window):
    """
    Starts HyperWorker
    :type window: Interface.MainWindow
    """
    window.StopHyper = False
    window.Worker_Hyper.start()
def stopHyperCube(window):
    """
    Sends a signal to the WorkerHyper to stop
    :type window: Interface.MainWindow
    """
    window.StopHyper = True
    log('Stopping hyperspectral imaging...')
def saveDataTxt(window, data, directory, filename):
    """
    Saves data into a txt file with every value and corresponding indexes
    :type window: Interface.MainWindow
    """
    if data is None:
        return log('No data found to export')

    result = []
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            z = data[y, x]
            result.append((x, y, z))

    cur_time = dt.now()
    dir_name = f"{CONFIG['SAVING_ROOT']}\\{directory}\\{cur_time.year}/{cur_time.month}/{cur_time.day}"
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name, exist_ok=True)

    np.savetxt(f"{dir_name}\\{filename}@{cur_time.hour:02d}-{cur_time.minute:02d}-{cur_time.second:02d}.txt", result, fmt='%s')
    log('Data saved as txt file')
def saveDataNpy(window, data, directory, filename):
    """
    Saves data as a npy extended file
    :type window: Interface.MainWindow
    """
    if data is None:
        return log('No data found to export')
    cur_time = dt.now()
    dir_name = f"{CONFIG['SAVING_ROOT']}\\{directory}\\{cur_time.year}/{cur_time.month}/{cur_time.day}"
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name, exist_ok=True)

    np.save(f"{dir_name}\\{filename}@{cur_time.hour:02d}-{cur_time.minute:02d}-{cur_time.second:02d}.npy", data)
    log('Data saved as npy file')
def saveCubeTxt(window, data, directory, filename):
    """
    Saves hypercube data into a txt file with every value and corresponding wavelength
    :type window: Interface.MainWindow
    """
    if data is None:
        return log('No data found to export')
    wavenumber_start = int(window.WavenumberMin.value())
    wavenumber_stop = int(window.WavenumberMax.value())
    step = int(window.Step.currentData())
    wavelengths = [*range(wavenumber_start, wavenumber_stop, step), wavenumber_stop]
    result = []
    for f in range(data.shape[0]):
        for x in range(data.shape[1]):
            for y in range(data.shape[2]):
                z = data[f, x, y]
                result.append((f, wavelengths[f], x, y, z))

    cur_time = dt.now()
    dir_name = f"{CONFIG['SAVING_ROOT']}\\{directory}\\{cur_time.year}/{cur_time.month}/{cur_time.day}"
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name, exist_ok=True)

    np.savetxt(f"{dir_name}\\{filename}@{cur_time.hour:02d}-{cur_time.minute:02d}-{cur_time.second:02d}.txt", result, fmt='%s')
    log('HyperCube saved as txt file')
def hyperCheckChanged(window):
    """
    Disbales and enables buttons on HyperCheck change
    :type window: Interface.MainWindow
    """
    if window.HyperCheck.isChecked():
        window.WavenumberMax.setEnabled(True)
        window.Step.setEnabled(True)
    else:
        window.WavenumberMax.setEnabled(False)
        window.Step.setEnabled(False)
def log(message):
    """
    Centralised message logging
    :type message: string
    """
    if CONFIG['DEBUG']:
        print(message)
