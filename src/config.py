# Game configuration (Must be non-mutable)

game_name = "Hestia"
version = 1.0

window_default_size = (1200, 1200 + 20)
fullscreen = False

fps = 30
update_rate = 0.005 # second per update

highlight_creatures = False
cell_size = 10
grid_size = window_default_size[0] // cell_size
nb_creatures_treshold = 50
food_init_percentage = 50

food_general_lost = 0.4
food_moving_lost = 0.3
max_body_food_storage = 500
food_grow_proba = 1

# Grid Cell types :
WALL = -3
MYBODY = -2
FOOD = -1
BASE = 0
BODY = 1
ARM = 2
REPRODUCTOR = 3
EYES = 4
SPIKE = 5

SPIKE_KILLABLE = (BODY, ARM, REPRODUCTOR, EYES, SPIKE)
CAN_MOVE_ON = (BASE, FOOD)
BELONG_CREATURE = (ARM, BODY, REPRODUCTOR, SPIKE, EYES)

# Colors
base_color = (50, 20, 0)
food_color = (30, 100, 0)
body_color = (0, 0, 100)
arm_color = (120, 200, 200)
reproductor_color = (200, 140, 40)
eyes_color = (100, 0, 200)
spike_color = (130, 0, 0)
