from Scooby_doo_mystery_hunt.shared import *

def draw_room_box(cx, cy, open_to_hall=True):
    # Draw room walls (interior walls of a house)
    half = ROOM_SIZE * 0.5
    wall_height = 150  # Much taller walls than character
    door_width = 60
    door_height = 120

    # Room floor
    glPushMatrix()
    glTranslatef(cx, cy, 5)
    glColor3f(0.6, 0.4, 0.2)  # wooden floor
    glScalef(ROOM_SIZE, ROOM_SIZE, 10)
    glutSolidCube(1.0)
    glPopMatrix()

    # Wall thickness
    wall_thick = 10

    # Back wall (away from hallway)
    glPushMatrix()
    if cx < 0:  # left rooms - back wall is on left side
        glTranslatef(cx - half, cy, wall_height/2)
    else:  # right rooms - back wall is on right side
        glTranslatef(cx + half, cy, wall_height/2)
    glColor3f(0.9, 0.9, 0.8)  # light wall color
    glScalef(wall_thick, ROOM_SIZE, wall_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # Side walls
    for side in [-1, 1]:
        wy = cy + side * half
        glPushMatrix()
        glTranslatef(cx, wy, wall_height/2)
        glColor3f(0.9, 0.9, 0.8)
        glScalef(ROOM_SIZE, wall_thick, wall_height)
        glutSolidCube(1.0)
        glPopMatrix()

    # Front wall (towards hallway) with door opening
    door_half = door_width * 0.5

    # Wall segments beside the door
    if cx < 0:  # left rooms
        wall_x = cx + half
    else:  # right rooms
        wall_x = cx - half

    # Bottom wall segment
    glPushMatrix()
    glTranslatef(wall_x, cy - half, wall_height/2)
    glColor3f(0.9, 0.9, 0.8)
    glScalef(wall_thick, ROOM_SIZE - door_width, wall_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # Top wall segment
    glPushMatrix()
    glTranslatef(wall_x, cy + half, wall_height/2)
    glColor3f(0.9, 0.9, 0.8)
    glScalef(wall_thick, ROOM_SIZE - door_width, wall_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # Top part above door
    glPushMatrix()
    glTranslatef(wall_x, cy, door_height + (wall_height - door_height)/2)
    glColor3f(0.9, 0.9, 0.8)
    glScalef(wall_thick, door_width, wall_height - door_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # Door frame
    glColor3f(0.4, 0.2, 0.1)  # dark brown frame
    frame_thick = 5

    # Door frame sides
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(wall_x, cy + side * door_half, door_height/2)
        glScalef(frame_thick, frame_thick, door_height)
        glutSolidCube(1.0)
        glPopMatrix()

    # Door frame top
    glPushMatrix()
    glTranslatef(wall_x, cy, door_height + frame_thick/2)
    glScalef(frame_thick, door_width, frame_thick)
    glutSolidCube(1.0)
    glPopMatrix()

    # Actual door
    glColor3f(0.6, 0.3, 0.1)  # brown door
    glPushMatrix()
    if cx < 0:
        glTranslatef(wall_x - 3, cy, door_height/2)
    else:
        glTranslatef(wall_x + 3, cy, door_height/2)
    glScalef(6, door_width - 10, door_height - 10)
    glutSolidCube(1.0)
    glPopMatrix()

    # Door handle
    glColor3f(0.8, 0.8, 0.2)  # golden handle
    glPushMatrix()
    if cx < 0:
        glTranslatef(wall_x - 6, cy + 15, 70)
    else:
        glTranslatef(wall_x + 6, cy + 15, 70)
    draw_sphere(3, 6, 6)
    glPopMatrix()

def draw_floor_and_hall():
    # Floor (entire house floor)
    glColor3f(0.7, 0.5, 0.3)  # wooden color
    glPushMatrix()
    glTranslatef(0, 0, -5)
    glScalef(HOUSE_WIDTH, HOUSE_LENGTH, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Hall floor (slightly raised)
    glColor3f(0.6, 0.4, 0.25)  # slightly darker hall
    glPushMatrix()
    glTranslatef(0, 0, 2)
    glScalef(HALL_HALF * 2, HALL_LEN, 5)
    glutSolidCube(1)
    glPopMatrix()

    # House walls
    wall_h = CEILING_HEIGHT
    thick = 15
    
    # Front/back walls
    for y in [-HOUSE_LENGTH*0.5, HOUSE_LENGTH*0.5]:
        glPushMatrix()
        glTranslatef(0, y, wall_h*0.5)
        glColor3f(0.8, 0.7, 0.6)
        glScalef(HOUSE_WIDTH, thick, wall_h)
        glutSolidCube(1)
        glPopMatrix()
    
    # Left/right walls
    for x in [-HOUSE_WIDTH*0.5, HOUSE_WIDTH*0.5]:
        glPushMatrix()
        glTranslatef(x, 0, wall_h*0.5)
        glColor3f(0.8, 0.7, 0.6)
        glScalef(thick, HOUSE_LENGTH, wall_h)
        glutSolidCube(1)
        glPopMatrix()

def draw_all_rooms():
    for y in ROOM_Y:
        # left and right rooms
        glPushMatrix(); draw_room_box(LEFT_X, y); glPopMatrix()
        glPushMatrix(); draw_room_box(RIGHT_X, y); glPopMatrix()

def draw_house_decorations():
    """Add simple decorations to make the house more lively using only basic shapes"""

    # Hallway decorations - simple shapes only
    # Potted plants along the hallway
    for y in [-400, -200, 0, 200, 400]:
        for x in [-HALL_HALF - 30, HALL_HALF + 30]:
            # Pot
            glColor3f(0.4, 0.2, 0.1)  # brown pot
            glPushMatrix()
            glTranslatef(x, y, 15)
            draw_cylinder(12, 8, 20, 8, 1)
            glPopMatrix()

            # Plant
            glColor3f(0.0, 0.6, 0.0)  # green leaves
            glPushMatrix()
            glTranslatef(x, y, 35)
            for i in range(3):
                glPushMatrix()
                glRotatef(i * 120, 0, 0, 1)
                glTranslatef(8, 0, 0)
                draw_sphere(5, 6, 6)
                glPopMatrix()
            glPopMatrix()

    # Ceiling lights (if roof is enabled)
    if not NO_ROOF:
        for y in [-300, 0, 300]:
            glColor3f(1.0, 1.0, 0.8)  # warm light color
            glPushMatrix()
            glTranslatef(0, y, CEILING_HEIGHT - 20)
            draw_sphere(8, 8, 8)
            glPopMatrix()

    # Wall decorations - simple picture frames
    frame_positions = [
        (LEFT_X + ROOM_SIZE*0.4, ROOM_Y[1], 80),  # Left wall
        (RIGHT_X - ROOM_SIZE*0.4, ROOM_Y[1], 80), # Right wall
    ]
    
    for x, y, z in frame_positions:
        # Frame
        glColor3f(0.6, 0.3, 0.1)  # dark wood frame
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(30, 5, 40)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Picture (simple colored rectangle)
        glColor3f(0.2, 0.4, 0.8)  # blue picture
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(25, 2, 35)
        glutSolidCube(1.0)
        glPopMatrix()

def create_trap(x, y, trap_type="spike"):
    """Create a new trap at the given location"""
    traps.append({
        'x': x, 'y': y,
        'active': True,
        'type': trap_type,
        'timer': 0.0,
        'triggered': False
    })

def init_traps():
    """Initialize traps in hallway and rooms"""
    global traps
    traps = []
    
    # Always place some traps in hallway
    for i in range(2):
        x = random.uniform(-HALL_HALF + 20, HALL_HALF - 20)
        y = random.uniform(-HALL_LEN * 0.3, HALL_LEN * 0.3)
        create_trap(x, y, "spike")
    
    # Add more traps based on difficulty
    if DIFFICULTY == "medium":
        # Add 2 more hallway traps
        for i in range(2):
            x = random.uniform(-HALL_HALF + 20, HALL_HALF - 20)
            y = random.uniform(-HALL_LEN * 0.4, HALL_LEN * 0.4)
            create_trap(x, y, "spike")
    elif DIFFICULTY == "hard":
        # Add 3 more hallway traps + room traps
        for i in range(3):
            x = random.uniform(-HALL_HALF + 20, HALL_HALF - 20)
            y = random.uniform(-HALL_LEN * 0.4, HALL_LEN * 0.4)
            create_trap(x, y, "spike")
        
        # Add traps in some rooms
        for room_y in ROOM_Y[:2]:  # First 2 rooms
            for side in [LEFT_X, RIGHT_X]:
                trap_x = side + random.uniform(-ROOM_SIZE*0.3, ROOM_SIZE*0.3)
                trap_y = room_y + random.uniform(-ROOM_SIZE*0.3, ROOM_SIZE*0.3)
                create_trap(trap_x, trap_y, "spike")

def draw_traps():
    """Draw all active traps"""
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    
    for trap in traps:
        if not trap['active']:
            continue
            
        x, y = trap['x'], trap['y']
        
        if trap['type'] == "spike":
            # Animated spike trap
            spike_height = 8 + 6 * abs(math.sin(t * 3 + x + y))
            
            glColor3f(0.6, 0.6, 0.6)  # metallic gray
            glPushMatrix()
            glTranslatef(x, y, spike_height * 0.5)
            
            # Base
            glPushMatrix()
            glScalef(12, 12, 3)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Spikes
            for i in range(4):
                glPushMatrix()
                glTranslatef((i-1.5)*3, 0, spike_height*0.3)
                glScalef(1, 1, spike_height)
                glutSolidCube(1.0)
                glPopMatrix()
            
            glPopMatrix()

def update_traps(dt):
    """Update trap states and timers"""
    global trap_spawn_timer
    
    # Update individual trap timers
    for trap in traps:
        if trap['triggered']:
            trap['timer'] += dt
            if trap['timer'] > 2.0:  # Reset after 2 seconds
                trap['triggered'] = False
                trap['timer'] = 0.0
    
    # Check for player collision with traps
    for trap in traps:
        if not trap['active'] or trap['triggered']:
            continue
            
        dist = math.sqrt((px - trap['x'])**2 + (py - trap['y'])**2)
        if dist < 15.0:  # Player stepped on trap
            trap['triggered'] = True
            # Damage player if not invulnerable
            global lives, invuln_t
            if invuln_t <= 0:
                lives -= 1
                invuln_t = 2.0  # 2 seconds invulnerability
                print(f"Trap triggered! Lives: {lives}")

def target_for_monster():
    """Calculate where monster should move towards player"""
    # Basic AI: move towards player with some randomness
    target_x = px + random.uniform(-50, 50)
    target_y = py + random.uniform(-50, 50)
    return target_x, target_y

def try_spawn_monster(dt):
    """Try to spawn monster based on difficulty and collected clues"""
    global m_spawn_timer, m_visible, mx, my
    
    if m_visible:
        return
        
    m_spawn_timer += dt * monster_spawn_rate
    
    # Spawn chance increases with clues collected
    clue_count = sum(1 for c in clues if c['got'])
    spawn_threshold = max(1.0, 3.0 - clue_count * 0.5)
    
    if m_spawn_timer >= spawn_threshold:
        m_visible = True
        m_spawn_timer = 0.0
        # Spawn monster away from player
        place_monster_away()

def place_monster_away():
    """Place monster at a location away from player"""
    global mx, my
    
    # Try to place monster in a different area than player
    attempts = 10
    for _ in range(attempts):
        mx = random.uniform(-HALL_HALF + 30, HALL_HALF - 30)
        my = random.uniform(-HALL_LEN * 0.4, HALL_LEN * 0.4)
        
        # Make sure it's not too close to player
        if math.sqrt((mx - px)**2 + (my - py)**2) > 200:
            break

def update_monster(dt):
    """Update monster AI and movement"""
    global mx, my, m_visible_timer, m_visible, m_speed
    
    if not m_visible:
        return
        
    # Update visibility timer
    m_visible_timer += dt
    
    # Monster disappears after some time
    max_visible_time = 5.0 + collected_clues() * 2.0
    if m_visible_timer >= max_visible_time:
        m_visible = False
        m_visible_timer = 0.0
        return
    
    # Set monster speed based on clues collected
    clue_count = sum(1 for c in clues if c['got'])
    m_speed = m_speed_base * (1.0 + clue_count * 0.3) * monster_speed_mult
    
    # Simple AI: move towards player
    target_x, target_y = target_for_monster()
    
    dx = target_x - mx
    dy = target_y - my
    dist = math.sqrt(dx*dx + dy*dy)
    
    if dist > 0:
        mx += (dx / dist) * m_speed * dt
        my += (dy / dist) * m_speed * dt
    
    # Keep monster in bounds
    mx = max(-HALL_HALF + 20, min(HALL_HALF - 20, mx))
    my = max(-HALL_LEN * 0.45, min(HALL_LEN * 0.45, my))

def check_player_hit():
    """Check if monster caught the player"""
    global lives, invuln_t, m_visible
    
    if not m_visible or invuln_t > 0:
        return
        
    # Check distance to monster
    dist = math.sqrt((px - mx)**2 + (py - my)**2)
    if dist < 25.0:  # Monster caught player
        lives -= 1
        invuln_t = 2.0  # 2 seconds invulnerability
        m_visible = False  # Monster disappears after hitting
        print(f"Monster caught you! Lives: {lives}")

def draw_monster():
    """Draw the monster"""
    if not m_visible:
        return
        
    # Time-based animation
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    bob = math.sin(t * 4) * 3  # Bobbing motion
    
    glPushMatrix()
    glTranslatef(mx, my, 30 + bob)
    
    # Make monster more threatening based on clues collected
    clue_count = sum(1 for c in clues if c['got'])
    size_mult = 1.0 + clue_count * 0.2
    
    # Main body - dark and scary
    glColor3f(0.1, 0.0, 0.2)  # dark purple
    glPushMatrix()
    glScalef(size_mult, size_mult, size_mult)
    draw_sphere(20)
    glPopMatrix()
    
    # Glowing eyes
    eye_glow = 0.5 + 0.5 * math.sin(t * 6)
    glColor3f(1.0, eye_glow * 0.2, 0.0)  # red glowing eyes
    
    for eye_x in [-8, 8]:
        glPushMatrix()
        glTranslatef(eye_x * size_mult, -15 * size_mult, 5)
        draw_sphere(4)
        glPopMatrix()
    
    # Trailing smoke/mist effect
    glColor3f(0.3, 0.0, 0.4)
    for i in range(3):
        glPushMatrix()
        glTranslatef(0, 15 + i*10, -i*5)
        alpha_mult = 1.0 - i * 0.3
        glScalef(alpha_mult, alpha_mult, alpha_mult)
        draw_sphere(8)
        glPopMatrix()
    
    glPopMatrix()

def get_current_room():
    """Get which room the player is currently in"""
    # Check if player is in any room
    for i, room_y in enumerate(ROOM_Y):
        # Check left rooms
        if (abs(px - LEFT_X) < ROOM_SIZE * 0.5 and 
            abs(py - room_y) < ROOM_SIZE * 0.5):
            return i  # Room index 0, 1, 2
            
        # Check right rooms  
        if (abs(px - RIGHT_X) < ROOM_SIZE * 0.5 and 
            abs(py - room_y) < ROOM_SIZE * 0.5):
            return i + 3  # Room index 3, 4, 5
    
    return None  
    # Player is in hallway

def is_player_in_room():
    """Check if player is currently inside any room"""
    return get_current_room() is not None
