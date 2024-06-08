import time
import numpy as np
from Config import CONFIG
from scipy.interpolate import CubicSpline
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches


def drawSquareOnPlot(event, window):
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

# Precision delay function using time.perf_counter_ns
def delay_ns(ns, t=time.perf_counter_ns):
    n = t()
    e = n + ns
    while n < e:
        n = t()

# global rounding function
def preciseRound(v):
    iv = int(v)
    diff = v - iv
    return int(v + 1) if diff > 0.5 else iv

def mirror_correction(wavenumber):
    spl_x = CubicSpline(CONFIG['WAVENUMBER_CAL'], CONFIG['X_MOTOR'])
    spl_y = CubicSpline(CONFIG['WAVENUMBER_CAL'], CONFIG['Y_MOTOR'])
    return float(spl_x(wavenumber)), float(spl_y(wavenumber))

def setup_camera(camera):
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

def getInitialImage(window):
    window.Worker_Initial.start()

def getLiveImage(window):
    window.Worker_Live.start()

def getHyperCube(window):
    window.Worker_Hyper.start()


