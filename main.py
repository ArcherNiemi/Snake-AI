import pygame
import random

WIDTH, HEIGHT = 600, 600

SNAKE_COLOR = "white"
SNAKE_SIZE = 30
MOVEMENT_AMOUNT = SNAKE_SIZE

SNAKE_STARTING_LOCATION = 300

APPLE_COLOR = "red"
APPLE_SIZE = SNAKE_SIZE

NUM_OF_APPLES = 1

FPS = 10

pygame.init()

FONT = pygame.font.SysFont("arial", 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 1
        self.body = [pygame.Rect(SNAKE_STARTING_LOCATION, SNAKE_STARTING_LOCATION, SNAKE_SIZE, SNAKE_SIZE)]
        self.movementDirection = "left"
        self.size = SNAKE_SIZE
        self.color = SNAKE_COLOR
        self.speed = MOVEMENT_AMOUNT
    
    def draw(self):
        for i in range(self.length):
            pygame.draw.rect(screen, self.color, self.body[i])
    
    def move(self):
        if(self.movementDirection == "left"):
            self.body.insert(0, pygame.Rect(self.body[0].x - self.speed, self.body[0].y, self.size, self.size))
        if(self.movementDirection == "right"):
            self.body.insert(0, pygame.Rect(self.body[0].x + self.speed, self.body[0].y, self.size, self.size))
        if(self.movementDirection == "up"):
            self.body.insert(0, pygame.Rect(self.body[0].x, self.body[0].y - self.speed, self.size, self.size))
        if(self.movementDirection == "down"):
            self.body.insert(0, pygame.Rect(self.body[0].x, self.body[0].y + self.speed, self.size, self.size))
    
    def changeMovmentDirection(self, newDirection):
        self.movementDirection = newDirection
    
    def collectApple(self):
        self.length += 1
    
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
        self.color = APPLE_COLOR
        self.size = APPLE_SIZE
    
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))


def main():
    snake = Snake()
    apples = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed() # Get the state of all keys
            if keys[pygame.K_LEFT]:
                snake.changeMovmentDirection("left")
            if keys[pygame.K_RIGHT]:
                snake.changeMovmentDirection("right")
            if keys[pygame.K_UP]:
                snake.changeMovmentDirection("up")
            if keys[pygame.K_DOWN]:
                snake.changeMovmentDirection("down")
        
        if(NUM_OF_APPLES > len(apples)):
            apples.append(Apple())
        
        for i in range(len(apples)):
            if(snake.body[0].x == apples[i].x and snake.body[0].y == apples[i].y):
                snake.collectApple()
                apples.remove(apples[i])
        
        snake.move()
        if(snake.deathCheck()):
            running = False

        draw(snake, apples)
        clock.tick(FPS)

def draw(snake, apples):
    pygame.draw.rect(screen, "black", pygame.Rect(0,0,WIDTH,HEIGHT))
    for i in range(len(apples)):
        apples[i].draw()
    snake.draw()
    score_text = FONT.render(f"Score: {snake.length - 1}", True, "white")
    screen.blit(score_text, (5,5))
    pygame.display.flip()

if __name__ == "__main__":
    main()
