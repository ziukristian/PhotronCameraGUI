
# PhotronCameraGUI

## Overview
PhotronCameraGUI is a Python-based graphical user interface designed to control a Photron High-Speed Camera and synchronize its operation with a FireFly Infrared Laser. This system was developed for advanced nanoparticle research at the University of Notre Dame, enabling precise experimental control and efficient data acquisition.

## Key Features
- **Multithreaded Camera Control:** Robust software architecture allows for responsive and reliable control of the Photron camera, supporting concurrent operations and minimizing latency.
- **Laser Synchronization:** Seamless integration with the FireFly Infrared Laser enables synchronized triggering and timing for complex experimental setups.
- **Real-Time Data Visualization:** Utilizes Matplotlib for live plotting and visualization of acquired data, providing immediate feedback and insight during experiments.
- **Hyperspectral Imaging Data Management:** Supports the acquisition, plotting, and management of hyperspectral imaging datasets, facilitating advanced analysis and research workflows.

## Technologies Used
- **Python** (core language)
- **Matplotlib** (real-time data visualization)
- **Multithreading** (concurrent camera and laser control)
- **Custom DLLs and C Libraries** (hardware interfacing)

## Folder Structure
- `Config.py`, `Interface.py`, `Repository.py`: Main Python modules for configuration, GUI, and data management.
- `C_Libraries/`: Contains DLLs and C source files for hardware communication.
- `Instruments_Libraries/`: Python modules for instrument-specific control and integration.
- `Measurements/`: Stores experimental data and results.
- `Misc/`: Miscellaneous files (e.g., logo, documentation).

## Usage
1. **Setup:** Ensure all required DLLs and Python dependencies are installed.
2. **Run the GUI:** Launch the main interface to connect to the camera and laser.
3. **Configure Experiment:** Set parameters for camera and laser operation.
4. **Acquire Data:** Start acquisition and monitor real-time plots.
5. **Analyze Results:** Access and plot hyperspectral imaging data for further analysis.

## Applications
- Nanoparticle research
- Hyperspectral imaging
- Synchronized high-speed imaging and laser experiments

## Author
Developed by Kristian Ziu for the University of Notre Dame.

