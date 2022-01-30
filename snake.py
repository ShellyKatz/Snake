import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

BLOCK_SIZE = 10
SPEED = 11
BLACK =  (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLUE2 = (0, 100, 255)
RED = (255, 0, 0)

#font = pygame.font.Font('name of file i need to place in dir')
font = pygame.font.SysFont('Segoe UI', 20, bold=True)

class Direction(Enum): #helps to reduce errors (for example typing errors)
    R = 1 # right
    L = 2 # left
    U = 3 # up
    D = 4 # down

Point = namedtuple('Point', 'x, y') #configuring point type also helps to reduce errors

class SnakeGame:
    def __init__(self, w=360, h=360):
        # init display
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock();
        pygame.display.set_caption('Snake')
        #self.background = pygame.image.load('images/nokia.png')

        # init game state
        self.direction = Direction.R
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]

        self.score = 0
        self.food = None

        self.place_food()

    def place_food(self):
        x = random.randint(0, self.w // BLOCK_SIZE - 1) * BLOCK_SIZE
        y =  random.randint(0, self.h // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.food = Point(x, y)
        print(self.food.x, self.food.y)
        if self.food in self.snake: #check food point isn't on snake
            self.place_food()

    def update_ui(self):
        self.display.fill(BLACK) #fill screen in black
        #self.display.blit(self.background, (0, 0))
        for p in self.snake: #todo- change later, don't use a loop
            pygame.draw.rect(self.display, BLUE, [p.x, p.y, BLOCK_SIZE, BLOCK_SIZE])
            # smaller rect with lighter color inside the bigger rect to create nicer look
            pygame.draw.rect(self.display, BLUE2, [p.x+2, p.y+2, 6, 6])

        pygame.draw.rect(self.display, RED, [self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE])

        #score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0]) #0,0 = upper left corner

        #display all
        pygame.display.update() #with no arguments - similar to flip

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.R:
            x += BLOCK_SIZE
        elif direction == Direction.L:
            x -= BLOCK_SIZE
        elif direction == Direction.D: #remember 0,0 is upper left!
            y += BLOCK_SIZE
        elif direction == Direction.U:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def is_collision(self):
        # check if hits boundaries
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or \
           self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True

        # check if hits body
        if self.head in self.snake[1:]: #todo change to check this before adding new head list
            return True

        return False


    def play_step(self):
        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.L;
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.R
                elif event.key == pygame.K_UP:
                    self.direction = Direction.U
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.D

        # move snake
        self.move(self.direction)
        self.snake.insert(0, self.head) #?? todo - maybe move inside function?

        # check if game over
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score

        # check if ate food if not just move snake
        if self.head == self.food:
            print("hit food!")
            self.score += 1
            self.place_food()
        else:
            self.snake.pop() #move by removing tail point

        # update UI and clock
        self.update_ui()
        self.clock.tick(SPEED) #??

        return game_over, self.score


def main():
    game = SnakeGame()

    game_over = False
    while not game_over:
        game_over, score = game.play_step()

    print("Final Score:", score)
    pygame.quit() #close all modules

main()