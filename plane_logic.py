import random as r
import math
import pygame
import sys


class PlaneLogic:
    def __init__(self):
        self.map_size = (10000, 10000, 5000)  # width, length, height
        self.start_position = self.generate_start_position()
        self.plane_speed = self.generate_plane_speed()
        self.current_fuel = 10800  # fuel for 3h
        self.target_air_corridor = (6000, 6000, 0)  # air corridor location
        self.current_position = self.start_position


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
            z = r.randint(2000, height)
        elif edge == 'bottom':
            x = r.randint(0, width)
            y = r.randint(length - edge_width, length)
            z = r.randint(2000, height)
        elif edge == 'left':
            x = r.randint(0, edge_width)
            y = r.randint(0, length)
            z = r.randint(2000, height)
        elif edge == 'right':
            x = r.randint(width - edge_width, width)
            y = r.randint(0, length)
            z = r.randint(2000, height)

        return x, y, z

    def generate_plane_speed(self):
        return r.randint(10, 100)

    def update_plane_position(self):
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

        self.current_fuel -= 1

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
        if self.distance_to(other_position) <= 20:
            return True
        if self.current_fuel <= 0:
            return True
        return False



if __name__ == "__main__":
    pygame.init()
    plane_logic = PlaneLogic()
    plane_logic.pygame_loop()
