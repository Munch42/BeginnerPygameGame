import pygame
import os
# Starts the font and sound aspects of pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets the name
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER_WIDTH = 10
#  So we want halfway and then push it to the left a bit because if it was exactly halfway, then the box would draw the width beyond the halfway mark
BORDER = pygame.Rect(WIDTH // 2 - (BORDER_WIDTH // 2), 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "CustomHit.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "CustomPew.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# The + 1 or 2 represents what we are adding to the code (identifier) for the user event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # Fills Screen with Colour
    # WIN.fill(WHITE)

    WIN.blit(SPACE, (0, 0))

    # This draws a rectangle so you put in the surface, the colour, and then the rectangle object.
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    # To place the text, we place it to the furthest right minus its own width so it isn't off of the screen (and then a 10 pixel padding from the edge)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Blit is for drawing a surface onto the screen
    # Basically text or images
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        # Down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        # Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        # Move it to the right
        bullet.x += BULLET_VEL

        # Did the bullet collide with the other rectangle (player)
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        # Move it to the right
        bullet.x -= BULLET_VEL

        # Did the bullet collide with the other rectangle (player)
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    text_to_draw = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(text_to_draw, (WIDTH // 2 - (text_to_draw.get_width() // 2), HEIGHT // 2 - (text_to_draw.get_height() // 2)))
    pygame.display.update()

    # Delays for 5 seconds (5000 milliseconds = 5 seconds)
    pygame.time.delay(5000)

# Main Game Loop
def main():
    #                  X    Y     Width           Height
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()

    run = True
    while run:
        # Controls the speed of the while loop
        clock.tick(FPS)

        # Gets a list of all events that are happening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

                # We need pygame.quit here because if we had it outside of the while run, then we couldn't restart the game
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # Bullet goes to the right
                    #                                              The - 2 is for half bullet height  # Width of Bullet, Height of Bullet
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + (yellow.height // 2) - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + (red.height // 2) - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            # Someone Won So Restart Main Loop After showing winner text for 5 seconds
            draw_winner(winner_text)
            break

        # This is how you move them
        # yellow.x += 1

        # print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # We pass in the "red" and "yellow" rectangles (they are rectangles just to be represented as something
        # so that we can change the position that we draw the spaceships at so we can change their x and y and then it will draw them
        # in the new position
        draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health)

    # We restart the game after we exit the run loop.
    main()

# This makes it so that it only runs it if we run it directly, and not if we import it
if __name__ == "__main__":
    main()
