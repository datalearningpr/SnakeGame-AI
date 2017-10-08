
import pygame
import random
from models import Apple, DQN_Snake
import numpy as np
import pickle
from keras.models import load_model
from DQN import DQN

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
FPS = 2000


# set up for the DQN
actions = ["up", "left", "right"]
look_up = {"up": 0, "left": 1, "right": 2}
# state size is 5, action size is 3
agent = DQN(5, 3)
# if you have already trained some model before and saved
# you can uncomment the below code to get the saved model

# agent.load_model()

# traning batch_size
batch_size = 32

# training method
def training_game(times = 100):
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
        snake = DQN_Snake(gameDisplay, display_width, display_height, img, lead_x, lead_y)
        apple = Apple(gameDisplay, display_width, display_height, block_size, img2, snake.snake_list)

        a_x, a_y = apple.get_apple_pos()
        
        # get the initial state, and action will be "up" starting
        action = "up"
        old_state = snake.get_state([a_x, a_y])
        
        while not game_over:
            
            # based on the direction, we can work out the x, y changes to update the snake
            a_x, a_y = apple.get_apple_pos()
            snake.update_snake_list(a_x, a_y)

            # get the new state
            state = snake.get_state([a_x, a_y])
        
            # snake not die or eats the apple, reward will be -10
            # this is negative so that it will "encourage" the snake to 
            # move towards to the apple, since that is the only positive award
            reward = -10
            
            # check if snake dies
            if snake.is_alive() is False:
                game_over = True
                # copy the weights from q_model to target_model
                agent.copy_weights()
                # if snake dies, award is -100
                reward = -100
                s.append(snake.snake_length-1)

            gameDisplay.fill(white)
            
            # if snake eats the apple, make a random new apple
            if snake.eaten is True:
                apple.update_apple_pos(snake.snake_list)
                # if snake eats the apple, reward is 100
                reward = 100
            
            #############################################

            # store the train_data to the memory
            agent.store_train_data(np.reshape(old_state, [1, 5]), look_up[action], reward, np.reshape(state, [1, 5]), game_over)
            
            # if the memory size is larger than the batch_size, start training
            if len(agent.memory) > batch_size:
                agent.train(batch_size)
                       
            # push state to old state
            a_x, a_y = apple.get_apple_pos()
            old_state = snake.get_state([a_x, a_y])
        
            # get the action from the DQN model
            action = actions[agent.get_action(np.reshape(old_state, [1, 5]))]
            snake.set_direction_by_action(action)
            #############################################

            apple.display()
            snake.eaten = False
            snake.display()
            snake.display_score()
            pygame.display.update()
            clock.tick(FPS)
    # when the training is finised, sae the model
    agent.save_model()
    # after traning is done, print out the average score
    print("Average score is: {}".format(sum(s)/len(s)))

if __name__ == "__main__":
    training_game(50)