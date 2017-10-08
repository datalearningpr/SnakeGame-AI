
import pygame
import random
from models import Apple, NN_Snake
import numpy as np
import pickle
from keras.models import load_model
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
FPS = 20000

# set up for the NN
actions = ["up", "left", "right"]

# training method
def training_game(times = 40000):
    # we need to store the training data first
    # then use the data to train the NN
    train_data = []
    # f = open("train_data.txt", "rb")
    # train_data = pickle.load(f)
    # f.close()

    for i in range(times):
        # print out the game number
        print(i)

        pygame.event.pump()
        game_over = False

        # Will be the leader of the #1 block of the snake
        lead_x = 70
        lead_y = 70

        # snake default direction is right
        snake = NN_Snake(gameDisplay, display_width, display_height, img, lead_x, lead_y)
        apple = Apple(gameDisplay, display_width, display_height, block_size, img2, snake.snake_list)

        a_x, a_y = apple.get_apple_pos()
        
        # get the initial state, and action will be "up" starting
        action = "up"
        state = snake.get_state([a_x, a_y], action)
        old_distance = snake.get_distance([a_x, a_y])

        while not game_over:
                   
            # based on the direction, we can work out the x, y changes to update the snake
            a_x, a_y = apple.get_apple_pos()
            snake.update_snake_list(a_x, a_y)
            
            # after snake moves, get the new distance
            distance = snake.get_distance([a_x, a_y])

            # default reward is 0
            reward = 0
            # check if snake dies
            if snake.is_alive() is False:
                game_over = True
                # if snake dies, award is -1
                reward = -1

            gameDisplay.fill(white)
            
            # if snake eats the apple, make a random new apple
            if snake.eaten is True:
                apple.update_apple_pos(snake.snake_list)
               
            # if snake eats the apple, or moved closer to apple, reward is 1
            if snake.eaten is True or distance < old_distance:
                 reward = 1

            #############################################
            # collect the training data for NN
            train_data.append([np.array(state), reward])


            # this part is using random method to move the snake
            action = random.choice(actions)
            a_x, a_y = apple.get_apple_pos()
            old_distance = snake.get_distance([a_x, a_y])
            state = snake.get_state([a_x, a_y], action)
            snake.set_direction_by_action(action)
            #############################################

            apple.display()
            snake.eaten = False
            snake.display()
            snake.display_score()
            pygame.display.update()
            clock.tick(FPS)
    # store the training data to txt
    print(len(train_data))
    f = open("train_data.txt", "wb")
    pickle.dump(train_data, f)
    f.close()

# using the NN to play the snake game
def testing_game(times = 10):
    # load the trained NN model
    model = load_model('my_model.h5')
    
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
        snake = NN_Snake(gameDisplay, display_width, display_height, img, lead_x, lead_y)
        apple = Apple(gameDisplay, display_width, display_height, block_size, img2, snake.snake_list)

        a_x, a_y = apple.get_apple_pos()
        
        # get the initial state, and action will be "up" starting
        action = "up"
        state = snake.get_state([a_x, a_y], action)
        old_distance = snake.get_distance([a_x, a_y])

        while not game_over:
                
            # based on the direction, we can work out the x, y changes to update the snake
            a_x, a_y = apple.get_apple_pos()
            snake.update_snake_list(a_x, a_y)

            # check if snake dies
            if snake.is_alive() is False:
                game_over = True
                s.append(snake.snake_length)

            gameDisplay.fill(white)
            
            # if snake eats the apple, make a random new apple
            if snake.eaten is True:
                apple.update_apple_pos(snake.snake_list)

            #############################################
            # get the position of the apple
            a_x, a_y = apple.get_apple_pos()

            # use NN model to get the action with max Q
            precictions = {}
            for action in actions:
               state = snake.get_state([a_x, a_y], action)
               precictions[action] = model.predict(np.array(state).reshape(-1, 5))[0][0]
            action = max(precictions, key=precictions.get)
            
            # set the direction of snake using the chosen action
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
    # training_game(5000)
    testing_game()
