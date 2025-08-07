import pytest

def test_score_increment():
    snake_pos = [100, 50]
    food_pos = [100, 50]
    score = 0
    food_spawn = True

    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False

    assert score == 1
    assert food_spawn is False

def test_direction_change_prevention():
    direction = 'UP'
    change_to = 'DOWN'

    # Prevent reversal
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Should not allow reversal
    assert direction == 'UP'

def test_out_of_bounds_detection():
    frame_size_x = 720
    frame_size_y = 480
    snake_pos = [730, 50]  # Out of bounds on X

    out_of_bounds = (
        snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or
        snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10
    )

    assert out_of_bounds is True
