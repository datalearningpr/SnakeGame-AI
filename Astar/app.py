
import pygame
import random
from astar import A_star
from models import Apple, Snake

pygame.init()

# colors
white = (0, 0, 0)
black = (255, 255, 255)
red = (255, 0, 0)
green = (0, 155, 0)

# window size
display_width = 150
display_height = 150

# all the pygame settings
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon)
img = pygame.image.load('snakehead.png')
img2 = pygame.image.load('apple.png')
pygame.display.flip()



block_size = 10
# frame per second will control the game speed
FPS = 20

def one_game():
    pygame.event.pump()
    game_over = False

    # snake will start in the middle of the game window
    lead_x = 70
    lead_y = 70

    # snake default direction is right
    snake = Snake(gameDisplay, display_width, display_height, img, lead_x, lead_y)
    apple = Apple(gameDisplay, display_width, display_height, block_size, img2, snake.snake_list) 

    while not game_over:
                 

        # based on the direction, we can work out the x, y changes to update the snake
        x, y = apple.get_apple_pos()
        snake.update_snake_list(x, y)

        # check if snake dies
        if snake.is_alive() is False:
            game_over = True

        gameDisplay.fill(white)
        
        # if snake eats the apple, make a random new apple
        if snake.eaten is True:
            apple.update_apple_pos(snake.snake_list)

        apple.display()
        snake.eaten = False
        snake.display()
        snake.display_score()
        pygame.display.update()
        
        # this part is using the snake position and apple
        # position to use the A* method to get the path
        a_x, a_y = apple.get_apple_pos()
        s_x, s_y = snake.get_snake_head()
        visited = snake.snake_list.copy()
        visited.remove([s_x, s_y])
        result = A_star(display_width, display_height, block_size, visited, (a_x, a_y), (s_x, s_y))

        # since the path starts from snake position, the second element will
        # be next move
        next_cell = result[1]
        
        # update the snake position based on the next move position
        x_diff = next_cell[0] - s_x
        y_diff = next_cell[1] - s_y
        if x_diff > 0:
            snake.direction = "right"
        elif x_diff < 0:
            snake.direction = "left"
        elif y_diff > 0:
            snake.direction = "down"
        elif y_diff < 0:
            snake.direction = "up"

        clock.tick(FPS)

if __name__ == "__main__":
    one_game()
