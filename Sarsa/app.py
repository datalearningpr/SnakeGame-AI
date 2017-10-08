
import pygame
import random
from ReinforcementLearning import Sarsa
from models import Apple, RL_Snake

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

# set up for the Qlearning
actions = ["up", "left", "right"]
snake_agent = Sarsa(actions, e = 0.01)

# if it is the first time to train, there is no Q.txt to load
# then comment out this line
snake_agent.loadQ()


# training method
def training_game(times = 10):
    # s list will store the score of each game
    s = []
    for i in range(times):
        # print out the game number
        print(i)

        pygame.event.pump()
        game_over = False

        # Will be the leader of the #1 block of the snake
        lead_x = 70
        lead_y = 70

        # snake default direction is right
        snake = RL_Snake(gameDisplay, display_width, display_height, img, lead_x, lead_y)
        apple = Apple(gameDisplay, display_width, display_height, block_size, img2, snake.snake_list)

        a_x, a_y = apple.get_apple_pos()

        # get the initial state, and action will be "up" starting
        old_state = snake.get_state([a_x, a_y])
        old_action = "up"

        while not game_over:
                   
            # based on the direction, we can work out the x, y changes to update the snake
            a_x, a_y = apple.get_apple_pos()
            snake.update_snake_list(a_x, a_y)

            # snake not die or eats the apple, reward will be -10
            # this is negative so that it will "encourage" the snake to 
            # move towards to the apple, since that is the only positive award
            reward = -10
            
            # check if snake dies
            if snake.is_alive() is False:
                game_over = True
                # if snake dies, award is -100
                reward = -100
                s.append(snake.snake_length-1)

            gameDisplay.fill(white)
            
            # if snake eats the apple, make a random new apple
            if snake.eaten is True:
                apple.update_apple_pos(snake.snake_list)
                # if snake eats the apple, reward is 500
                reward = 500
            
            #############################################
            # get he new state and new action, then we can update the Q table
            state = snake.get_state([a_x, a_y])
            action = snake_agent.getA(tuple(state))

            snake_agent.updateQ(tuple(old_state), old_action, tuple(state), action, reward)
            old_action = action

            # training will take a lot of time, so archive the Q table
            snake_agent.saveQ()

            # this part is using the snake position and apple
            # position to use the Sarsa method to get the action
            a_x, a_y = apple.get_apple_pos()
            old_state = snake.get_state([a_x, a_y])
            snake.set_direction_by_action(action)
            #############################################

            apple.display()
            snake.eaten = False
            snake.display()
            snake.display_score()
            pygame.display.update()
            clock.tick(FPS)    
    # after traning is done, print out the average score
    print("Average score is: {}".format(sum(s)/len(s)))

if __name__ == "__main__":
    training_game()
