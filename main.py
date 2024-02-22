import pygame
import time
import random
from pygame.locals import *


SIZE = 40  # all images are 40 x 40px


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apples.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * 40  # screen size is 1000
        self.y = random.randint(1, 19) * 40


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/snake.png").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((153, 217, 234))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()  # updating the window

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE

        self.draw()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"


class Game:
    def __init__(self):
        pygame.init()

        # initialize game window
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((103, 179, 206))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # checking if head of snake touched the apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # starting from 3, because snake's head will never collide with second or third block of the body
        for i in range(1, self.snake.length):
            if self.collision(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                raise "Game Over"

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score:{self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def collision(self, x1, y1, x2, y2):
        # comparing the coordinates
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def show_game_over(self):
        self.surface.fill((103, 179, 206))
        font = pygame.font.SysFont("arial", 30)
        line = font.render(f"Score:{self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line, (300, 400))
        line1 = font.render(
            "To play again press Enter. To exit press Escape", True, (255, 255, 255)
        )
        self.surface.blit(line1, (300, 450))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
