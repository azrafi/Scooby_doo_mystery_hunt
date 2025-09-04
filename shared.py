from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random  # Add random import for traps

# ---------- Window & camera ----------
WIN_W, WIN_H = 1000, 800
ASPECT = WIN_W / float(WIN_H)
fovY = 70.0

CAM_TPS = 0
CAM_FPS = 1
# New overhead camera mode (named per request)
third_person_mode = 2
camera_mode = CAM_TPS
third_person_height = 520.0  # Initial height for birdview
third_person_angle = 0.0    # Initial horizontal angle (degrees)

# Camera rig relative offsets (TPS) - restored to better working values
TPS_DIST = 250.0  # Back to the working distance for better room view
TPS_HEIGHT = 80.0  # Back to the working height for room interior visibility

# Overhead camera parameters
OVERHEAD_HEIGHT = 520.0  # how high the camera is above the scene
OVERHEAD_BACK = 120.0    # slight tilt (pull back along facing direction)

# Global rendering toggle
NO_ROOF = True  # draw with no ceilings/roof

# ---------- World layout ----------
# World is on XY plane, Z is up.
HALL_LEN = 1800.0
HALL_HALF = 120.0        # half width of the corridor
ROOM_SIZE = 400.0        # much larger square rooms for better visibility
ROOM_GAP = 500.0         # Reduced spacing so all rooms are more visible
DOOR_W = 120.0           # even wider doors for better visibility

# Door Y coordinates for 3 rooms per side - closer together
ROOM_Y = [-ROOM_GAP, 0.0, ROOM_GAP]  # Will be [-500, 0, 500]
LEFT_X = -HALL_HALF - ROOM_SIZE * 0.5   # rooms on left side of hall
RIGHT_X = HALL_HALF + ROOM_SIZE * 0.5   # rooms on right side of hall

# House dimensions
HOUSE_WIDTH = 1200.0     # wider house to accommodate larger rooms
HOUSE_LENGTH = 2400.0    # longer house
CEILING_HEIGHT = 280.0   # even higher ceiling for better view

# ---------- Player (Scooby Doo) ----------
px, py = 0.0, -HALL_LEN * 0.25
pdir = 0.0               # yaw in degrees (0 = +Y)
pspd = 180.0             # units/sec
lives = 3
invuln_t = 0.0
game_won = False         # Win condition when monster name is revealed

player_frozen = False

DIFFICULTY = 'easy'  # 'easy', 'medium', 'hard'
monster_spawn_rate = 1.0   # multiplier for monster spawn frequency
clue_switch_rate = 1.0     # multiplier for clue switching frequency
# ---------- Clues ----------
# Clues needed to reveal monster name
monster_speed_mult = 1.0  # multiplier for monster speed
clues = []  # list of dict: {x,y,got}
TOTAL_CLUES = 3  # Only 3 clues needed to reveal monster name


clue_switch_timer = 0.0
CLUE_SWITCH_BASE = 8.0  # seconds between clue switches at easy
# Create 3 clues total: place them strategically in key rooms
# Left side: 2 clues (first and third rooms)
for i in [0, 2]:  # Skip middle room on left
    clues.append({'x': LEFT_X, 'y': ROOM_Y[i], 'got': False})
# Right side: 1 clue (middle room)
clues.append({'x': RIGHT_X, 'y': ROOM_Y[1], 'got': False})

# ---------- Monster ----------
mx, my = 0.0, HALL_LEN * 0.25
m_visible = False
m_speed_base = 60.0
m_speed = m_speed_base
m_spawn_cooldown = 3.0
m_visible_timer = 0.0
m_spawn_timer = 0.0
m_name_revealed = False
m_name = "???"

# ---------- Traps ----------
traps = []  # list of dict: {x, y, active, type, timer}
trap_spawn_timer = 0.0

# ---------- Keys ----------
keys = {'w': False, 's': False, 'a': False, 'd': False, 'q': False, 'e': False}

# ---------- Boost ----------
scooby_timer = 0.0       # how long Boost lasts
scooby_cd_left = 0.0     # cooldown remaining
SCOOBY_CD = 15.0         # 15 sec cooldown
SCOOBY_DURATION = 5.0    # 5 sec boost

# ---------- Clue Timer ----------
clue_timer = 0.0

# ---------- Achievements ----------
achievements = {}
achievement_times = {}
achievement_notifications = []

# Initialize achievements
def init_achievements():
    global achievements, achievement_times
    achievements = {
        'first_clue': False,
        'all_clues': False,
        'survivor': False,
        'speedrun': False,
        'explorer': False,
        'pro_gamer': False
    }
    achievement_times = {
        'first_clue': 0.0,
        'all_clues': 0.0,
        'survivor': 0.0,
        'speedrun': 0.0,
        'explorer': 0.0,
        'pro_gamer': 0.0
    }

# Track exploration statistics
exploration_stats = {
    'rooms_visited': set(),
    'start_time': 0.0,
    'damage_taken': 0,
    'boosts_used': 0
}

# Rooms data structure for achievements
rooms = [
    {'x': LEFT_X, 'y': ROOM_Y[0], 'visited': False},
    {'x': LEFT_X, 'y': ROOM_Y[1], 'visited': False},
    {'x': LEFT_X, 'y': ROOM_Y[2], 'visited': False},
    {'x': RIGHT_X, 'y': ROOM_Y[0], 'visited': False},
    {'x': RIGHT_X, 'y': ROOM_Y[1], 'visited': False},
    {'x': RIGHT_X, 'y': ROOM_Y[2], 'visited': False}
]

# Initialize achievements at module load
init_achievements()
