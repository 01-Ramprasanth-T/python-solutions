import pygame
from sys import exit

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
PINK = (255, 102, 155)
LIGHT_BLUE = "#E5CCFF"
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

# File paths
FONT_PATH = r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\font\Pixeltype.ttf"
GROUND_PATH = r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\ground.png"
SKY_PATH = r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Sky.png"
SNAIL_PATH = r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\snail\snail1.png"
PLAYER_PATH = r"C:\Users\Ramprasanth.T\OneDrive\Documents\pygame\resources\UltimatePygameIntro\graphics\Player\player_stand.png"

def load_resources():
    """Load all resources such as fonts and images."""
    font = pygame.font.Font(FONT_PATH, 60)
    platform_surface = pygame.image.load(GROUND_PATH).convert()
    sky_surface = pygame.image.load(SKY_PATH).convert()
    snail = pygame.image.load(SNAIL_PATH).convert_alpha()
    player = pygame.image.load(PLAYER_PATH).convert_alpha()
    return font, platform_surface, sky_surface, snail, player

def main():
    """Main function to run the game."""
    pygame.init()
    display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("game")

    # Load resources
    font, platform_surface, sky_surface, snail, player = load_resources()

    # Render text
    title_text = font.render("Running Snail", False, PURPLE)
    title_rect = title_text.get_rect(center=(400, 50))
    warning_text = font.render("warning", False, "red")

    # Create rectangles for images
    snail_rect = snail.get_rect(midbottom=(800, 310))
    player_rect = player.get_rect(midbottom=(200, 310))

    # Create a block surface
    block = pygame.Surface((50, 50))
    block.fill(PINK)
    block_rect = block.get_rect(center=(400, 200))

    # Initialize clock and control variables
    clock = pygame.time.Clock()
    stop = 1
    dragging = False
    click = False
    live = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and block_rect.collidepoint(event.pos):
                    dragging = True
                elif event.button == 2 and block_rect.collidepoint(event.pos):
                    click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 2 and block_rect.collidepoint(event.pos):
                    click = False
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    block_rect.center = event.pos

        # Draw background elements
        display_screen.blit(sky_surface, (0, 0))
        display_screen.blit(platform_surface, (0, 300))
        pygame.draw.rect(display_screen, WHITE, title_rect, 0, 6)
        pygame.draw.rect(display_screen, PURPLE, title_rect, 2, 6)
        display_screen.blit(title_text, title_rect)
        pygame.draw.rect(display_screen, BLACK, (0, 0, SCREEN_WIDTH, 20))
        pygame.draw.rect(display_screen, BLACK, (0, 365, SCREEN_WIDTH, 35))

        # Move snail
        if stop:
            if snail_rect.left >= -90:
                snail_rect.left -= 6
            else:
                snail_rect.left = 800

        stop = 1
        display_screen.blit(snail, snail_rect)

        # Handle mouse interactions with snail
        point_m = pygame.mouse.get_pos()
        rcl = pygame.mouse.get_pressed()
        if snail_rect.collidepoint(point_m):
            if rcl[1]:
                stop = 0
            elif rcl[0]:
                snail_rect.left -= 3
            elif rcl[2]:
                snail_rect.left += 3

        # Draw player and check for collisions
        if not click:
            if not player_rect.collidepoint(point_m) or dragging:
                display_screen.blit(player, player_rect)
                if player_rect.colliderect(snail_rect):
                    display_screen.blit(warning_text, (345, 100))
                    live -= 1

        # Draw block and circle
        display_screen.blit(block, block_rect)
        pygame.draw.circle(display_screen, LIGHT_BLUE, block_rect.center, (block_rect.width - 1) // 2)

        # Check for game over
        if live <= 0:
            pygame.quit()
            exit()

        # Draw health bar
        x = live * 1.40
        pygame.draw.rect(display_screen, GREEN, (130, 185, x, 10), 0, 5)
        pygame.draw.rect(display_screen, GREY, (130, 185, 140, 10), 2, 5)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

# Initialize the blink variables
blink_start_time = None  # Time when the blink starts
blink_duration = 500  # Blink duration in milliseconds (e.g., 500ms = half a second)
blink_interval = 100  # Interval between toggling visibility in milliseconds
blink_visible = True  # Flag to toggle visibility of the score

def score_counter(total_time, font, screen):
    """Display the current score with blinking effect."""
    global blink_start_time, blink_visible
    
    current_time = pygame.time.get_ticks() - total_time  # Time since the start in milliseconds
    score = current_time // 1000  # Score in seconds
    
    # Check if the score exceeds high score or if it's a multiple of 100
    if score > high_score_ or score % 100 == 0:
        if blink_start_time is None:
            blink_start_time = pygame.time.get_ticks()  # Start the blink effect
        
        # If blinking is active, calculate the time since it started
        blink_elapsed_time = pygame.time.get_ticks() - blink_start_time
        if blink_elapsed_time < blink_duration:
            # Toggle score visibility
            if blink_elapsed_time % blink_interval < blink_interval // 2:
                blink_visible = True
            else:
                blink_visible = False
        else:
            # Stop the blinking effect after the duration
            blink_start_time = None
            blink_visible = True  # Ensure score is visible after the blink ends

    # Display the score if it's visible
    if blink_visible:
        score_text = font.render(f"SCORE  : {score}", False, "purple")
        score_rect = score_text.get_rect(center=(400, 50))
        screen.blit(score_text, score_rect)
    
    return score

def high_score(current_score, font_h, screen):
    """Display the high score."""
    global high_score_
    if current_score > high_score_:
        high_score_ = current_score  # Update high score if current score is higher
    
    # Display the high score at the top right corner
    high_score_text = font_h.render(f"HIGH SCORE  : {high_score_}", False, "black")
    high_score_rect = high_score_text.get_rect(center=(700, 50))  # Position high score at top right
    screen.blit(high_score_text, high_score_rect)
