import numpy as np

CONFIG = {
    'WINDOW_TITLE': 'IR-PHI ToolBox',
    'ICON_PATH': 'Misc/logo.svg',
    'INTERFACE_WIDTH': 1600,
    'INTERFACE_HEIGHT': 600,
    'IMAGE_SIZE': 512,
    'SQUARE_COLOR': 'black',
    'SQUARE_SIZES': [512, 256, 128, 62],
    'HYPER_STEPS': [2, 4, 5, 10],
    'SHUTTERSPEED_OPTIONS_NS': [333, 500, 1000, 2000],
    'WAVENUMBER_CAL': np.array([1041, 1075, 1100, 1125, 1150, 1175, 1200, 1225, 1250, 1275, 1300, 1325, 1350, 1375, 1400, 1425, 1450, 1475, 1500, 1525, 1550, 1575, 1600, 1625, 1650, 1675, 1700, 1725, 1750, 1775, 1800, 1825, 1840]),
    'X_MOTOR': np.array([3.026, 3.015, 3.015, 3.011, 3.008, 3.008, 3.008, 3.012, 3.015, 3.007, 3.009, 3.006, 3.006, 3.004, 3.006, 3.008, 3.009, 3.013, 3.014, 3.012, 3.008, 3.009, 3.007, 3.005, 3.002, 3.002, 3.003, 2.979, 2.970, 2.961, 2.962, 2.966, 2.968]),
    'Y_MOTOR': np.array([0.991, 0.994, 0.993, 0.995, 0.993, 0.995, 0.996, 0.991, 0.990, 0.990, 0.990, 0.99165, 0.99165, 0.9914, 0.9913, 0.989, 0.988, 0.987, 0.987, 0.986, 0.986, 0.985, 0.987, 0.985, 0.9845, 0.985, 0.982, 0.985, 0.9837, 0.9839, 0.986, 0.9837, 0.9837]),
    'CAMERA_SyncInDelay_μsec': 24.3,
    'CAMERA_Speed_fps': 500000,
    'CAMERA_Resolution_pixel': (512, 512),
    'CMAPS': ['bwr'],
    'PLOT_TITLESIZE': 10,
    'PLOT_LABELSIZE': 9,
    'PLOT_TICKERSIZE': 9,
    'SAVING_ROOT': 'Measurements',
    'DEBUG': True,  # Set to true if you want console logs
    'INSTRUMENTS_MISSING': True,  # Set to true if you're not in the lab
}
