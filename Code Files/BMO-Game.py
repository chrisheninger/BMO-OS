import pygame
import sys
import RPi.GPIO as GPIO
import random
import base64
from io import BytesIO

# Initialize Pygame
pygame.init()

# GPIO setup
GPIO.setmode(GPIO.BCM)
buttons = {
    17: "up",
    27: "right",
    22: "down",
    23: "left",
    24: "triangle",
    25: "small circle",
    26: "large circle",
}

for pin in buttons.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Constants
WHITE = (217, 255, 234)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 480
PLATFORM_HEIGHT = 20
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 50
SPEED = 5
JUMP_FORCE = 15
GRAVITY = 0.8
NUM_PLATFORMS = 21
PLATFORM_WIDTH = 280
PLATFORM_GAP = 100
PLATFORM_Y_VARIATION = 60
LEVEL_WIDTH = (PLATFORM_WIDTH + PLATFORM_GAP) * NUM_PLATFORMS
LANDING_MARGIN = 2  # A small buffer zone for landing detection
COIN_RADIUS = 10
WIN_SCORE = NUM_PLATFORMS - 1

# Player sprite image
image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAFAAAAAyCAYAAADLLVz8AAAAAXNSR0IArs4c6QAAAr5JREFUaEPtmlFywyAMROP7H9odZ6qOogK7C7LjEPpZhFg9CQFut8f6GSKwDc1ekx8fD3Df9/3sPG7bVuU0BcBWgKNwjwQNAXx3hhEAC/AMnQe4FIDvzLACMFOnT8xwBVomUDDqOJNh5JMNFPmJ46xf2ANZR2cJRH7frW96gKiH1cbZxEwNEEFojaO5tjOGANrJ12qyNRtW4NRbeAF84JdIVqX0nnJTVyAKrjWelRjVD7NrDt2s36Ee6AHF04w9/ZAdShIbqPm5LUDL2t/p1HiAKxnOBoj8edC1i75PeloFssIYgYovtQJZ38wV5/B1S4DKtl4AC5+LegGy1cXafewW7gHIQlHtSlq6e6C6OLJnMly6P8bfZX7GUtejeyCC0TuOMty6KvnTPN4CWnoQcK8J7YZ/AO2e5AWgBXvh1YKurafAHtGEkvbCBhnHbDDCEHAlw4o+RptqI1XgHTO8AIKUowyfDRCtj8ZfeuDdK7CUi1qAzJvX93ul73b3QLV/xFNSAcCuNQKwpuf4vQGVKlAJ8KoMI5AxwNItwgNh/N0GYEaGmYD99lMBokJIr0BVYAQQBSOBKkCzR2Bie2m1gpQ/rEdhMbBWE25toa8DeHWGeysQzWPjQAnufgtftUUQCBQgmo/Gkf9ugGjhrAyjdVCAaD4aR/5PBzgqkJmPbEbHUw+RUTGlUxl9fOhdE1WP96vY+nlUBfYGwM6bGmALgpI1xZYFj+yUNRVbf4eEFbgAlgkY8AXwlw/7pjac1na+GmDtWWovJ+Zz1/QAWy0I/V9j/EhRsn8CVBuovySzJ6i6hrdHc1ElocOmNF7a0lWABrFnobPmRLEIErPdFK0yQHTaxuapiCldnrP9MdtN1cwkBfZANhOsuGx/pRaEtjyrlbFbABlKDZspAMYezh5sg+ye0yHAM8QxvSUjuCt8/AA2uRR+CtQNlAAAAABJRU5ErkJggg=="
image_data = BytesIO(base64.b64decode(image_base64))
player_image = pygame.image.load(image_data)
player_frame1 = player_image.subsurface((0, 0, PLAYER_WIDTH, PLAYER_HEIGHT))
player_frame2 = player_image.subsurface(
    (PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT))

# Platforms
platforms = [pygame.Rect(0, 380 - random.randint(-PLATFORM_Y_VARIATION,
                         PLATFORM_Y_VARIATION), random.randint(180, 280), PLATFORM_HEIGHT)]
for i in range(1, NUM_PLATFORMS):
    prev_platform = platforms[-1]
    x_position = prev_platform.x + prev_platform.width + PLATFORM_GAP
    platforms.append(pygame.Rect(x_position, 380 - random.randint(-PLATFORM_Y_VARIATION,
                     PLATFORM_Y_VARIATION), random.randint(180, 280), PLATFORM_HEIGHT))

# Coins (positioned on random platforms except the first)
coins = [pygame.Vector2(platform.x + random.randint(20, platform.width - COIN_RADIUS * 2 - 20),
                        platform.y - COIN_RADIUS * 2) for platform in platforms[1:]]

# Player
player_pos = [platforms[0].x + platforms[0].width // 2 -
              PLAYER_WIDTH // 2, platforms[0].y - PLAYER_HEIGHT]
player_velocity = [0, 0]
is_jumping = False
score = 0
high_score = 0
is_winner = False

# Camera
camera_pos = [0, 0]

# Window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("2D Platformer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Game loop
while True:
    screen.fill(BLACK)

    # Check for win condition
    if score >= WIN_SCORE and not is_winner:
        is_winner = True
        print("YOU WIN!")

    # If the player has won, prevent any additional input
    if not is_winner:
        player_rect = pygame.Rect(
            player_pos[0], player_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)

        # Player movement
        moving_left = False
        moving_right = False

        if not GPIO.input(23):  # Left (button pressed)
            player_velocity[0] = -SPEED
            moving_left = True
        elif not GPIO.input(27):  # Right (button pressed)
            player_velocity[0] = SPEED
            moving_right = True
        else:
            # Reset horizontal velocity if neither left nor right is pressed
            player_velocity[0] = 0

        if (not GPIO.input(26) or not GPIO.input(25)) and not is_jumping:
            player_velocity[1] = -JUMP_FORCE
            is_jumping = True

        if not GPIO.input(24):
            print("Exiting the game...")
            pygame.quit()
            GPIO.cleanup()
            sys.exit()

        # Gravity
        player_velocity[1] += GRAVITY

        # Collision detection for coins
        for coin in coins[:]:
            coin_rect = pygame.Rect(
                coin.x, coin.y, COIN_RADIUS * 2, COIN_RADIUS * 2)
            if player_rect.colliderect(coin_rect):
                coins.remove(coin)
                # Increment score or perform other actions when a coin is collected
                score += 1

        # Draw coins
        for coin in coins:
            pygame.draw.circle(screen, WHITE, (int(
                coin.x - camera_pos[0]), int(coin.y - camera_pos[1])), COIN_RADIUS)
            pygame.draw.circle(screen, BLACK, (int(
                coin.x - camera_pos[0]), int(coin.y - camera_pos[1])), COIN_RADIUS - 3)

        # Collision detection and score increment
        on_platform = False
        for index, platform in enumerate(platforms):
            # Modify the player's rectangle to include the landing margin
            landing_rect = player_rect.inflate(0, LANDING_MARGIN)
            if platform.colliderect(landing_rect) and player_velocity[1] >= 0:
                # Set the player's position to be above the platform
                player_pos[1] = platform.y - PLAYER_HEIGHT
                player_velocity[1] = 0  # Stop vertical movement
                is_jumping = False
                on_platform = True
            pygame.draw.rect(screen, WHITE, (platform.x -
                                             camera_pos[0], platform.y - camera_pos[1], platform.width, platform.height))

        # If the player is not on any platform, they should be in a jumping state
        if not on_platform:
            is_jumping = True

        # Update player position
        player_pos[0] += player_velocity[0]
        player_pos[1] += player_velocity[1]

        camera_pos[0] = player_pos[0] - WIDTH // 2
        camera_pos[0] = max(0, min(camera_pos[0], LEVEL_WIDTH - WIDTH))

        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > LEVEL_WIDTH - PLAYER_WIDTH:
            player_pos[0] = LEVEL_WIDTH - PLAYER_WIDTH

        if player_pos[1] > HEIGHT + PLAYER_HEIGHT:
            print("Fell down! Resetting...")
            player_pos = [platforms[0].x + platforms[0].width // 2 -
                          PLAYER_WIDTH // 2, platforms[0].y - PLAYER_HEIGHT]
            player_velocity = [0, 0]
            is_jumping = False
            camera_pos = [0, 0]
            high_score = max(high_score, score)
            score = 0
            # Reset Coins (positioned on random platforms except the first)
            coins = [pygame.Vector2(platform.x + random.randint(20, platform.width - COIN_RADIUS * 2 - 20),
                                    platform.y - COIN_RADIUS * 2) for platform in platforms[1:]]

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(
            f"High Score: {high_score}", True, WHITE)
        high_score_position = (WIDTH - high_score_text.get_width() - 10, 10)
        screen.blit(high_score_text, high_score_position)

        # Display player sprite (mirrored if moving left)
        if is_jumping:
            player_image = player_frame2
        else:
            player_image = player_frame1

        # Flip the image horizontally if moving left
        if moving_left:
            player_image = pygame.transform.flip(player_image, True, False)

        screen.blit(player_image, (int(
            player_pos[0] - camera_pos[0]), int(player_pos[1] - camera_pos[1])))

    else:
        win_text = font.render("YOU WIN!", True, WHITE)
        win_text_position = (WIDTH // 2 - win_text.get_width() //
                             2, HEIGHT // 2 - win_text.get_height() // 2)
        screen.blit(win_text, win_text_position)

        if not GPIO.input(24):
            print("Exiting the game...")
            pygame.quit()
            GPIO.cleanup()
            sys.exit()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            GPIO.cleanup()
            sys.exit()

    clock.tick(60)
