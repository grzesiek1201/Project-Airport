import random as r
import math
import pygame
import sys
import time

class AirportLogic:
    def __init__(self):
        self.map_size = (100000, 100000, 10000)  # width, length, height
        self.air_corridor = [(50000, 35000, 5000), (50000, 60000, 0)]  # Start and end of air corridor
        self.no_fly_zone_center = self.air_corridor[1]  # Center of the no-fly zone
        self.no_fly_zone_radius = (9000, 9000, 5000)  # Radius of the no-fly zone
        self.checkpoints = self.generate_checkpoints()

    def generate_checkpoints(self):
        cx, cy, cz = self.no_fly_zone_center
        rx, ry, rz = self.no_fly_zone_radius
        # Generate checkpoints around the no-fly zone
        return [
            (cx - rx, cy - ry, cz),
            (cx + rx, cy - ry, cz),
            (cx + rx, cy + ry, cz),
            (cx - rx, cy + ry, cz)
        ]

    def is_within_air_corridor(self, position):
        x, y, z = position
        (start_x, start_y, start_z), (end_x, end_y, end_z) = self.air_corridor
        return start_x <= x <= end_x and start_y <= y <= end_y and end_z <= z <= start_z

    def is_within_no_fly_zone(self, position):
        x, y, z = position
        cx, cy, cz = self.no_fly_zone_center
        rx, ry, rz = self.no_fly_zone_radius
        return cx - rx <= x <= cx + rx and cy - ry <= y <= cy + ry and cz - rz <= cz + rz

    def get_next_checkpoint(self, current_position):
        # Find the nearest checkpoint
        checkpoints = self.checkpoints
        distances = [self.calculate_distance(current_position, cp) for cp in checkpoints]
        return checkpoints[distances.index(min(distances))]

    def calculate_distance(self, pos1, pos2):
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

class PlaneLogic:
    def __init__(self, airport_logic):
        self.airport_logic = airport_logic
        self.map_size = self.airport_logic.map_size
        self.start_position = self.generate_start_position()
        self.plane_speed = self.generate_plane_speed()
        self.current_fuel = 10800  # fuel for 3h
        self.target_air_corridor = self.airport_logic.air_corridor[0]  # Start of air corridor
        self.current_position = self.start_position
        self.in_air_corridor = False  # Indicates if the plane is in the air corridor
        self.avoiding_no_fly_zone = False  # Indicates if the plane is avoiding the no-fly zone

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Project Airport")

        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (800, 600))

        self.blink = True
        self.blink_timer = 0

    def pygame_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            self.update_plane_position()
            self.draw_plane()
            pygame.display.flip()

            clock.tick(60)

    def generate_start_position(self):
        edge_width = 100
        width, length, height = self.map_size

        edge = r.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            x = r.randint(0, width)
            y = r.randint(0, edge_width)
            z = r.randint(2000, 5000)
        elif edge == 'bottom':
            x = r.randint(0, width)
            y = r.randint(length - edge_width, length)
            z = r.randint(2000, 5000)
        elif edge == 'left':
            x = r.randint(0, edge_width)
            y = r.randint(0, length)
            z = r.randint(2000, 5000)
        elif edge == 'right':
            x = r.randint(width - edge_width, width)
            y = r.randint(0, length)
            z = r.randint(2000, 5000)

        return x, y, z

    def generate_plane_speed(self):
        return r.randint(300, 800)

    def update_plane_position(self):
        if self.airport_logic.is_within_no_fly_zone(self.current_position) and not self.in_air_corridor:
            self.avoiding_no_fly_zone = True
            self.target_air_corridor = self.airport_logic.get_next_checkpoint(self.current_position)
        elif self.is_near_target(self.airport_logic.air_corridor[0]):
            self.in_air_corridor = True
            self.avoiding_no_fly_zone = False  # Stop avoiding no-fly zone once in air corridor
            self.target_air_corridor = self.airport_logic.air_corridor[1]

        self.move_towards_target()
        self.current_fuel -= 1

    def move_towards_target(self):
        x, y, z = self.current_position
        tx, ty, tz = self.target_air_corridor

        dx = tx - x
        dy = ty - y
        dz = tz - z

        dist = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        if dist > 0:
            dx /= dist
            dy /= dist
            dz /= dist

            self.current_position = (
                x + dx * self.plane_speed,
                y + dy * self.plane_speed,
                z + dz * self.plane_speed
            )

    def is_near_target(self, target, tolerance=500):
        tx, ty, tz = target
        x, y, z = self.current_position
        return math.isclose(x, tx, abs_tol=tolerance) and \
               math.isclose(y, ty, abs_tol=tolerance) and \
               math.isclose(z, tz, abs_tol=tolerance)

    def draw_plane(self):
        x, y, _ = self.current_position
        screen_x = int(x * self.screen.get_width() / self.map_size[0])
        screen_y = int(y * self.screen.get_height() / self.map_size[1])

        self.blink_timer += 1
        if self.blink_timer >= 30:
            self.blink = not self.blink
            self.blink_timer = 0

        color = (255, 0, 0) if self.blink else (0, 0, 0)
        pygame.draw.circle(self.screen, color, (screen_x, screen_y), 5)

    def distance_to(self, other_position):
        x1, y1, z1 = self.current_position
        x2, y2, z2 = other_position
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

    def collision_confirm(self, other_position):
        return self.airport_logic.is_within_no_fly_zone(self.current_position) or self.current_fuel <= 0


if __name__ == "__main__":
    airport_logic = AirportLogic()
    plane_logic = PlaneLogic(airport_logic)
    plane_logic.pygame_loop()
