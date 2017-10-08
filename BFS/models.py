import random

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
