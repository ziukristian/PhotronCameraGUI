import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and size of the main window
        self.setWindowTitle("Matplotlib Imshow in PyQt6")
        self.setGeometry(100, 100, 800, 600)

        # Create a widget for the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout(central_widget)

        # Create a Matplotlib figure and add a subplot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Add the canvas to the layout
        layout.addWidget(self.canvas)

        # Create and display an imshow plot
        self.display_imshow_plot()

    def display_imshow_plot(self):
        # Create a sample image (for example purposes, using a random matrix)
        data = np.random.random((10, 10))

        # Clear the axes and display the image
        self.ax.clear()
        self.ax.imshow(data, cmap='viridis')

        # Refresh the canvas
        self.canvas.draw()

# Set up the application loop
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
