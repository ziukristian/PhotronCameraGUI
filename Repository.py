import time
from Config import CONFIG
from scipy.interpolate import CubicSpline


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
