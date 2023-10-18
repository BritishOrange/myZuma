from unittest import TestCase

from Path import MapAggregator
from BallSpawner import BallSpawner
from Sprites import *
from ShootingAggregator import ShootingAggregator
from BonusAggregator import BonusAggregator, Bonus
from ScoreAggregator import ScoreAggregator


def shoot_aggregator_set(spawner, color_bullet):
    shoot_agg = ShootingAggregator(spawner, SCREEN_CENTER,
                                   BonusAggregator(spawner),
                                   ScoreAggregator())
    shoot_agg.shooting_balls = [ShootingBall(color_bullet)]
    return shoot_agg


def balls_set(path, colors):
    positions = pos_set(path, len(colors))
    return [Ball(colors[i], positions[i], path) for i in range(len(colors))]


def pos_set(path, length):
    step = 2 * BALL_RADIUS // path.step
    return [i for i in range(0, length * step + 1, step)]


def ball_spawner_set(path, colors):
    spawner = BallSpawner(path, len(colors), ScoreAggregator())
    spawner.balls = balls_set(path, colors)
    return spawner


class TestBonus(TestCase):

    def test_bomb(self):
        spawner = ball_spawner_set(MapAggregator(1), [YELLOW] * 4 + [BLUE] * 2 + [RED] * 4)

        spawner.balls[4].take_bonus(Bonus.Bomb)
        expected = [spawner.balls[0], spawner.balls[-1]]
        shoot_agg = shoot_aggregator_set(spawner, BLUE)
        chain = shoot_agg.make_chain(spawner.balls[4], BLUE)
        chain += shoot_agg.is_bonus_in_chain(chain)
        spawner.del_balls(chain)

        assert expected == spawner.balls


class TestChain(TestCase):
    @staticmethod
    def test_set(level, colors, bullet_col, ind_begin, expected):
        spawner = ball_spawner_set(MapAggregator(level), colors)
        shoot_agg = shoot_aggregator_set(spawner, bullet_col)
        curr_chain = shoot_agg.make_chain(spawner.balls[ind_begin], bullet_col)
        expected_chain = [spawner.balls[i] for i in expected]
        return expected_chain == curr_chain

    def test_is_chain_in_begin_others_colors(self):
        assert self.test_set(1, [BLUE, GREEN, GREEN, GREEN], GREEN, 0,
                             [1, 2, 3]) is True

    def test_is_chain_in_end(self):
        assert self.test_set(1, [GREEN, GREEN, BLUE, BLUE], GREEN, 0,
                             [0, 1]) is True

    def test_got_only_one(self):
        assert self.test_set(1, [BLUE, GREEN, RED, YELLOW], GREEN, 1,
                             [1]) is True

    def test_dont_collect_chain(self):
        assert self.test_set(1, [GREEN] * 4, BLUE, 2, []) is True

    def test_is_chain_in_begin(self):
        assert self.test_set(1, [GREEN, GREEN, BLUE, BLUE], BLUE, 3,
                             [2, 3]) is True

    def test_is_chain_in_center(self):
        assert self.test_set(1, [GREEN, BLUE, BLUE, GREEN], BLUE, 1,
                             [1, 2]) is True


class TestUpdateChain(TestCase):
    path = MapAggregator(1)

    @staticmethod
    def are_stopped(start_index, balls):
        for i in range(0, start_index):
            if not balls[i].can_move:
                return False

        for i in range(start_index, len(balls)):
            if balls[i].can_move:
                return False

        return True

    def are_moved(self, balls):
        for i in range(1, len(balls)):
            if balls[i].pos_in_path - balls[i - 1].pos_in_path != 2 * BALL_RADIUS // self.path.step:
                return False
        return True

    def test_block_movement_for_one(self):
        spawner = self.test_set([RED, BLUE, BLUE, GREEN], [1, 2])
        assert self.are_stopped(1, spawner.balls) is True

    def test_block_movement_more(self):
        colors = [RED, BLUE, BLUE] + [GREEN, YELLOW] * 5
        spawner = self.test_set(colors, [1, 2])
        assert self.are_stopped(1, spawner.balls) is True

    def test_merge_more(self):
        colors = [RED, BLUE, BLUE, RED] + [GREEN, YELLOW] * 5
        spawner = self.test_set(colors, [1, 2])
        assert self.are_moved(spawner.balls) is True

    def test_set(self, colors, destroy_indexes):
        ball_generator = ball_spawner_set(self.path, colors)
        ball_generator.del_balls([ball_generator.balls[i] for i in destroy_indexes])
        ball_generator.chain_upd()
        return ball_generator

    def test_merge_couple(self):
        spawner = self.test_set([RED, BLUE, BLUE, RED], [1, 2])
        assert self.are_moved(spawner.balls) is True


class TestInsert(TestCase):
    @staticmethod
    def test_set(color_bullet, map_number, balls_colors, ins_ind, expected):
        bullet = ShootingBall(color_bullet)
        path = MapAggregator(map_number)
        spawner = ball_spawner_set(path, balls_colors)
        spawner.insertion(ins_ind, bullet)
        expected_balls = balls_set(path, expected)
        return expected_balls == spawner.balls

    def test_end_insert1(self):
        assert self.test_set(RED, 1, [YELLOW, GREEN, BLUE], 0,
                             [YELLOW, RED, GREEN, BLUE]) is True

    def test_end_insert2(self):
        assert self.test_set(RED, 2, [YELLOW, GREEN, BLUE], 0,
                             [YELLOW, RED, GREEN, BLUE]) is True

    def test_end_insert3(self):
        assert self.test_set(RED, 3, [YELLOW, GREEN, BLUE], 0,
                             [YELLOW, RED, GREEN, BLUE]) is True

    def test_center_insert1(self):
        assert self.test_set(RED, 1, [YELLOW, GREEN, BLUE], 1,
                             [YELLOW, GREEN, RED, BLUE]) is True

    def test_center_insert2(self):
        assert self.test_set(RED, 2, [YELLOW, GREEN, BLUE], 1,
                             [YELLOW, GREEN, RED, BLUE]) is True

    def test_center_insert3(self):
        assert self.test_set(RED, 3, [YELLOW, GREEN, BLUE], 1,
                             [YELLOW, GREEN, RED, BLUE]) is True

    def test_begin_insert1(self):
        assert self.test_set(RED, 1, [YELLOW, GREEN, BLUE], 2,
                             [YELLOW, GREEN, BLUE, RED]) is True

    def test_begin_insert2(self):
        assert self.test_set(RED, 2, [YELLOW, GREEN, BLUE], 2,
                             [YELLOW, GREEN, BLUE, RED]) is True

    def test_begin_insert3(self):
        assert self.test_set(RED, 3, [YELLOW, GREEN, BLUE], 2,
                             [YELLOW, GREEN, BLUE, RED]) is True


class TestRemove(TestCase):

    def test_remove(self):
        spawner = ball_spawner_set(MapAggregator(1), [GREEN, BLUE, BLUE, RED])
        expected = [spawner.balls[0], spawner.balls[3]]
        spawner.del_balls([spawner.balls[1], spawner.balls[2]])
        assert expected == spawner.balls
