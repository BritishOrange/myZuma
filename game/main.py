from Path import MapAggregator
from Sprites import *
from BallSpawner import BallSpawner
from ShootingAggregator import ShootingAggregator
from BonusAggregator import BonusAggregator
from ScoreAggregator import ScoreAggregator
from UIManager import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level_num = 1
        self.score_aggregator = ScoreAggregator()
        self.new_game_settings()
        self.is_quit = False

    def continue_game(self, button, window):
        continued = False
        while not continued and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.rect.collidepoint(mouse):
                        continued = True
            self.update_display(window)

    def update_display(self, display):
        self.ui_manager.draw_window(display)
        if display is self.ui_manager.game_display:
            self.ui_manager.print_score(self.score_aggregator.score)
            self.ui_manager.print_lives(self.score_aggregator.lives)
        pygame.display.update()

    def new_game_settings(self):
        self.level = Level(self.level_num, self.score_aggregator)
        self.ui_manager = UIAggregator(self.screen, self.level)

    def run_game(self):
        finished = False

        while not finished and not self.is_quit:
            self.level.ball_generator.gen_balls()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.level.shooting_manager.shoot(pygame.mouse.get_pos())
            self.update_sprites()
            self.update_display(self.ui_manager.game_display)

            if self.score_aggregator.is_win:
                finished = True
                self.aggregate_win()
            elif self.score_aggregator.is_lose:
                finished = True
                self.aggregate_lose()

    def aggregate_win(self):
        if self.level_num != 3:
            self.continue_game(self.ui_manager.continue_btn,
                               self.ui_manager.win_level_display)
            self.level_num += 1
            self.score_aggregator.default_for_next_level()
        else:
            self.aggregate_end_game()

    def update_sprites(self):
        self.level.player.update()
        self.level.shooting_manager.update()
        self.level.ball_generator.update()
        self.level.bonus_manager.update()
        self.level.finish.update()

    def aggregate_lose(self):
        self.score_aggregator.decrease_lives()
        if not self.score_aggregator.lose_game:
            self.continue_game(self.ui_manager.start_level_again_btn,
                               self.ui_manager.lose_level_display)
            self.score_aggregator.default_for_next_level()
        else:
            self.continue_game(self.ui_manager.new_game_button,
                               self.ui_manager.lose_game_display)
            self.level_num = 1
            self.score_aggregator = ScoreAggregator()

    def play(self):
        self.continue_game(self.ui_manager.start_game_btn, self.ui_manager.start_game_display)
        while not self.is_quit:
            self.new_game_settings()
            self.run_game()

        pygame.quit()

    def aggregate_end_game(self):
        on_win_window = True
        while on_win_window and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui_manager.start_game_again_btn.rect.collidepoint(mouse):
                        on_win_window = False
                        self.level_num = 1
                    elif self.ui_manager.finish_btn.rect.collidepoint(mouse):
                        self.is_quit = True

            self.update_display(self.ui_manager.win_game_display)


class Level:
    def __init__(self, number, score_manager):
        self.number = number
        self.player = Player(number)
        self.path = MapAggregator(number)
        self.ball_generator = BallSpawner(self.path, number * 50, score_manager)
        self.finish = Finish(self.path, self.ball_generator.balls, score_manager)
        self.bonus_manager = BonusAggregator(self.ball_generator)
        self.shooting_manager = ShootingAggregator(self.ball_generator, self.player.pos, self.bonus_manager, score_manager)


if __name__ == '__main__':
    game = Game()
    game.play()
