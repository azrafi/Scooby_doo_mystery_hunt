from shared import *
from respawn_replay_system import*
from player_movement_and_rotation import*
from Boost import*
from trapping_system import*    

def keyboard_down(k, x, y):
    global camera_mode, third_person_height, third_person_angle
    global DIFFICULTY, monster_spawn_rate, clue_switch_rate, monster_speed_mult
    global player_frozen

    keys_down.add(k)
    if k == b'1': camera_mode = CAM_TPS
    if k == b'2': camera_mode = CAM_FPS
    if k == b'u':
        camera_mode = third_person_mode
        third_person_height = 520.0
        third_person_angle = 0.0
    if k == b'r': reset_game()
    if k == b'b' and boost_available():
        activate_boost()
    # Difficulty controls
    if k == b'm':  # Medium
        DIFFICULTY = 'medium'
        monster_speed_mult = 1.5
        clue_switch_rate = 1.5
        init_traps()  # <--- ADD THIS LINE
    if k == b'n':  # Hard
        DIFFICULTY = 'hard'
        monster_speed_mult = 2.0
        clue_switch_rate = 2.2
        init_traps()  # <--- ADD THIS LINE
    if k == b'v':  # Easy (reset)
        DIFFICULTY = 'easy'
        monster_speed_mult = 1.0
        clue_switch_rate = 1.0
    # if k == b'9' and player_frozen:
    #     player_frozen = False

def keyboard_up(k, x, y):
    if k in keys_down:
        keys_down.remove(k)

def special_down(key, x, y):
    # Camera controls with arrow keys - back to working ranges
    global pdir, TPS_DIST, TPS_HEIGHT, third_person_height, third_person_angle
    if camera_mode == third_person_mode:
        # Up/down control height, left/right control horizontal rotation
        if key == GLUT_KEY_UP:
            third_person_height = min(1200.0, third_person_height + 20.0)
        elif key == GLUT_KEY_DOWN:
            third_person_height = max(100.0, third_person_height - 20.0)
        elif key == GLUT_KEY_LEFT:
            third_person_angle = (third_person_angle + 10.0) % 360
        elif key == GLUT_KEY_RIGHT:
            third_person_angle = (third_person_angle - 10.0) % 360
        return

    # Ignore arrows while in overhead "third_person_mode"
    if camera_mode == third_person_mode:
        return

    if key == GLUT_KEY_LEFT:
        pdir += 4.0  # Rotate camera left
    elif key == GLUT_KEY_RIGHT:
        pdir -= 4.0  # Rotate camera right
    elif key == GLUT_KEY_UP:
        TPS_DIST = max(150.0, TPS_DIST - 20.0)  # Move camera closer (better min range)
        TPS_HEIGHT = max(40.0, TPS_HEIGHT - 5.0)  # Also lower camera slightly
    elif key == GLUT_KEY_DOWN:
        TPS_DIST = min(400.0, TPS_DIST + 20.0)  # Move camera further (reasonable max)
        TPS_HEIGHT = min(150.0, TPS_HEIGHT + 5.0)  # Also raise camera slightly (better max)

def mouse(button, state, x, y):
    pass



def reshape(w, h):
    global WIN_W, WIN_H, ASPECT
    WIN_W, WIN_H = max(1, w), max(1, h)
    ASPECT = WIN_W / float(WIN_H)
