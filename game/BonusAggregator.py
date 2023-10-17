import datetime
import random
from enum import Enum


class Bonus(Enum):
    Pause = 0
    Reverse = 1
    Bomb = 2
    Speed = 3


class BonusAggregator:
    def __init__(self, b_gen):
        self.ball_generator = b_gen
        self.balls_with_bonuses = []
        self.speed_start_time = None
        self.bonuses = [Bonus.Pause, Bonus.Reverse, Bonus.Bomb, Bonus.Speed]
        self.reverse_start_time = None
        self.game_start_time = datetime.datetime.now()
        self.pause_start_time = None

    def aggregate_bomb(self, chain):
        end = self.ball_generator.balls.index(chain[0]) - 1
        begin = self.ball_generator.balls.index(chain[-1]) + 1

        res = []

        for _ in range(3):
            if end >= 0:
                res.append(self.ball_generator.balls[end])
                end -= 1
            else:
                break

        for _ in range(3):
            if len(self.ball_generator.balls) - 1 >= begin:
                res.append(self.ball_generator.balls[begin])
                begin += 1
            else:
                break

        return res

    def aggregate_speed(self):
        if self.speed_start_time is None or (datetime.datetime.now() -
                                             self.speed_start_time).seconds == 5:
            self.deact_speed_bonus()
            return False
        return True

    def aggregate_pause(self):
        if self.pause_start_time is not None:
            if (datetime.datetime.now() - self.pause_start_time).seconds != 5:
                return
            self.deact_pause_bonus()

    def reverse_move(self):
        for i in range(len(self.ball_generator.balls)):
            self.ball_generator.balls[i].move(-1)

    def aggregate_reverse(self):
        if self.reverse_start_time is not None:
            if 4 <= (datetime.datetime.now() - self.reverse_start_time).seconds:
                self.deact_reverse_bonus()
            else:
                self.reverse_move()

    def deact_speed_bonus(self):
        self.speed_start_time = None

    def deact_pause_bonus(self):
        self.pause_start_time = None
        self.ball_generator.pause = False

    def deact_reverse_bonus(self):
        self.ball_generator.reverse = False
        self.reverse_start_time = None

    def activate_pause_bonus(self):
        self.ball_generator.pause = True
        self.pause_start_time = datetime.datetime.now()

    def activate_reverse_bonus(self):
        self.ball_generator.reverse = True
        self.reverse_start_time = datetime.datetime.now()

    def activate_speed_bonus(self):
        self.speed_start_time = datetime.datetime.now()

    def run_bonus(self, bonus):
        if bonus is Bonus.Speed:
            self.activate_speed_bonus()
        elif bonus is Bonus.Pause:
            self.activate_pause_bonus()
        elif bonus is Bonus.Reverse:
            self.activate_reverse_bonus()

    def bonus_generation(self):
        curr_t = datetime.datetime.now()
        if (curr_t - self.game_start_time).seconds == 15:
            bonus_ball = random.choice(self.ball_generator.balls)
            bonus = random.choice(self.bonuses)
            bonus_ball.take_bonus(bonus)
            self.balls_with_bonuses.append((bonus_ball, curr_t))
            self.game_start_time = curr_t

    def bonus_ball_upd(self):
        for b, t in self.balls_with_bonuses:
            if (datetime.datetime.now() - t).seconds == 15:
                b.take_bonus(None)

    def update(self):
        self.aggregate_pause()
        self.bonus_ball_upd()
        self.bonus_generation()
        self.aggregate_reverse()
