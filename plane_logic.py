import random as r


class PlaneLogic:
    def __init__(self):
        self.map_size = (10000, 10000, 5000)  # width, length, height
        self.start_position = self.generate_start_position()
        self.plane_speed = 0
        self.start_fuel = 10800  # fuel for 3h
        self.target_air_corridor = (6000, 6000, 0)  # air corridor location

    def generate_start_position(self):
        edge_width = 100
        width, length, height = self.map_size

        edge = r.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            x = r.randint(0, width)
            y = r.randint(0, edge_width)
        elif edge == 'bottom':
            x = r.randint(0, width)
            y = r.randint(height - edge_width, height)
        elif edge == 'left':
            x = r.randint(0, edge_width)
            y = r.randint(0, height)
        elif edge == 'right':
            x = r.randint(width - edge_width, width)
            y = r.randint(0, height)

        return x, y

    def fuel_management(self):
        self.current_fuel = self.start_fuel

    def generate_plane_speed(self):
        self.plane_speed = r.randint(10, 100)

    def collision_confirm(self):
        if self.plane_distance <= 20:
            return True
        if self.current_fuel <= 0:
            return True
