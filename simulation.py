import pygame
import random

WIDTH, HEIGHT = 600, 600

SNAKE_SIZE = 60
MOVEMENT_AMOUNT = SNAKE_SIZE

SNAKE_STARTING_LOCATION = 300

APPLE_SIZE = SNAKE_SIZE

NUM_OF_APPLES = 1

class Snake:
    def __init__(self):
        self.length = 1
        self.body = [pygame.Rect(SNAKE_STARTING_LOCATION, SNAKE_STARTING_LOCATION, SNAKE_SIZE, SNAKE_SIZE)]
        self.movementDirection = "left"
        self.size = SNAKE_SIZE
        self.speed = MOVEMENT_AMOUNT
        self.amountOfMoves = 0
    
    def move(self):
        if(self.movementDirection == "left"):
            self.body.insert(0, pygame.Rect(self.body[0].x - self.speed, self.body[0].y, self.size, self.size))
        if(self.movementDirection == "right"):
            self.body.insert(0, pygame.Rect(self.body[0].x + self.speed, self.body[0].y, self.size, self.size))
        if(self.movementDirection == "up"):
            self.body.insert(0, pygame.Rect(self.body[0].x, self.body[0].y - self.speed, self.size, self.size))
        if(self.movementDirection == "down"):
            self.body.insert(0, pygame.Rect(self.body[0].x, self.body[0].y + self.speed, self.size, self.size))
        self.amountOfMoves += 1
    
    def changeMovmentDirection(self, newDirection):
        self.movementDirection = newDirection
    
    def collectApple(self):
        self.length += 1
        self.amountOfMoves = 0
    
    def deathCheck(self):
        for i in range(self.length - 1):
            if(self.body[0] == self.body[i + 1]):
                return True
        if(self.body[0].x < 0 or self.body[0].y < 0 or self.body[0].x >= WIDTH or self.body[0].y >= HEIGHT):
            return True
        return False

class Apple:
    def __init__(self):
        self.x = random.randint(0, int(WIDTH / SNAKE_SIZE) - 1) * SNAKE_SIZE
        self.y = random.randint(0, int(WIDTH / SNAKE_SIZE) - 1) * SNAKE_SIZE
        self.size = APPLE_SIZE

def main(NN):
    snake = Snake()
    apples = [Apple()]
    closestDistance = 10000

    running = True
    while running:
        if(NUM_OF_APPLES > len(apples)):
            apples.append(Apple())
        output = NN.run((snake.body[0].x, snake.body[0].y, apples[0].x, apples[0].y))
        snake.changeMovmentDirection(output)

        distance = (abs(snake.body[0].x - apples[0].x) ** 2 + abs(snake.body[0].y - apples[0].y) ** 2) ** 0.5
        if(distance <= closestDistance):
            closestDistance = distance
        
        for i in range(len(apples)):
            if(snake.body[0].x == apples[i].x and snake.body[0].y == apples[i].y):
                snake.collectApple()
                apples.remove(apples[i])
                closestDistance = 10000
        
        snake.move()

        if(snake.deathCheck()):
            running = False
        if(snake.amountOfMoves >= 30):
            running = False

    if(closestDistance != 0):
        return snake.length - 1 + 1/(closestDistance/SNAKE_SIZE + 1)
    else:
        return snake.length - 1