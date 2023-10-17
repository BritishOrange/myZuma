from Sprites import ShootingBall
from Settings import *
from BonusAggregator import Bonus
import random
import datetime


class ShootingAggregator:
    def __init__(self, gen_b, coords, agg_bonus, agg_score):
        self.shooting_balls = []
        self.ball_generator = gen_b
        self.combo_chain = []
        self.agg_score = agg_score
        self.agg_bonus = agg_bonus
        self.speed = False
        self.coords = coords
        self.cur_ball = ShootingBall(random.choice(
            self.ball_generator.colors), self.coords)

    def make_chain_part(self, i, d, color):
        part = []
        while 0 <= i < len(self.ball_generator.balls) and \
                self.ball_generator.balls[i].color == color:
            part.append(self.ball_generator.balls[i])
            i += d

        return part

    def reload(self):
        return ShootingBall(random.choice(self.ball_generator.get_curr_colors()), self.coords)

    def draw(self, screen):
        self.cur_ball.draw(screen)
        for b in self.shooting_balls:
            b.draw(screen)

    def update(self):
        self.speed = self.agg_bonus.aggregate_speed()
        self.cur_ball.update()
        for b in self.shooting_balls:
            b.update()
            self.aggregate_shooting(b)
            self.delete_out(b)

    def delete_out(self, b):
        y = b.rect.center[1]
        x = b.rect.center[0]
        if y < 0 or WIDTH < x or x < 0 or y > HEIGHT:
            self.shooting_balls.remove(b)

    def aggregate_shooting(self, curr_b):
        for b in self.ball_generator.balls:
            if curr_b.rect.colliderect(b.rect):
                chain = self.make_chain(b, curr_b.color)
                if len(chain) <= 1:
                    ind_b = self.ball_generator.balls.index(b)
                    self.ball_generator.insertion(ind_b, curr_b)
                else:
                    chain += self.is_bonus_in_chain(chain)
                    self.agg_score.increase_score(10 * len(chain))
                    self.ball_generator.del_balls(chain)
                    if self.cur_ball.color not in self.ball_generator.get_curr_colors() and \
                            len(self.ball_generator.balls) != 0:
                        self.cur_ball = self.reload()
                self.shooting_balls.remove(curr_b)
                break

    def is_bonus_in_chain(self, chain):
        for b in chain:
            if b.bonus is None:
                continue
            else:
                if b.bonus is Bonus.Speed:
                    self.agg_bonus.run_bonus(b.bonus)
                    self.speed = True
                elif b.bonus is Bonus.Bomb:
                    return self.agg_bonus.aggregate_bomb(chain)
                else:
                    self.agg_bonus.run_bonus(b.bonus)
        return []

    def make_chain(self, b, color):
        ind_b = self.ball_generator.balls.index(b)
        color_b = b.color

        right = self.make_chain_part(ind_b + 1, 1, color)
        left = self.make_chain_part(ind_b - 1, -1, color)

        if color_b != color:
            return right

        res = left + [self.ball_generator.balls[ind_b]] + right
        res.sort(key=lambda x: x.pos_in_path)

        return res

    def shoot(self, target):
        if len(self.shooting_balls) == 0 or self.speed or \
                (datetime.datetime.now() - self.shooting_balls[-1].time).microseconds > 300000:
            curr_b = self.cur_ball
            curr_b.set_time(datetime.datetime.now())
            curr_b.set_target(target)
            self.shooting_balls.append(curr_b)
            self.cur_ball = self.reload()
