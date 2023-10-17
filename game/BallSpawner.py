from Settings import *
from Sprites import Ball
import random


class BallSpawner:
    def __init__(self, path, number, score_manager):
        self.pause = False
        self.balls = []
        self.path = path
        self.score_manager = score_manager
        self.n_to_gen = number

        self.reverse = False

        self.count_generated = 0

        self.colors = [BLUE, RED, GREEN, YELLOW]

    def update(self):
        self.chain_upd()

        if self.count_generated == self.n_to_gen and len(self.balls) == 0:
            self.score_manager.win()

        if not (self.pause or self.reverse):
            self.balls_upd()

    def conv_ball_shoot(self, index, ball_shoot):
        b = Ball(ball_shoot.color, self.get_next_position(index), self.path)
        b.can_move = self.balls[index].can_move
        return b

    def del_balls(self, chain):
        for ball in chain:
            self.balls.remove(ball)

    def merge_balls(self, index):
        for i in range(index, len(self.balls)):
            self.balls[i].take_coords(self.get_next_position(i - 1))

    def stop_movement(self, tail_index):
        for i in range(tail_index, len(self.balls)):
            self.balls[i].can_move = False

    def get_next_position(self, index):
        return BALL_RADIUS // self.path.step * 2 + self.balls[index].pos_in_path

    def gen_balls(self):
        if self.n_to_gen > self.count_generated:
            if len(self.balls) == 0 or BALL_RADIUS // self.path.step * 2 <= self.balls[0].pos_in_path:
                self.balls.insert(0, Ball(random.choice(self.colors), 0,
                                          self.path))
                self.count_generated += 1

    def balls_upd(self):
        for ind in range(len(self.balls)):
            self.balls[ind].update()
            self.move_after_stop(ind)

    def chain_upd(self):
        for ind in range(1, len(self.balls)):
            ball_l = self.balls[ind - 1]
            ball_r = self.balls[ind]
            if ball_r.pos_in_path - (20 + ball_l.pos_in_path) <= 0:
                continue
            else:
                if ball_r.color != ball_l.color:
                    self.stop_movement(ind)
                else:
                    self.merge_balls(ind - 1)

    def insertion(self, index, shooting_ball):
        b = self.conv_ball_shoot(index, shooting_ball)
        self.balls.insert(index + 1, b)
        for i in range(index + 2, len(self.balls)):
            if BALL_RADIUS // self.path.step * 2 > self.balls[i].pos_in_path - self.balls[i - 1].pos_in_path:
                self.balls[i].take_coords(self.get_next_position(i - 1))
            else:
                break

    def move_after_stop(self, ind):
        if not self.balls[ind].can_move:
            if ind != 0 and self.balls[ind - 1].can_move and \
                    self.balls[ind - 1].rect.colliderect(self.balls[ind].rect):
                self.balls[ind].can_move = True
            elif ind == 0:
                self.balls[ind].can_move = True

    def get_curr_colors(self):
        return [ball.color for ball in self.balls]

    def draw(self, screen):
        for b in self.balls:
            b.draw(screen)