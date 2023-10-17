class ScoreAggregator:
    def __init__(self):
        self.lose_game = False
        self.lives = 2
        self.is_lose = False
        self.score = 0
        self.is_win = False

    def default_for_next_level(self):
        self.is_win = False
        self.is_lose = False

    def lose(self):
        self.is_lose = True

    def win(self):
        self.is_win = True

    def is_game_over(self):
        if self.lives == 0:
            self.lose_game = True

    def decrease_lives(self):
        self.lives -= 1
        self.is_game_over()

    def increase_lives(self, buffer_score):
        for sc in range(self.score + 1, self.score + buffer_score + 1):
            if sc % 500 != 0:
                continue
            else:
                self.lives += 1

    def increase_score(self, buffer_score):
        self.increase_lives(buffer_score)
        self.score += buffer_score
