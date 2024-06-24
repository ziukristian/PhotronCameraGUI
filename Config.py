import numpy as np

CONFIG = {
    'WINDOW_TITLE': 'IR-PHI ToolBox',
    'ICON_PATH': 'Misc/logo.svg',
    'INTERFACE_WIDTH': 1900,
    'INTERFACE_HEIGHT': 800,
    'IMAGE_SIZE': 512,
    'SQUARE_COLOR': 'black',
    'SQUARE_SIZES': [512, 256, 128, 62, 40],
    'HYPER_STEPS': [2, 4, 5, 10],
    'SHUTTERSPEED_OPTIONS_NS': [333, 500, 1000, 2000],
    'WAVENUMBER_CAL': np.array([1075,  1100,  1125,  1150,  1175,   1200,   1225,   1250,  1275,   1300,    1325,   1350,  1375,   1400,   1425,   1450,   1475,   1500,   1525,   1550,   1575,   1600,   1625,  1650,   1675,   1700,   1725,   1727,   1750,   1775,   1800,   1825,    1840]),
    'X_MOTOR': np.array([      3.005, 3.005, 2.999, 2.993, 2.995,  2.997,  2.998,  2.998, 2.999,  3.000,   3.000,  2.998, 2.997,  2.997,  2.998,  3.000,  3.003,  3.005, 3.0015,  3.000,  3.000,  2.999,  3.001, 2.994,  2.994, 2.9945,  2.972,  2.970,  2.960,  2.952,  2.956,  2.962,  2.9645]),
    'Y_MOTOR': np.array([      1.000, 1.000, 1.010, 1.010, 1.010,  1.010,  1.007,  1.006, 1.006,  1.007,  1.0065, 1.0062, 1.006, 1.0058, 1.0046,  1.000, 1.0019, 1.0016,  1.000, 0.9987, 0.9987, 0.9987, 0.9975, 0.998, 0.9978,  0.997, 0.9975,  0.997, 0.9972, 0.9974, 0.9974, 0.9974,   0.997]),
    'CAMERA_SyncInDelay_μsec': 23.1,
    'CAMERA_Speed_fps': 500000,
    'CAMERA_Resolution_pixel': (512, 512),
    'CMAPS': ['bwr'],
    'PLOT_TITLESIZE': 10,
    'PLOT_LABELSIZE': 9,
    'PLOT_TICKERSIZE': 9,
    'SAVING_ROOT': 'Measurements',
    'DEBUG': True,  # Set to true if you want console logs
    'INSTRUMENTS_MISSING': False,  # Set to true if you're not in the lab
}
