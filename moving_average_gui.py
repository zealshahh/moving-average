import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from calc_average import get_moving_average, get_API_key  

class MovingAverageApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # set up GUI window and input fields 
        self.setWindowTitle("Moving Average Plotter")
        self.setGeometry(100, 100, 800, 600)
        self.ticker_label = QLabel("Ticker symbol:")
        self.ticker_input = QLineEdit()
        self.days_label = QLabel("Days in one period:")
        self.days_input = QLineEdit()
        self.periods_label = QLabel("Number of periods:")
        self.periods_input = QLineEdit()
        self.plot_button = QPushButton("Click to plot your moving average!")
        self.plot_button.clicked.connect(self.plot_moving_average)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        # regular vertical widget layout
        layout = QVBoxLayout() 
        layout.addWidget(self.ticker_label)
        layout.addWidget(self.ticker_input)
        layout.addWidget(self.days_label)
        layout.addWidget(self.days_input)
        layout.addWidget(self.periods_label)
        layout.addWidget(self.periods_input)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_moving_average(self):
        
        ticker = self.ticker_input.text()
        try:
            days_in_period = int(self.days_input.text())
            num_periods = int(self.periods_input.text())
        except ValueError:
            self.show_error("Try again! Days and periods must be integers.")
            return
        
        API_key = get_API_key() # gets API key from calc.py 

        result = get_moving_average(API_key, ticker, days_in_period, num_periods)

        if isinstance(result, str):  # if the result is an error 
            self.show_error(result)
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(result, marker='o', linestyle='-', color='pink', label="Moving Average")
        ax.set_title(f"Moving Average of {ticker}")
        ax.set_xlabel("Periods")
        ax.set_ylabel("Moving Average")
        ax.legend()
        self.canvas.draw()

    def show_error(self, message):
        error_label = QLabel(f"Error: {message}")
        self.layout().addWidget(error_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovingAverageApp()
    window.show()
    sys.exit(app.exec_())
