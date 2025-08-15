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

    def render_screen(selected):
        game_window.fill(black)
        title_surface = title_font.render('SNAKE EATER', True, green)
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

    def handle_event(event, selected):
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

    while True:
        render_screen(selected)
        for event in pygame.event.get():
            selected, start = handle_event(event, selected)
            if start:
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
high_score = 0  # Track high score for the session

# --- Game Over ---
# This module was modified to include a replay button, and modified end screen text
def game_over():
    global score, high_score
    if score > high_score:
        high_score = score  # Update high score if needed
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
    score_text = f"Score : {score}  |  High Score : {high_score}"  # Partition with vertical bar
    score_surface = score_font.render(score_text, True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x // 2, 15)  # Centered at top
    else:
        score_rect.midtop = (frame_size_x // 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)



# --- Main Game Logic ---
# This section was completely refactored to modularize each key game component.
# This makes the code more organized and easier to manage and edit.
def handle_events():
    """Handle user input and quit events."""
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
    # Move the snake in the current direction
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

# --- Snake Body Growing Mechanism ---
def grow_snake_and_check_food():
    """Grow the snake if food is eaten, play sound, and spawn new food if needed."""
    global score, food_spawn, food_pos
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

 # --- GFX ---
def draw_elements():
    """Draw the snake, food, and update the display."""
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

# --- Game Over Conditions ---
def check_game_over():
    """Check for collisions with walls or self."""
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
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

