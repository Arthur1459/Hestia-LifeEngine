# Game configuration (Must be non-mutable)

game_name = "Hestia"
version = 1.0

window_default_size = (800, 800 + 20) # keep the format (x, x + 20)
fullscreen = False

update_rate = 0.005 # seconds minimum between 2 steps

highlight_creatures = False # Press 'H' during simulation
cell_size = 10 # it will set the size of the grid (keep it in [5, 50])
grid_size = window_default_size[0] // cell_size
nb_creatures_treshold = 50 # It will generate random creature if there is less than this amount of creature
food_init_percentage = 50 # Initial food distribution

food_general_lost = 0.4 # Press S : +0.1 | X : -0.1
food_moving_lost = 0.3 # Press D : +0.1 | V : -0.1
food_grow_proba = 1 # Press F : +0.1 | V : -0.1

max_body_food_storage = 500 # Max storage for a body (the other part of cell have a max storage of 100)
life_amount_per_food = 2 # The number of life point gave to the creature which eat the food

mutation_spread = 0.2 # the variance of the normal law which control the mutations
new_neuron_proba = 0.2 # Probabilty of a new neuron in a random layer when mutate in %
new_layer_proba = 0.1 # Probabilty of a new layer when mutate in %

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
