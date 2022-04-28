import random
import sys
import pygame

HEIGHT = 700
WIDTH = 700
BLACK = (0, 0, 0)
PINK = (255, 0, 122)
PURPLE = (100, 0, 255)
YELLOW = (255, 236, 0)
GREEN = (43, 159, 3)
GRID_SIZE = 20

class Snake:

    def __init__(self):

        self.velocity = 20
        self.length = 1
        self.snake_body = [[220, 220]]
        self.actual_movements = random.choice(["right", "left", "down", "up"])
        self.incorrect_movements = {"right": ["left"], "left": ["right"], "up": ["down"], "down": ["up"]}
        self.best_score = 1
        self.temp_score = 1

    def move_snake(self, window):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue

                    self.actual_movements = "left"
                
                if event.key == pygame.K_RIGHT:

                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue

                    self.actual_movements = "right"

                if event.key == pygame.K_UP:

                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue

                    self.actual_movements = "up"

                if event.key == pygame.K_DOWN:
                    
                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue

                    self.actual_movements = "down"
                
        self.snake_movements(window)

    def snake_movements(self, window):

        if self.actual_movements == "right":
            temp = self.snake_body[0][0] + self.velocity
            x = self.check_bounds(temp, "max_limit")
            self.update_snake(x, "X", window)
        
        if self.actual_movements == "left":
            temp = self.snake_body[0][0] - self.velocity
            x = self.check_bounds(temp, "min_limit")
            self.update_snake(x, "X", window)

        if self.actual_movements == "up":
            temp = self.snake_body[0][1] - self.velocity
            y = self.check_bounds(temp, "min_limit")
            self.update_snake(y, "Y", window)

        if self.actual_movements == "down":
            temp = self.snake_body[0][1] + self.velocity
            y = self.check_bounds(temp, "max_limit")
            self.update_snake(y, "Y", window)

    def update_snake(self, value, key, window):
        
        if key == "X":
            self.snake_body.insert(0, [value, self.snake_body[0][1]])
            self.snake_body.pop()
            self.draw_snake(window)
        else:
            self.snake_body.insert(0, [self.snake_body[0][0], value])
            self.snake_body.pop()
            self.draw_snake(window)

    def draw_snake(self, window):

        for idx, body in enumerate(self.snake_body):

            if idx == 0:
                pygame.draw.rect(window, YELLOW, [body[0], body[1], 20, 20])
                continue

            pygame.draw.rect(window, PURPLE, [body[0], body[1], 20, 20])
    
    def check_valid_movement(self, next_mov):

        if next_mov in self.incorrect_movements[self.actual_movements]:
            return True
    
    def check_bounds(self, value_to_check_, limit):
        
        if limit == "max_limit":
            if value_to_check_ > 680:
                return 0
            else:
                return value_to_check_
        
        else:
            if value_to_check_ < 0:
                return 680
            else:
                return value_to_check_

    def get_snake_head(self):
        return self.snake_body[0]
    
    def grow_snake(self, value, window):
        self.snake_body.insert(0, list(value))
        self.draw_snake(window)

class Food:

    def __init__(self):
        self.food_position = (0, 0)
        self.random_position()

    def random_position(self):
        self.food_position = (random.randrange(0, 680, 20), random.randrange(0, 680, 20))

    def draw_food(self, window):
        pygame.draw.rect(window, PINK, [self.food_position[0], self.food_position[1], 20, 20])


def check_food(snake, food, window):
    if tuple(snake.get_snake_head()) == food.food_position:

        snake.grow_snake(food.food_position, window)

        food.random_position()
        food.draw_food(window)

        snake.length += 1

def draw_grid(window):
    window.fill(GREEN)
    x = 0
    y = 0

    for i in range(WIDTH):
        x += GRID_SIZE
        y += GRID_SIZE

        pygame.draw.line(window, BLACK, (x, 0), (x, WIDTH))
        pygame.draw.line(window, BLACK, (0, y), (HEIGHT, y))

def main():

    pygame.init()
    window = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    game_font = pygame.font.SysFont("Helvetica", 28)

    while True:
        
        clock.tick(12)

        draw_grid(window)
        snake.move_snake(window)

        check_food(snake, food, window)

        score = game_font.render(f"Score {snake.length}", True, BLACK)
        window.blit(score, (5, 0))
        best_score = game_font.render("Best score", True, BLACK)
        window.blit(best_score, (5, 30))

        food.draw_food(window)
        pygame.display.update()

main()