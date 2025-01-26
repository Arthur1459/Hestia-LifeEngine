# Game configuration (Must be non-mutable)

game_name = "Hestia"
version = 1.0

window_default_size = (800, 820)
fullscreen = False

fps = 30
update_rate = 0.005 # second per update

cell_size = 5
grid_size = 800 // cell_size
nb_creatures = 200
food_init_percentage = 50

food_general_lost = 0.4
food_moving_lost = 0.4
max_body_food_storage = 500

# Grid Cell types :
FOOD = -1
BASE = 0
BODY = 1
ARM = 2
REPRODUCTOR = 3
SPIKE = 5
EYES = 4