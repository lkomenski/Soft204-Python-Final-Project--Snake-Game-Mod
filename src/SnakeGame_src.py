# SOFT204 Final Project - Snake Eater
# Code edited and modified by Leena Komenski, Andrew Riley, and Olena Volkova


import pygame, sys, time, random
import os # For file path handling, for sound effects

# --- Sound Effect Setup ---
"""
Initializes sound effects for eating food.
Attempts to load 'bite.wav' from the script directory.
If the sound files are missing or cannot be loaded, disables sound effects without errors.
"""
# This section adds and sets up sound effects for the game. 
sound_path = os.path.join(os.path.dirname(__file__), 'bite.wav')
if not os.path.isfile(sound_path):
    eat_sound = None
    print(f"[!] Required sound file 'bite.wav' not found at {sound_path}. Sound effects will be disabled.")
else:
    try:
        pygame.mixer.init()
        eat_sound = pygame.mixer.Sound(sound_path)
    except Exception as e:
        eat_sound = None
        print(f"[!] Could not load sound: {e}")




# --- Window Size ---
# Window size was enlarged from 480x720
frame_size_x = 1280
frame_size_y = 720

# --- Check for Errors Encountered ---
"""
Check for errors encountered during pygame initialization.
If any errors are found, print the error count and exit the program.
Otherwise, print a success message.
"""
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# --- Initialise Game Window ---
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# --- Colors (R, G, B) ---
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# --- FPS (frames per second) Controller ---
fps_controller = pygame.time.Clock()

# --- Splash Screen and Difficulty Selection in Window ---
# This section was added and displays the splash screen and allows the player to 
# select the game difficulty by navigating through the options with the arrow keys 
# and pressing ENTER to confirm. Previously, this was hardcoded into the game logic.
def splash_screen_and_select_difficulty():
    """
    Display the splash screen and allow the user to select a difficulty level.
    Shows the game title, instructions, and difficulty options.
    User can navigate options with arrow keys or number keys, and start the game with ENTER.
    Returns:
        int: The selected difficulty value (game speed).
    """
    title_font = pygame.font.SysFont('times new roman', 60)
    info_font = pygame.font.SysFont('consolas', 28)
    small_font = pygame.font.SysFont('consolas', 22)
    difficulties = [
        ("Easy", 10),
        ("Medium", 25),
        ("Hard", 40),
        ("Harder", 60),
        ("Impossible", 120)
    ]
    selected = 0
    while True:
        game_window.fill(black)
        # Title
        title_surface = title_font.render('SNAKE EATER', True, green)
        title_rect = title_surface.get_rect(center=(frame_size_x/2, frame_size_y/6))
        game_window.blit(title_surface, title_rect)

        # Instructions
        info_surface = info_font.render('Select Difficulty:', True, white)
        info_rect = info_surface.get_rect(center=(frame_size_x/2, frame_size_y/3))
        game_window.blit(info_surface, info_rect)

        # Difficulty options
        for i, (label, _) in enumerate(difficulties):
            color = blue if i == selected else white
            diff_surface = small_font.render(f"{i+1} - {label}", True, color)
            diff_rect = diff_surface.get_rect(center=(frame_size_x/2, frame_size_y/2 + i*35))
            game_window.blit(diff_surface, diff_rect)

        # Start button
        start_surface = small_font.render('Press ENTER to Start', True, green)
        start_rect = start_surface.get_rect(center=(frame_size_x/2, frame_size_y - 60))
        game_window.blit(start_surface, start_rect)

        pygame.display.flip()
       
        # Key selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                elif event.key in [pygame.K_1, pygame.K_KP1]:
                    selected = 0
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    selected = 1
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    selected = 2
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    selected = 3
                elif event.key in [pygame.K_5, pygame.K_KP5]:
                    selected = 4
                elif event.key == pygame.K_RETURN:
                    return difficulties[selected][1]

# Show splash and get difficulty before starting the game
difficulty = splash_screen_and_select_difficulty()




# --- Game Variables ---
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# --- Game Over ---
# This module was modified to include a replay button, and modified end screen text
def game_over():
    """
    Display the end game screen and handle replay or exit.
    Shows the 'BETTER LUCK NEXT TIME' message and a replay button.
    Waits for user input to either replay the game or exit.
    """
    my_font = pygame.font.SysFont('times new roman', 90)
    button_font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = my_font.render('BETTER LUCK NEXT TIME', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    replay_surface = button_font.render('Replay', True, black)
    replay_rect = replay_surface.get_rect()
    replay_rect.center = (frame_size_x/2, frame_size_y/2)
    button_color = green

    # Added loop with replay button 
    while True:
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, 'times', 20)
        pygame.draw.rect(game_window, button_color, replay_rect.inflate(40, 20))
        game_window.blit(replay_surface, replay_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.inflate(40, 20).collidepoint(event.pos):
                    restart_game()
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
def restart_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    
# --- Score ---
def show_score(choice, color, font, size):
    """
    Display the current score on the game window.
    Args:
        choice (int): 1 to show score at the top left, 0 to show at the center bottom.
        color (pygame.Color): Color of the score text.
        font (str): Font name for the score text.
        size (int): Font size for the score text.
    """
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()



# --- Main Game Logic ---
# This section was completely refactored to modularize each key game component.
# This makes the code more organized and easier to manage and edit.
def handle_events():
    """Handle user input and quit events."""
    global change_to
    # Handle all events in the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

def update_direction():
    """Update the snake's direction, preventing reversal."""
    global direction
    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

def move_snake():
    """Move the snake in the current direction."""
    # Move the snake in the current direction
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

def grow_snake_and_check_food():
    """Grow the snake if food is eaten, play sound, and spawn new food if needed."""
    global score, food_spawn, food_pos
    # --- Snake Body Growing Mechanism ---
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
        # Added sound effect (if available)
        if eat_sound:
            eat_sound.play()
    else:
        snake_body.pop()
    # --- Spawning Food on the Screen ---
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

def draw_elements():
    """Draw the snake, food, and update the display."""
    # --- GFX ---
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    # --- Snake Food ---
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()

def check_game_over():
    """Check for collisions with walls or self."""
    # --- Game Over Conditions ---
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

def main_game_loop():
    """Main game loop, calling helper functions each frame."""
    while True:
        handle_events()         # Handle user input
        update_direction()      # Update direction
        move_snake()           # Move the snake
        grow_snake_and_check_food() # Grow snake and check for food
        check_game_over()      # Check for collisions
        draw_elements()        # Draw everything
        fps_controller.tick(difficulty) # Refresh rate / Control game speed

# Start the refactored main game loop
main_game_loop()

