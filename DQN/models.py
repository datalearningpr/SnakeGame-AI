import random
import numpy as np
import math

# this is the apple object of the snake game
class Apple:
    
    def __init__(self, gameDisplay, display_width, display_height, block_size, img, snake_list, apple_thickness = 10):
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height
        self.block_size = block_size
        self.apple = img
        self.apple_thickness = apple_thickness
        
        self.rand_apple_x = random.randint(0, self.display_width/self.block_size - 1) * 10 
        self.rand_apple_y = random.randint(0, self.display_height/self.block_size - 1) * 10 

        while [self.rand_apple_x, self.rand_apple_y] in snake_list:
            self.rand_apple_x = random.randint(0, self.display_width/self.block_size - 1) * 10 
            self.rand_apple_y = random.randint(0, self.display_height/self.block_size - 1) * 10

    # method to get the new apple
    def update_apple_pos(self, snake_list):
        self.rand_apple_x = random.randint(0, self.display_width/self.block_size - 1) * 10 
        self.rand_apple_y = random.randint(0, self.display_height/self.block_size - 1) * 10 

        while [self.rand_apple_x, self.rand_apple_y] in snake_list:
            self.rand_apple_x = random.randint(0, self.display_width/self.block_size - 1) * 10 
            self.rand_apple_y = random.randint(0, self.display_height/self.block_size - 1) * 10

    # get the apple 
    def get_apple_pos(self):
        return self.rand_apple_x, self.rand_apple_y

    # display the apple to the pygame board
    def display(self):        
        self.gameDisplay.blit(self.apple, [self.rand_apple_x, self.rand_apple_y, self.apple_thickness,
                                 self.apple_thickness])


# this is the snake object of the snake game
class Snake:
    def __init__(self, gameDisplay, display_width, display_height, img, x, y, block_size =10):
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height
        self.head = img
        self.snake_length = 1
        self.snake_list = [[x, y]]
        self.block_size = block_size
        self.eaten = False
        self.direction = "right"

    # check if the snake is still alive
    def is_alive(self):
        if self.snake_list[-1][0] >= self.display_width or self.snake_list[-1][0] < 0 or self.snake_list[-1][1] >= self.display_height\
                or self.snake_list[-1][1] < 0:
            return False
        elif self.snake_list[-1] in self.snake_list[:-1]:
            return False
        else:
            return True

    # check if snake eats the apple
    def eat_apple(self, rand_apple_x, rand_apple_y):
        if self.snake_list[-1][0] == rand_apple_x and self.snake_list[-1][1] == rand_apple_y:
            return True
        else: 
            return False
    
    # display the score to the pygame board 
    def display_score(self):
        from app import black, pygame
        score = self.snake_length - 1
        text = pygame.font.SysFont("Comic Sans MS", 15).render("Score: " + str(score), True, black)
        self.gameDisplay.blit(text, [0, 0])

    # return the snake head position
    def get_snake_head(self):
        return self.snake_list[-1][0], self.snake_list[-1][1]

    # move the snake by one step based on the snake's direction
    def update_snake_list(self, rand_apple_x, rand_apple_y):
        if self.direction == "left":
            lead_x_change = -self.block_size
            lead_y_change = 0
        elif self.direction == "right":
            lead_x_change = self.block_size
            lead_y_change = 0
        elif self.direction == "up":
            lead_y_change = -self.block_size
            lead_x_change = 0
        elif self.direction == "down":
            lead_y_change = self.block_size
            lead_x_change = 0

        snake_head = []
        snake_head.append(self.snake_list[-1][0] + lead_x_change)
        snake_head.append(self.snake_list[-1][1] + lead_y_change)
        self.snake_list.append(snake_head)

        if self.eat_apple(rand_apple_x, rand_apple_y):
            self.snake_length += 1
            self.eaten = True

        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

    # display the snake to the board
    def display(self):
        from app import pygame, green
        self.gameDisplay.blit(self.head, (self.snake_list[-1][0], self.snake_list[-1][1]))

        for XnY in self.snake_list[:-1]:
            pygame.draw.rect(self.gameDisplay, green,
                            [XnY[0], XnY[1], self.block_size, self.block_size])

# extend the snake to facilitate the DQN
class DQN_Snake(Snake):
    # this one will return the state of the snake
    # the state is: with the direction snake is in
    # (what is in the left cell, what is in the above cell, what is in the right cell
    # , (diff of the position between target and the snake head))
    def get_state(self, target):            
        
        head_x, head_y = self.get_snake_head()
        start = [head_x, head_y]

        if self.direction == "up":
            options = [[start[0] - self.block_size, start[1]], [start[0], start[1] - self.block_size], [start[0] + self.block_size, start[1]]]
        elif self.direction == "right":
            options = [[start[0], start[1] - self.block_size], [start[0] + self.block_size, start[1]], [start[0], start[1] + self.block_size]]
        elif self.direction == "down":
            options = [[start[0] + self.block_size, start[1]], [start[0], start[1] + self.block_size], [start[0] - self.block_size, start[1]]]
        elif self.direction == "left":
            options = [[start[0], start[1] + self.block_size], [start[0] - self.block_size, start[1]], [start[0], start[1] - self.block_size]]

        state = []

        for o in options:
            result = None
            if [o[0], o[1]] in self.snake_list or o[0] < 0 or o[0] >= self.display_width or o[1] < 0 or o[1] >= self.display_height:
                result = 1
            else:
                result = 0
            state.append(result)

        quadrant = [target[0] - start[0], target[1] - start[1]]

        # until now, we will get what is in the left, up, right side of the snake head
        # 1 is something will get the snake die
        # 2 is the apple
        # 0 is empty space

        # quadrant is the difference of the position between target and snake head
        
        if self.direction == "up":
            pointer = [0, -1]
        elif self.direction == "right":
            pointer = [1, 0]
        elif self.direction == "down":
            pointer = [0, 1]
        elif self.direction == "left":
            pointer = [-1, 0]
        
        x = np.array(pointer)
        y = np.array(quadrant)

        if quadrant==[0,0]:
            angle = 0
        else:
            angle = np.arccos(x.dot(y) / (np.sqrt(x.dot(x)) * np.sqrt(y.dot(y))))
            if np.cross(x, y) > 0:
                angle = 2 * math.pi - angle 

        # angle is the rotate angle btween the quadrant and direction
        state.append(angle)
        state.append(self.get_distance(target))
        return state

    # method to get the distance between snake head and target
    def get_distance(self, target):
        head_x, head_y = self.get_snake_head()
        start = [head_x, head_y]
        quadrant = [target[0] - start[0], target[1] - start[1]]
        return math.hypot(quadrant[0], quadrant[1])

    # method change the direction based on the action chosen
    def set_direction_by_action(self, action):
        look_up = {"up": 0, "right": 1, "left": -1}
        value = look_up[action]

        if self.direction == "up":
            if value != 0:
                self.direction = ("left" if value == -1 else "right")
            else:
                self.direction = "up"
        elif self.direction == "right":
            if value != 0:
                self.direction = ("up" if value == -1 else "down")
            else:
                self.direction = "right"
        elif self.direction == "down":
            if value != 0:
                self.direction = ("right" if value == -1 else "left")
            else:
                self.direction = "down"
        elif self.direction == "left":
            if value != 0:
                self.direction = ("down" if value == -1 else "up")
            else:
                self.direction = "left"
