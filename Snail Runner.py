import pygame
from sys import exit
from random import randint

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snail Runner")

# Load resources
sky_surface = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Sky.png").convert()
ground_surface = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\ground.png").convert()
font = pygame.font.Font(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\font\Pixeltype.ttf", 70)
font_h = pygame.font.Font(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\font\Pixeltype.ttf", 30)
bgm = pygame.mixer.Sound(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\audio\music.wav")
bgm.set_volume(0.4)
bgm.play(loops=-1)

# Text elements
end_text = font.render("Game Over", False, "white")
end_rect = end_text.get_rect(center=(400, 140))
restart_text = font.render("Restart", False, "white")
restart_rect = restart_text.get_rect(center=(400, 230))
game_name_text = font.render("SNAIL RUNNER", False, "#FFCC99")
game_name_rect = game_name_text.get_rect(center=(400, 370))
start_text = font.render("Press SPACE to Start", False, "#CCFFFF")
start_rect = start_text.get_rect(center=(400, 250))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stand_image = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Player\player_stand.png").convert_alpha()
        self.jump_image = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Player\jump.png").convert_alpha()
        walk_1 = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Player\player_walk_1.png").convert_alpha()
        walk_2 = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Player\player_walk_2.png").convert_alpha()
        self.walk_images = [walk_1, walk_2]
        self.walk_index = 0

        self.image = self.stand_image
        self.rect = self.image.get_rect(midbottom=(150, 100))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\audio\jump.mp3")
        self.jump_sound.set_volume(0.2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom == 300:
            if keys[pygame.K_UP]:
                self.jump_sound.play()
                self.gravity = -12
            if keys[pygame.K_LEFT]:
                self.rect.x -=4
            elif keys[pygame.K_RIGHT]:
                self.rect.x +=4
        else:
            if keys[pygame.K_LEFT]:
                self.rect.x -=2
            elif keys[pygame.K_RIGHT]:
                self.rect.x +=2
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= 800:
            self.rect.right = 800

    def apply_gravity(self):
        self.gravity += 0.6
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            if self.gravity < 0:
                self.image = self.jump_image
            else:
                self.image = self.stand_image
        else:
            self.walk_index += 0.1
            if self.walk_index >= len(self.walk_images):
                self.walk_index = 0
            self.image = self.walk_images[int(self.walk_index)]
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.image = self.stand_image

    def update(self, end=False):
        if not end:
            self.handle_input()
            self.apply_gravity()
            self.animate()
        else:
            self.image = pygame.transform.rotate(self.stand_image, 90)
            self.rect.center = (140, 290)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, enemy_group):
        super().__init__()
        self.type = enemy_type
        if self.type == "fly":
            fly_1 = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Fly\Fly1.png").convert_alpha()
            fly_2 = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Fly\Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\snail\snail1.png").convert_alpha()
            snail_2 = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\snail\snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(self.find_x(enemy_group), y_pos))

    def find_x(self, enemy_group):
        while True:
            x = randint(800, 2800)
            if all(abs(x - enemy.rect.left) > 200 for enemy in enemy_group):
                break
        return x

    def animate(self):
        self.animation_index += 0.1 if self.type == "snail" else 0.4
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()
        self.rect.x -= 8
        if self.rect.right < 0:
            self.kill()

# Functions
def score_counter(total_time, font, screen):
    """Display the current score."""
    current_time = pygame.time.get_ticks() - total_time  # Time since the start in milliseconds
    score = font.render(f"SCORE  : {current_time // 1000}", False, "purple")
    score_rect = score.get_rect(center=(400, 50))  # Center the score on screen
    screen.blit(score, score_rect)
    return current_time // 1000  # Return score in seconds

def high_score(font_h, screen):
    """Display the high score."""
    high_score_text = font_h.render(f"HIGH SCORE  : {high_score_}", False, "black")
    high_score_rect = high_score_text.get_rect(center=(700, 50))  # Position high score at top right
    screen.blit(high_score_text, high_score_rect)

def collision_sprite():
    # Use spritecollide to get a list of all colliding enemies
    collided_enemies = pygame.sprite.spritecollide(player.sprite, enemy_group, False)  # False to not remove enemies
    
    # If there are any collisions
    if collided_enemies:
        for enemy in collided_enemies:
            # Check if the player collided with the enemy on the left or right side
            if player.sprite.rect.collidepoint(enemy.rect.midleft) or player.sprite.rect.collidepoint(enemy.rect.midright):
                enemy_group.empty()  # Clear all enemies from the group
                global collided_enemy_type
                if enemy.rect.y == 264:
                    enemy.image = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\snail\snail1.png").convert_alpha()
                    enemy.rect.midbottom = (155, 265)
                    collided_enemy_type = "snail"
                else:
                    enemy.image = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Fly\Fly1.png").convert_alpha()
                    enemy.rect.midbottom = (150, 265)
                    collided_enemy_type = "fly"
                return enemy  # Return the first enemy to indicate a collision

    return None  # No collision

def end_page_enemy(o):
    if o == "snail":
        enemy_image = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Fly\Fly1.png").convert_alpha()
        enemy_rect = enemy_image.get_rect(midbottom=(360, 212))
    else:
        enemy_image = pygame.image.load(r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\snail\snail1.png").convert_alpha()
        enemy_rect = enemy_image.get_rect(midbottom=(440, 208))
    screen.blit(enemy_image, enemy_rect)

# Initialize sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())

enemy_group = pygame.sprite.Group()

# Timer settings
custom_timer = pygame.USEREVENT + 1
pygame.time.set_timer(custom_timer, 900)

# Game variables
clock = pygame.time.Clock()
running = False
total_time = 0
start = False
final_score = 0
collided_enemy = None
collided_enemy_type = "snail"
high_score_ = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif running:
            if event.type == custom_timer:
                enemy_type = "snail" if randint(0, 1) else "fly"
                enemy_group.add(Enemy(enemy_type, enemy_group))

    if not start:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw(screen)
        pygame.draw.line(screen, "pink", (100, 100), (200, 100), 5)
        screen.blit(game_name_text, game_name_rect)
        screen.blit(start_text, start_rect)
        initial_score = font.render(f"SCORE  : {0}", False, "purple")
        initial_score_rect = initial_score.get_rect(center=(400, 50))
        screen.blit(initial_score, initial_score_rect)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            start = True
            running = True
            total_time = pygame.time.get_ticks()

    elif running:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        final_score = score_counter(total_time, font, screen)
        high_score(font_h, screen)
        player.draw(screen)
        player.update()
        enemy_group.draw(screen)
        enemy_group.update()

        collided_enemy = collision_sprite()
        if collided_enemy:
            total_time = pygame.time.get_ticks()
            player.sprite.rect.bottom = 100
            player.sprite.gravity = 0
            running = False

    else:
        bgm.stop()
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, "gold", end_rect, 0)
        pygame.draw.rect(screen, "orange", end_rect, 3)
        screen.blit(end_text, end_rect)
        pygame.draw.rect(screen, "pink", restart_rect, 0, 3)
        pygame.draw.rect(screen, "red", restart_rect, 3, 3)
        screen.blit(restart_text, restart_rect)
        final_score_text = font.render(f"SCORE  : {final_score}", False, "purple")
        final_score_rect = final_score_text.get_rect(center=(400, 50))
        screen.blit(final_score_text, final_score_rect)
        if final_score > high_score_:
            high_score_ = final_score  # Update high score if current score is higher
    
         # Display the high score at the end
        high_score(font_h, screen)

        player.update(True)
        player.draw(screen)

        screen.blit(collided_enemy.image, collided_enemy.rect)
        end_page_enemy(collided_enemy_type)

        screen.blit(game_name_text, game_name_rect)

        if pygame.mouse.get_pressed()[0]:
            if restart_rect.collidepoint(pygame.mouse.get_pos()):
                running = True
                total_time = pygame.time.get_ticks()
                player.sprite.image = player.sprite.stand_image
                player.sprite.rect.bottom = 100
                bgm.play(loops= - 1)

    pygame.display.flip()
    clock.tick(60)
