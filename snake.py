import pygame
import random

width = 400
height = 300
snake_size = 10

black =  (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

x_direction = 0
y_direction = 0

def generate_food(dis):
    food = [random.randint(0, width/snake_size-1),
            random.randint(0, height/snake_size-1)]
    print(food)
    pygame.draw.rect(dis, red, [food[0]*snake_size, food[1]*snake_size, snake_size, snake_size])
    return food

def main():
    global food,x_direction,y_direction
    pygame.init()
    dis = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake')
    snake = [(width/(snake_size*2), height/(snake_size*2))]
    game_over = False
    key_pressed = False
    i = 0
    food = generate_food(dis)
    while not game_over:
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if key_pressed:
                    continue
                if  event.key == pygame.K_LEFT:
                    if x_direction == 0:
                        x_direction = -1
                        y_direction = 0
                        print("direction change: x=", x_direction)
                        print("direction change: y=", y_direction)
                        key_pressed = True
                elif event.key == pygame.K_RIGHT:
                    if x_direction == 0:
                        x_direction = 1
                        y_direction = 0
                        print("direction change: x=", x_direction)
                        print("direction change: y=", y_direction)
                        key_pressed = True
                elif event.key == pygame.K_DOWN:
                    if y_direction == 0:
                        y_direction = 1
                        x_direction = 0
                        print("direction change: x=", x_direction)
                        print("direction change: y=", y_direction)
                        key_pressed = True
                elif event.key == pygame.K_UP:
                    if y_direction == 0:
                        y_direction = -1
                        x_direction = 0
                        print("direction change: x=", x_direction)
                        print("direction change: y=", y_direction)
                        key_pressed = True

        if (i%30000) != 0:
            continue
        key_pressed = False
        snake_head_x, snake_head_y = snake[-1]
        snake_head_x += x_direction
        snake_head_y += y_direction
        if snake_head_x >= width/snake_size or snake_head_x < 0 or snake_head_y >= height/snake_size or snake_head_y < 0:
            print("died! %d,%d" % (snake_head_x,snake_head_y))
            game_over = True
            break

        snake.append((snake_head_x, snake_head_y))


        if (snake_head_x == food[0]) and (snake_head_y == food[1]):
            print("eat!")
            food = generate_food(dis)
        else:
            snake_tail = snake.pop(0)
            pygame.draw.rect(dis, black, [snake_tail[0]*snake_size, snake_tail[1]*snake_size, snake_size, snake_size])
        pygame.draw.rect(dis, blue, [snake_head_x * snake_size, snake_head_y * snake_size, snake_size, snake_size])
        pygame.display.update()

        if (snake_head_x,snake_head_y) in snake[:-1]:
            print("touched body!")
            print(snake)
            print(snake_head_x, snake_head_y)
            game_over = True
            break

    input("?")
    pygame.quit()
    quit()

main()