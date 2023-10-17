import math
from Settings import *
from UIManager import BONUS_IMAGES
import images


class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.transform.smoothscale(
            pygame.image.load('images/player.png'), PLAYER_SIZE)
        self.image = self.original_image

        self.original_image.set_colorkey(BLACK)

        if level != 1:
            self.pos = SCREEN_CENTER
        else:
            self.pos = (530, 330)

        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        x, y = pygame.mouse.get_pos()
        rel_x = x - self.rect.x
        rel_y = y - self.rect.y

        self.angle = (180 / math.pi) * (-math.atan2(rel_y, rel_x)) + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)


class Finish(pygame.sprite.Sprite):
    def __init__(self, path, balls, agg_score):
        pygame.sprite.Sprite.__init__(self)

        self.balls = balls
        self.agg_score = agg_score

        self.img = pygame.transform.smoothscale(pygame.image.load("images/star.png"), (80, 80))
        self.img.set_colorkey(BLACK)
        self.rect = self.img.get_rect(center=path.positions[-1])

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def update(self):
        for ball in self.balls:
            if self.rect.colliderect(ball.rect):
                self.agg_score.lose()


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, pos_in_path, path):
        pygame.sprite.Sprite.__init__(self)
        self.can_move = True
        self.pos_in_path = pos_in_path
        self.path = path
        self.bonus = None
        self.color = color

        self.image = pygame.Surface(BALL_SIZE)
        self.coords = self.path.positions[self.pos_in_path]
        self.rect = self.image.get_rect(center=(round(self.coords.x),
                                                round(self.coords.y)))

    def __eq__(self, other):
        return self.rect.center == other.rect.center and \
               self.can_move == other.can_move and \
               self.color == other.color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)
        if self.bonus is not None:
            screen.blit(pygame.image.load(
                BONUS_IMAGES[self.bonus][self.color]),
                (self.rect.x, self.rect.y))

    def move(self, distance):
        self.pos_in_path += distance
        if self.pos_in_path < 0:
            return

        self.coords = pygame.math.Vector2(self.path.positions[self.pos_in_path])
        self.rect.center = (round(self.coords.x), round(self.coords.y))

    def update(self):
        if self.can_move:
            self.move(1)

    def take_coords(self, pos):
        self.pos_in_path = pos
        self.coords = self.path.positions[self.pos_in_path]
        self.rect.center = (round(self.coords.x), round(self.coords.y))

    def take_bonus(self, bonus):
        self.bonus = bonus


class ShootingBall(pygame.sprite.Sprite):
    def __init__(self, color, pos=SCREEN_CENTER):
        self.speed = 15
        pygame.sprite.Sprite.__init__(self)
        self.target = (0, 0)
        self.time = None
        self.image = pygame.Surface(BALL_SIZE)
        self.color = color

        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)

    def set_target(self, t):
        self.target = (t[0] - self.rect.center[0], t[1] - self.rect.center[1])
        l = math.hypot(*self.target)
        self.target = (self.target[0] / l, self.target[1] / l)

    def update(self):
        self.rect.center = (self.rect.center[0] + self.target[0] * self.speed,
                            self.rect.center[1] + self.target[1] * self.speed)

    def set_time(self, t):
        self.time = t
