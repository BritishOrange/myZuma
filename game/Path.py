import math
from Settings import *


class MapAggregator:
    def __init__(self, level):
        self.positions = []
        self.step = 2
        self.targets = []
        self.choose_map(level)

    def draw(self, screen):
        for i in range(len(self.targets) - 1):
            pygame.draw.line(screen, DARK_TAUPE, self.targets[i],
                             self.targets[i + 1], 10)

    def switch_dir(self, ind_t, coords):
        dir = pygame.math.Vector2(
            (self.targets[ind_t][0] - coords[0],
             self.targets[ind_t][1] - coords[1]))
        l = math.hypot(*dir)
        dir = pygame.math.Vector2((dir[0] / l, dir[1] / l))

        return dir

    def take_coords(self):
        coords = pygame.math.Vector2(self.targets[0])
        dir = pygame.math.Vector2((0, 0))

        ind_t = 0

        while len(self.targets) > ind_t:
            coords = coords + (dir * self.step)
            self.positions.append(coords)

            if self.targets[ind_t] == (round(coords.x), round(coords.y)):
                ind_t += 1
                if ind_t != len(self.targets):
                    dir = self.switch_dir(ind_t, coords)
                else:
                    break

    def take_spiral(self):
        self.targets = [(64, 0), (64, 416), (99, 492), (153, 559), (222, 607),
                        (301, 637), (382, 645), (461, 631), (536, 597),
                        (598, 546), (644, 481), (671, 406), (679, 330),
                        (665, 254), (634, 186), (586, 128), (524, 84),
                        (454, 58), (383, 51), (312, 64), (246, 94), (193, 140),
                        (151, 198), (127, 262), (121, 331), (133, 396),
                        (162, 458), (204, 508), (259, 546), (319, 567),
                        (383, 573), (444, 561), (500, 535), (547, 495),
                        (583, 444), (602, 389), (607, 330), (596, 273),
                        (571, 220), (534, 178), (488, 146), (435, 128),
                        (382, 123), (330, 133), (282, 156), (242, 190),
                        (214, 233), (197, 281), (193, 330), (203, 377),
                        (224, 421), (255, 457), (303, 470), (345, 469),
                        (383, 456), (409, 434), (427, 407), (432, 380),
                        (428, 356), (417, 340), (339, 330)]
        self.take_coords()

    def take_triangle(self):
        self.targets = [(80, 0), (80, HEIGHT - 80), (WIDTH - 80, HEIGHT - 80),
                        (400, 80), (160, 460), (WIDTH - 280, 460)]
        self.take_coords()

    def take_square(self):
        self.targets = [(0, 80), (WIDTH - 80, 80), (WIDTH - 80, HEIGHT - 80),
                   (80, HEIGHT - 80), (80, 140), (WIDTH - 160, 140),
                   (WIDTH - 160, HEIGHT - 160), (160, HEIGHT - 160),
                   (160, 340)]
        self.take_coords()

    def choose_map(self, level):
        if level == 3:
            self.take_triangle()
        elif level == 1:
            self.take_square()
        else:
            self.take_spiral()
