# SOFT204 Final Project - Snake Eater, Snake Smarter
# Code edited and modified by Leena Komenski, Andrew Riley, and Olena Volkova


import pygame, sys, time, random
import os # For file path handling, for sound effects

# --- Sound Effect Setup ---
"""
Initializes sound effects for eating food.
Attempts to load 'bite.wav' from the script directory.
If the sound files are missing or cannot be loaded, disables sound effects without errors.
"""
# Change #1: Two new sound effects added, for eating and crashing

assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
sound_path = os.path.join(assets_dir, 'bite.wav')
crash_sound_path = os.path.join(assets_dir, 'wall-crash.wav')
eat_sound = None
crash_sound = None
try:
    pygame.mixer.init()
    if os.path.isfile(sound_path):
        eat_sound = pygame.mixer.Sound(sound_path)
    else:
        print(f"[!] Required sound file 'bite.wav' not found at {sound_path}. Sound effects will be disabled.")
    if os.path.isfile(crash_sound_path):
        crash_sound = pygame.mixer.Sound(crash_sound_path)
    else:
        print(f"[!] Required sound file 'wall-crash.wav' not found at {crash_sound_path}. Crash sound will be disabled.")
except Exception as e:
    print(f"[!] Could not load sound: {e}")
    eat_sound = None
    crash_sound = None




# --- Window Size ---

# Change #2: Window size was enlarged from 480x720

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

pygame.display.set_caption('Snake Eater, Snake Smarter') # Caption updated to match new title
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# --- Colors (R, G, B) ---
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# --- Floating Hats ---

# Change #3: Snakes wear little floating hats when food is eaten

hats = [] 
def draw_hat(x, y):
    hat_color = (135, 206, 235)    # sky blue
    tassel_color = (255, 215, 0)   # gold

    # Top of the cap
    top = (x + 20, y - 15)
    right = (x + 40, y)
    bottom = (x + 20, y + 15)
    left = (x, y)

    pygame.draw.polygon(game_window, hat_color, [top, right, bottom, left])

    # Headband (base)
    pygame.draw.rect(game_window, hat_color, pygame.Rect(x + 10, y + 15, 20, 5))

    # Tassel
    tassel_top = (x + 20, y - 15)
    tassel_knot = (x + 24, y - 5)
    tassel_bottom = (x + 24, y + 5)

    pygame.draw.line(game_window, tassel_color, tassel_top, tassel_knot, 2)
    pygame.draw.line(game_window, tassel_color, tassel_knot, tassel_bottom, 2)
    pygame.draw.circle(game_window, tassel_color, tassel_bottom, 3)


# --- Snake Color Cycle Index ---

# Change #4: Adds a color cycle for the snake

color_cycle = [
    pygame.Color(0, 255, 0),     # green
    pygame.Color(255, 255, 0),   # yellow
    pygame.Color(0, 0, 255),     # blue
    pygame.Color(128, 0, 128),   # purple
    pygame.Color(139, 69, 19),   # brown
    pygame.Color(255, 165, 0),   # orange
    pygame.Color(255, 0, 0),     # red
    pygame.Color(255, 255, 255), # white
    pygame.Color(255, 105, 180), # pink
    pygame.Color(0, 0, 139),     # dark blue
    pygame.Color(144, 238, 144)  # light green
]

# --- FPS (frames per second) Controller ---
fps_controller = pygame.time.Clock()


# --- Splash Screen and Difficulty Selection in Window ---

# Change #5: Adds a splash screen with difficulty selection, instead of the
# difficulty being hardcoded into the game. Title of the game changed.

# Splash screen visual build
def render_splash_screen(selected, difficulties, title_font, info_font, small_font):
    game_window.fill(black)
    title_surface = title_font.render('SNAKE EATER, SNAKE SMARTER', True, green) # Game title changed
    title_rect = title_surface.get_rect(center=(frame_size_x/2, frame_size_y/6))
    game_window.blit(title_surface, title_rect)
    info_surface = info_font.render('Select Difficulty:', True, white)
    info_rect = info_surface.get_rect(center=(frame_size_x/2, frame_size_y/3))
    game_window.blit(info_surface, info_rect)
    for i, (label, _) in enumerate(difficulties):
        color = blue if i == selected else white
        diff_surface = small_font.render(f"{i+1} - {label}", True, color)
        diff_rect = diff_surface.get_rect(center=(frame_size_x/2, frame_size_y/2 + i*35))
        game_window.blit(diff_surface, diff_rect)
    start_surface = small_font.render('Press ENTER to Start', True, green)
    start_rect = start_surface.get_rect(center=(frame_size_x/2, frame_size_y - 60))
    game_window.blit(start_surface, start_rect)
    pygame.display.flip()

# Splash screen event handling
def handle_splash_event(event, selected, difficulties):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type != pygame.KEYDOWN:
        return selected, False
    if event.key == pygame.K_UP:
        return (selected - 1) % len(difficulties), False
    if event.key == pygame.K_DOWN:
        return (selected + 1) % len(difficulties), False
    if event.key == pygame.K_RETURN:
        return selected, True
    number_keys = [
        (pygame.K_1, pygame.K_KP1),
        (pygame.K_2, pygame.K_KP2),
        (pygame.K_3, pygame.K_KP3),
        (pygame.K_4, pygame.K_KP4),
        (pygame.K_5, pygame.K_KP5),
    ]
    for idx, keys in enumerate(number_keys):
        if idx < len(difficulties) and event.key in keys:
            return idx, False
    return selected, False

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
        render_splash_screen(selected, difficulties, title_font, info_font, small_font)
        for event in pygame.event.get():
            selected, start = handle_splash_event(event, selected, difficulties)
            if start:
                return difficulties[selected][1]

# Show splash and get difficulty before starting the game
difficulty = splash_screen_and_select_difficulty()




# --- Game Variables ---

# Change #6: Introduces a session high score and snake color cycle as a variable

snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
high_score = 0  # Track high score for the session

snake_color_index = 0 # Sets the initial color index for the snake

# --- Game Over ---

# Change #7: This module was modified to include a replay button, display session
# high score, and modified end screen text
"""
    Display the end game screen and handle replay or exit.
    Shows the 'BETTER LUCK NEXT TIME' message and a replay button.
    Waits for user input to either replay the game or exit.
"""
def game_over(play_crash_sound=False):
    global score, high_score
    if score > high_score:
        high_score = score  # Update high score if needed

    if play_crash_sound and 'crash_sound' in globals() and crash_sound:
        crash_sound.play() # Crash sound triggered with game end
    my_font = pygame.font.SysFont('times new roman', 90)
    button_font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = my_font.render('BETTER LUCK NEXT TIME', True, red) # Change text to be more encouraging
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    replay_surface = button_font.render('Replay', True, black) # Replay button added
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

        # Handle events for replay or exit
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
                elif event.key == pygame.K_RETURN:
                    restart_game()
                    return
                    
def restart_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score, snake_color_index
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    snake_color_index = 0 # Reset snake color index

# --- Score ---

# Change #8: Visually displays a scoring system that tracks the player's score (smarts)
# and high score displayed side-by-side in game window

def show_score(choice, color, font, size):
    """
    Display the current score as 'Smarts' on the game window.
    Args:
        choice (int): 1 to show score at the top left, 0 to show at the center bottom.
        color (pygame.Color): Color of the score text.
        font (str): Font name for the score text.
        size (int): Font size for the score text.
    """
    score_font = pygame.font.SysFont(font, size)
    score_text = f"Smarts : {score}  |  High Score : {high_score}"  # Partition with vertical bar
    score_surface = score_font.render(score_text, True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x // 2, 15)  # Centered at top
    else:
        score_rect.midtop = (frame_size_x // 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)



# --- Main Game Logic ---

# Change #9: This section was completely refactored to modularize each key game component.
# This makes the code more organized and easier to manage and edit.

def handle_events():
    """Handle user gameplay input and quit events."""
    global change_to
    # Handle all events in the queue
    def set_direction_from_key(key):
        global change_to
        key_map = {
            pygame.K_UP: 'UP',
            ord('w'): 'UP',
            pygame.K_DOWN: 'DOWN',
            ord('s'): 'DOWN',
            pygame.K_LEFT: 'LEFT',
            ord('a'): 'LEFT',
            pygame.K_RIGHT: 'RIGHT',
            ord('d'): 'RIGHT'
        }
        if key in key_map:
            change_to = key_map[key]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            set_direction_from_key(event.key)
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
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10


# --- Snake Body Growing Mechanism ---

# Contains new sound effect #1, color cycling, and floating hats

def grow_snake_and_check_food():
    """
    Grow the snake if food is eaten, play sound, cycle the snake color, and spawn new food if needed.
    Each time the snake eats food, the color cycles to the next in color_cycle.
    """
    global score, food_spawn, food_pos, snake_color_index
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
        if eat_sound:
            eat_sound.play() # Plays sound effect when snake eats food
        snake_color_index = (snake_color_index + 1) % len(color_cycle) # Cycle through snake colors
        hats.append([food_pos[0], food_pos[1]]) # Add hat position when food is eaten
    else:
        snake_body.pop()

    # --- Spawning Food on the Screen ---
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

 # --- GFX ---
def draw_elements():
    """
    Draw the snake, food, floating hats, and update the display.
    The snake body is drawn using the current color from color_cycle, which cycles on each food eaten.
    Floating hats are drawn and animated above the game area when food is eaten.
    """
    game_window.fill(black)

    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, color_cycle[snake_color_index], pygame.Rect(pos[0], pos[1], 10, 10))

    # --- Snake Food ---
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    show_score(1, white, 'consolas', 20)

    # Draw and animate hats
    for hat in hats[:]:
        hat[1] -= 2  # move up
        draw_hat(hat[0], hat[1])
        if hat[1] < -20:  # remove off-screen hats
            hats.remove(hat)

    # Refresh game screen
    pygame.display.update()


# --- Game Over Conditions ---

# Contains new sound effect #2

def check_game_over():
    """Check for collisions with walls or self."""
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over(play_crash_sound=True) # Plays crash sound on wall hit
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over(play_crash_sound=True)
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
            

# --- Main Game Loop ---

# This function demonstrates the effectiveness of the refactoring
# making the actual game loop much simpler

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

