# Section 1: Core Engine - Person A 
from shared import *

def init_gl():
    glClearColor(0.1, 0.05, 0.15, 1)  # Dark purple background
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Brighter, warmer lighting for better colors
    # glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 0.4, 0.8, 0.0))
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.2, 1.2, 1.0, 1.0))  # Brighter, slightly warm
    # glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))  # More ambient light

def update_camera():
    global camera_mode, TPS_DIST, TPS_HEIGHT, third_person_angle, third_person_height
    if camera_mode == CAM_TPS:
        # Third-person behind the player
        back_x = px - TPS_DIST * math.sin(math.radians(pdir))
        back_y = py - TPS_DIST * math.cos(math.radians(pdir))
        
        gluLookAt(back_x, back_y, TPS_HEIGHT,  # eye
                  px, py, 20,                   # center (look at player)
                  0, 0, 1)                      # up

    elif camera_mode == CAM_FPS:
        # First-person from player's eyes
        look_x = px + 100 * math.sin(math.radians(pdir))
        look_y = py + 100 * math.cos(math.radians(pdir))
        
        gluLookAt(px, py, 50,         # eye at player height
                  look_x, look_y, 50, # look forward
                  0, 0, 1)            # up

    elif camera_mode == third_person_mode:
        # Overhead camera with adjustable height and angle
        back_distance = OVERHEAD_BACK  # Distance to pull back
        back_x = px - back_distance * math.sin(math.radians(third_person_angle))
        back_y = py - back_distance * math.cos(math.radians(third_person_angle))
        
        gluLookAt(back_x, back_y, third_person_height,  # eye position
                  px, py, 0,                            # look at player
                  0, 0, 1)                              # up vector

def update_player(dt):
    global px, py, pdir, invuln_t, scooby_timer, scooby_active, scooby_cd_left, player_frozen

    if player_frozen or lives <= 0:
        return
        
    # Speed multiplier during boost
    spd_mult = 2.0 if scooby_active else 1.0
    
    # Rotation from Q/E
    if keys['q']:
        pdir -= 120.0 * dt
    if keys['e']:
        pdir += 120.0 * dt
    
    # Proposed movement
    dx, dy = 0.0, 0.0
    if keys['w']:
        dx += math.sin(math.radians(pdir)) * pspd * spd_mult * dt
        dy += math.cos(math.radians(pdir)) * pspd * spd_mult * dt
    if keys['s']:
        dx -= math.sin(math.radians(pdir)) * pspd * spd_mult * dt
        dy -= math.cos(math.radians(pdir)) * pspd * spd_mult * dt
    if keys['a']:
        dx -= math.cos(math.radians(pdir)) * pspd * spd_mult * dt
        dy += math.sin(math.radians(pdir)) * pspd * spd_mult * dt
    if keys['d']:
        dx += math.cos(math.radians(pdir)) * pspd * spd_mult * dt
        dy -= math.sin(math.radians(pdir)) * pspd * spd_mult * dt
    
    # Collision check
    nx, ny = px + dx, py + dy
    px, py = collide_world(nx, ny)

def collide_world(nx, ny):
    # House outer bounds
    hw = HOUSE_WIDTH * 0.5
    hl = HOUSE_LENGTH * 0.5
    if nx < -hw: nx = -hw
    if nx > +hw: nx = +hw
    if ny < -hl: ny = -hl
    if ny > +hl: ny = +hl
    
    # Hall bounds (player can't enter room through walls, only doors)
    hh = HALL_HALF
    
    # Check if trying to enter rooms through walls
    for i in range(3):
        room_y = ROOM_Y[i]
        door_min = room_y - DOOR_W * 0.5
        door_max = room_y + DOOR_W * 0.5
        
        # Left rooms
        left_room_left = LEFT_X - ROOM_SIZE * 0.5
        left_room_right = LEFT_X + ROOM_SIZE * 0.5
        
        # If player is trying to enter left room area
        if nx < left_room_right and nx > left_room_left:
            # Check if they're going through the door (in door Y range)
            if ny < door_min or ny > door_max:
                # Not through door, block entrance
                if px >= left_room_right:  # Coming from hall
                    nx = left_room_right
        
        # Right rooms  
        right_room_left = RIGHT_X - ROOM_SIZE * 0.5
        right_room_right = RIGHT_X + ROOM_SIZE * 0.5
        
        # If player is trying to enter right room area
        if nx > right_room_left and nx < right_room_right:
            # Check if they're going through the door (in door Y range)
            if ny < door_min or ny > door_max:
                # Not through door, block entrance
                if px <= right_room_left:  # Coming from hall
                    nx = right_room_left
    
    # Hall width bounds (when in main hall)
    if nx > -HALL_HALF - ROOM_SIZE * 0.5 and nx < HALL_HALF + ROOM_SIZE * 0.5:
        # Player is in hall area, enforce hall width
        if nx > -hh and nx < hh:
            # In main hall, OK
            pass
        else:
            # Outside hall bounds but not in rooms - this shouldn't happen with room logic above
            if nx < 0:
                nx = -hh
            else:
                nx = hh
    
    return nx, ny

def draw_shaggy():
    # Shaggy character
    glPushMatrix()
    glTranslatef(px, py, 0)
    glRotatef(-pdir, 0, 0, 1)
    
    # Body
    glColor3f(0.4, 0.8, 0.2)  # Green shirt
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glScalef(1.2, 0.8, 2.0)
    draw_cube(15)
    glPopMatrix()
    
    # Head
    glColor3f(1.0, 0.9, 0.8)  # Skin tone
    glPushMatrix()
    glTranslatef(0, 0, 65)
    draw_sphere(8)
    glPopMatrix()
    
    # Hair
    glColor3f(0.6, 0.4, 0.0)  # Brown hair
    glPushMatrix()
    glTranslatef(0, 0, 72)
    glScalef(1.2, 1.2, 1.0)
    draw_sphere(9)
    glPopMatrix()
    
    # Eyes
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(-3, -6, 68)
    draw_sphere(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(3, -6, 68)
    draw_sphere(1)
    glPopMatrix()
    
    # Pants
    glColor3f(0.4, 0.2, 0.0)  # Brown pants
    glPushMatrix()
    glTranslatef(0, 0, 20)
    glScalef(1.0, 0.7, 1.5)
    draw_cube(12)
    glPopMatrix()
    
    # Legs
    glColor3f(1.0, 0.9, 0.8)  # Skin
    glPushMatrix()
    glTranslatef(-5, 0, 5)
    glScalef(0.6, 0.6, 1.0)
    draw_cube(8)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(5, 0, 5)
    glScalef(0.6, 0.6, 1.0)
    draw_cube(8)
    glPopMatrix()
    
    # Arms
    glPushMatrix()
    glTranslatef(-12, 0, 35)
    glScalef(0.5, 0.5, 1.2)
    draw_cube(8)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(12, 0, 35)
    glScalef(0.5, 0.5, 1.2)
    draw_cube(8)
    glPopMatrix()
    
    glPopMatrix()

def reset_game():
    global px, py, pdir, lives, invuln_t, game_won, m_name_revealed, m_name
    global m_visible, m_spawn_timer, m_visible_timer, scooby_timer, scooby_cd_left, scooby_active
    global clues, clue_timer, clue_switch_timer, traps, trap_spawn_timer
    global player_frozen
    global achievements, achievement_times, achievement_notifications, exploration_stats, rooms
    
    # Reset player
    px, py = 0.0, -HALL_LEN * 0.25
    pdir = 0.0
    lives = 3
    invuln_t = 0.0
    game_won = False
    player_frozen = False
    
    # Reset monster
    m_name_revealed = False
    m_name = "???"
    m_visible = False
    m_spawn_timer = 0.0
    m_visible_timer = 0.0
    
    # Reset Scooby boost
    scooby_timer = 0.0
    scooby_cd_left = 0.0
    scooby_active = False
    
    # Reset clues (reinitialize the list)
    clues.clear()
    for i in [0, 2]:  # Skip middle room on left
        clues.append({'x': LEFT_X, 'y': ROOM_Y[i], 'got': False})
    # Right side: 1 clue (middle room)
    clues.append({'x': RIGHT_X, 'y': ROOM_Y[1], 'got': False})
    
    clue_timer = 0.0
    clue_switch_timer = CLUE_SWITCH_BASE
    
    # Reset traps
    traps.clear()
    trap_spawn_timer = 0.0
    init_traps()
    
    # Reset achievements
    init_achievements()
    
    # Reset exploration stats
    exploration_stats['rooms_visited'].clear()
    exploration_stats['start_time'] = time.time()
    exploration_stats['damage_taken'] = 0
    exploration_stats['boosts_used'] = 0
    
    # Reset room visited status
    for room in rooms:
        room['visited'] = False

def keyboard_down(k, x, y):
    global DIFFICULTY, monster_spawn_rate, clue_switch_rate, monster_speed_mult
    global camera_mode, third_person_height, third_person_angle
    global scooby_active
    
    if k == b'r':
        reset_game()
    elif k == b'1':
        DIFFICULTY = 'easy'
        monster_spawn_rate = 1.0
        clue_switch_rate = 1.0
        monster_speed_mult = 1.0
    elif k == b'2':
        DIFFICULTY = 'medium'
        monster_spawn_rate = 1.5
        clue_switch_rate = 1.5
        monster_speed_mult = 1.3
    elif k == b'3':
        DIFFICULTY = 'hard'
        monster_spawn_rate = 2.0
        clue_switch_rate = 2.0
        monster_speed_mult = 1.6
    elif k == b'c':
        camera_mode = (camera_mode + 1) % 3
    elif k == b'u':
        # Switch to overhead view
        camera_mode = third_person_mode
    elif k == b't':
        # Switch to third person view
        camera_mode = CAM_TPS
    elif k == b'f':
        # Switch to first person view
        camera_mode = CAM_FPS
    elif k == b' ':
        # Spacebar for boost
        activate_boost()
    elif k == b'w': keys['w'] = True
    elif k == b's': keys['s'] = True
    elif k == b'a': keys['a'] = True
    elif k == b'd': keys['d'] = True
    elif k == b'q': keys['q'] = True
    elif k == b'e': keys['e'] = True

def keyboard_up(k, x, y):
    if k == b'w': keys['w'] = False
    elif k == b's': keys['s'] = False
    elif k == b'a': keys['a'] = False
    elif k == b'd': keys['d'] = False
    elif k == b'q': keys['q'] = False
    elif k == b'e': keys['e'] = False

def special_down(key, x, y):
    global third_person_height, third_person_angle
    
    if camera_mode == third_person_mode:
        if key == GLUT_KEY_UP:
            third_person_height += 20.0
            if third_person_height > 800.0:
                third_person_height = 800.0
        elif key == GLUT_KEY_DOWN:
            third_person_height -= 20.0
            if third_person_height < 100.0:
                third_person_height = 100.0
        elif key == GLUT_KEY_LEFT:
            third_person_angle -= 15.0
            if third_person_angle < -180.0:
                third_person_angle += 360.0
        elif key == GLUT_KEY_RIGHT:
            third_person_angle += 15.0
            if third_person_angle > 180.0:
                third_person_angle -= 360.0

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        activate_boost()

def activate_boost():
    global scooby_active, scooby_timer, scooby_cd_left, exploration_stats
    if boost_available():
        scooby_active = True
        scooby_timer = SCOOBY_DURATION
        scooby_cd_left = SCOOBY_CD
        exploration_stats['boosts_used'] += 1

# Utility functions
def clamp(v, a, b):
    return max(a, min(v, b))

def sqr(x):
    return x * x

def dist2(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return dx*dx + dy*dy

def saw01(period):
    return 0.5 + 0.5 * math.sin(2 * math.pi * (glutGet(GLUT_ELAPSED_TIME) / 1000.0) / period)

def draw_cube(s):
    glutSolidCube(s)

def draw_cylinder(base, top, h, slices=12, stacks=1):
    glutSolidCone(base, h, slices, stacks)

def draw_sphere(r, slices=12, stacks=12):
    glutSolidSphere(r, slices, stacks)
