# Global variables used by the game
import config as cf

window_size = cf.window_default_size
win_width, win_height = window_size[0], window_size[1]
middle = (win_width // 2, win_height // 2)

window = None

running = False

# In game
inputs = {}
dt, t, t_key = 1/cf.update_rate, 0, 0
nb_updates = 0
pause = False

cursor = (0, 0)
id = 0

grid = None
id_updated = {}
