import matplotlib.pyplot as plt
import numpy as np


class Charts:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = plt.axes(projection='3d')
        self.ax.set_title('Project Airport')
        self.ax.set_xlim([0, 100000])
        self.ax.set_ylim([0, 100000])
        self.ax.set_zlim([0, 6000])

    def airport_charts(self):
        x_line1 = np.linspace(40000, 40000, 100)
        y_line1 = np.linspace(20000, 60000, 100)
        z_line1 = np.zeros_like(x_line1)
        self.ax.plot3D(x_line1, y_line1, z_line1, 'green', linewidth=2)

        x_line2 = np.linspace(20000, 20000, 100)
        y_line2 = np.linspace(20000, 60000, 100)
        z_line2 = np.zeros_like(x_line2)
        self.ax.plot3D(x_line2, y_line2, z_line2, 'blue', linewidth=2)

    def airplane_cords(self):
        

    def airplane_charts(self):
        x_point = [0.5]
        y_point = [0.5 * np.cos(25 * 0.5)]
        z_point = [0.5]
        self.ax.scatter3D(x_point, y_point, z_point, color='red', s=10)


charts = Charts()
charts.airport_charts()
charts.airplane_charts()


plt.show()
