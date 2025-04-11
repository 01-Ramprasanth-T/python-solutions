import pygame
import random
from sys import exit

pygame.init()

# Constants
fps = 60
width = 1000
height = 500
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprite Example")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 100)
        self.velocity = 0
        self.speed = 5
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        self.velocity += 1
        if self.velocity > 10:
            self.velocity = 10
        self.rect.y += self.velocity

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

    def jump(self, platforms):
        if not self.is_jumping:
            self.velocity = -15
            self.is_jumping = True
        self.rect.y += self.velocity
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity > 0:
                self.velocity = 0
                self.is_jumping = False

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))  # Corrected attribute name
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player and platforms
player = Player()
all_sprites.add(player)

platform1 = Platform(400, height-10, 200, 10)
platform2 = Platform(600, height - 150, 200, 10)
platforms.add(platform1, platform2)
all_sprites.add(platform1, platform2)

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Update sprites
    all_sprites.update()

    # Draw everything
    screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(fps)
 