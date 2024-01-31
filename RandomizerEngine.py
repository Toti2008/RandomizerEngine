import pygame
import sys
import random
import math
import numpy as np
from pygame_gui import UIManager, elements

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
SAMPLING_RATE = 44100  # Samples per second
BIT_DEPTH = -16  # Audio bit depth

# Colors
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Spinning, Color Changes, and Dynamic Sine Wave Notes")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to draw a spinning random polygon
def draw_random_polygon(surface, color, x, y, size, rotation_angle, vertices):
    rotated_vertices = []
    for vertex in vertices:
        rotated_x = vertex[0] * math.cos(rotation_angle) - vertex[1] * math.sin(rotation_angle)
        rotated_y = vertex[0] * math.sin(rotation_angle) + vertex[1] * math.cos(rotation_angle)
        rotated_vertices.append((x + rotated_x * size, y + rotated_y * size))

    pygame.draw.polygon(surface, color, rotated_vertices)

# Function to generate a dynamic sine wave note
def generate_sine_wave(frequency, duration_ms):
    duration_sec = duration_ms / 1000.0
    time = np.arange(0, duration_sec, 1 / SAMPLING_RATE)
    samples = 32767 * np.sin(2 * np.pi * frequency * time)
    return samples.astype(np.int16)

# Function to play a random sine wave note
def play_random_note():
    frequency = random.uniform(220.0, 880.0)  # Random frequency between 220 Hz and 880 Hz
    duration = random.randint(200, 1000)  # Random duration between 200 ms and 1000 ms
    pygame.mixer.Sound(buffer=generate_sine_wave(frequency, duration)).play()

# Parameters to tweak
background_speed = 5  # Adjust the speed of background color changes
min_shape_size = 10
max_shape_size = 50
min_shapes = 5
max_shapes = 15

# Variables to store current values
randomness = random.randint(100, 200)
min_shape = random.randint(100, 200)
max_shape = random.randint(100, 200)
min_shape_size = random.randint(100, 200)
max_shape_size = random.randint(100, 200)

# Toggle for background color
random_background = True

# UI manager
ui_manager = UIManager((WIDTH, HEIGHT))

# Create a font for displaying variable values
font = pygame.font.Font(None, 24)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                random_background = not random_background  # Toggle background color

    # Handle keyboard input to change shape behavior randomly
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        randomness = random.randint(100, 200)
        min_shape = random.randint(100, 200)
        max_shape = random.randint(100, 200)
        if min_shape > max_shape:
            min_shape, max_shape = max_shape, min_shape  # Swap values
        play_random_note()
    elif keys[pygame.K_s]:
        min_shape = random.randint(100, 200)
        max_shape = random.randint(100, 200)
        if min_shape > max_shape:
            min_shape, max_shape = max_shape, min_shape  # Swap values
        play_random_note()
    elif keys[pygame.K_a]:
        min_shape = random.randint(100, 200)
        max_shape = random.randint(100, 200)
        min_shape_size = random.randint(100, 200)
        max_shape_size = random.randint(100, 200)
        if min_shape > max_shape:
            min_shape, max_shape = max_shape, min_shape  # Swap values
        if min_shape_size > max_shape_size:
            min_shape_size, max_shape_size = max_shape_size, min_shape_size  # Swap values
        play_random_note()
    elif keys[pygame.K_d]:
        min_shape_size = random.randint(100, 200)
        max_shape_size = random.randint(100, 200)
        if min_shape_size > max_shape_size:
            min_shape_size, max_shape_size = max_shape_size, min_shape_size  # Swap values
        play_random_note()

    # Rapidly change background color
    if random_background:
        background_color = random_color()
    else:
        background_color = BLACK
    screen.fill(background_color)

    # Draw many randomly generated spinning random polygons
    for _ in range(random.randint(min_shapes, max_shapes)):  # Random number of shapes
        shape_color = random_color()
        shape_size = random.randint(min_shape_size, max_shape_size)
        shape_x = random.randint(0, max(1, WIDTH - shape_size))
        shape_y = random.randint(0, HEIGHT - shape_size)
        rotation_angle = math.radians(pygame.time.get_ticks() / 10)

        # Generate random polygon with a random number of vertices
        num_vertices = random.randint(3, 8)
        vertices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_vertices)]

        draw_random_polygon(screen, shape_color, shape_x, shape_y, shape_size, rotation_angle, vertices)

    # Display variable values on the screen
    text_randomness = font.render(f"Randomness: {randomness}", True, (255, 255, 255))
    text_min_shape = font.render(f"Min Shape: {min_shape}", True, (255, 255, 255))
    text_max_shape = font.render(f"Max Shape: {max_shape}", True, (255, 255, 255))
    text_min_shape_size = font.render(f"Min Shape Size: {min_shape_size}", True, (255, 255, 255))
    text_max_shape_size = font.render(f"Max Shape Size: {max_shape_size}", True, (255, 255, 255))
    
    screen.blit(text_randomness, (10, 10))
    screen.blit(text_min_shape, (10, 40))
    screen.blit(text_max_shape, (10, 70))
    screen.blit(text_min_shape_size, (10, 100))
    screen.blit(text_max_shape_size, (10, 130))

    # Display background toggle information
    text_background_toggle = font.render(f"Background: {'Random' if random_background else 'Black'} (Press 'B' to toggle)", True, (255, 255, 255))
    screen.blit(text_background_toggle, (10, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)
    pygame.time.wait(background_speed)  # Adjust the speed of background color changes
