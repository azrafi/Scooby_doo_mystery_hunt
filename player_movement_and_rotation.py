from shared import *


def clamp(v, a, b):
    return a if v < a else (b if v > b else v)



def update_player(dt):
    global px, py, pdir, player_frozen
    # If frozen, don't allow movement
    if player_frozen:
        return

    move = 0.0
    strafe = 0.0
    rot = 0.0

    # WASD for movement relative to player direction
    if b'w' in keys_down: move += 1.0
    if b's' in keys_down: move -= 1.0
    if b'a' in keys_down: strafe -= 1.0
    if b'd' in keys_down: strafe += 1.0
    if b't' in keys_down: rot -= 0.4  # Rotate right (clockwise)
    if b'f' in keys_down: rot += 0.4  # Rotate left (counterclockwise)

    pdir += rot
    rad = math.radians(pdir)
    fx = math.sin(rad)
    fy = math.cos(rad)
    nx = math.sin(rad + math.pi/2)
    ny = math.cos(rad + math.pi/2)
    # Only slow down if player is actually stepping on a trap
    slow_factor = 1.0
    for trap in traps:
        if trap.get('player_on', False):
            slow_factor = 0.3  # Significantly slow down
            break
    speed = pspd * (1.2 if scooby_active else 1.0) * slow_factor

    px += (fx * move + nx * strafe) * speed * dt
    py += (fy * move + ny * strafe) * speed * dt
    # Collision with corridor/rooms: clamp inside corridor or inside any room
    px, py = collide_world(px, py)
    # After movement, check for trap collision in rooms
    if DIFFICULTY in ("medium", "hard"):
        for trap in traps:
            # Only check traps inside rooms
            for room_y in ROOM_Y:
                if ((trap['x'], trap['y']) == (LEFT_X, room_y) or (trap['x'], trap['y']) == (RIGHT_X, room_y)):
                    if abs(px - trap['x']) < 20 and abs(py - trap['y']) < 20:
                        player_frozen = True
                        return




def collide_world(nx, ny):
    """Enhanced collision system for walls and furniture"""
    player_radius = 15  # Player collision radius

    # World boundaries - keep player within reasonable bounds
    world_half = 1000
    nx = clamp(nx, -world_half, world_half)
    ny = clamp(ny, -world_half, world_half)

    # Check if player is trying to enter a room through a door
    door_half = DOOR_W * 0.5
    room_half = ROOM_SIZE * 0.5

    for room_y in ROOM_Y:
        # Check door entry for left rooms
        left_door_x = LEFT_X + room_half  # Door is on the right side of left room (facing corridor)
        if (left_door_x - 30 <= nx <= left_door_x + 30 and
            room_y - door_half <= ny <= room_y + door_half):
            # Player is in door area for left room - allow free movement
            # Clamp Y to door height to prevent slipping through corners
            ny = clamp(ny, room_y - door_half, room_y + door_half)
            return nx, ny

        # Check door entry for right rooms
        right_door_x = RIGHT_X - room_half  # Door is on the left side of right room (facing corridor)
        if (right_door_x - 30 <= nx <= right_door_x + 30 and
            room_y - door_half <= ny <= room_y + door_half):
            # Player is in door area for right room - allow free movement
            ny = clamp(ny, room_y - door_half, room_y + door_half)
            return nx, ny

    # Check furniture collisions in each room
    for room_y in ROOM_Y:
        # Left room furniture collision
        if (LEFT_X - room_half <= nx <= LEFT_X + room_half and
            room_y - room_half <= ny <= room_y + room_half):

            # Table collision (table at LEFT_X - 30, room_y, size 60x40)
            table_x, table_y = LEFT_X - 30, room_y
            table_w, table_h = 60, 40
            if (table_x - table_w*0.5 - player_radius <= nx <= table_x + table_w*0.5 + player_radius and
                table_y - table_h*0.5 - player_radius <= ny <= table_y + table_h*0.5 + player_radius):
                # Push player away from table
                dx = nx - table_x
                dy = ny - table_y
                if abs(dx) > abs(dy):
                    nx = table_x + (table_w*0.5 + player_radius) * (1 if dx > 0 else -1)
                else:
                    ny = table_y + (table_h*0.5 + player_radius) * (1 if dy > 0 else -1)

            # Chair collision (chair at LEFT_X + 40, room_y, size 30x30)
            chair_x, chair_y = LEFT_X + 40, room_y
            chair_size = 30
            if (chair_x - chair_size*0.5 - player_radius <= nx <= chair_x + chair_size*0.5 + player_radius and
                chair_y - chair_size*0.5 - player_radius <= ny <= chair_y + chair_size*0.5 + player_radius):
                # Push player away from chair
                dx = nx - chair_x
                dy = ny - chair_y
                if abs(dx) > abs(dy):
                    nx = chair_x + (chair_size*0.5 + player_radius) * (1 if dx > 0 else -1)
                else:
                    ny = chair_y + (chair_size*0.5 + player_radius) * (1 if dy > 0 else -1)

        # Right room furniture collision
        if (RIGHT_X - room_half <= nx <= RIGHT_X + room_half and
            room_y - room_half <= ny <= room_y + room_half):

            # Bookshelf collision (bookshelf at RIGHT_X + 40, room_y, size 25x80)
            shelf_x, shelf_y = RIGHT_X + 40, room_y
            shelf_w, shelf_h = 25, 80
            if (shelf_x - shelf_w*0.5 - player_radius <= nx <= shelf_x + shelf_w*0.5 + player_radius and
                shelf_y - shelf_h*0.5 - player_radius <= ny <= shelf_y + shelf_h*0.5 + player_radius):
                # Push player away from bookshelf
                dx = nx - shelf_x
                dy = ny - shelf_y
                if abs(dx) > abs(dy):
                    nx = shelf_x + (shelf_w*0.5 + player_radius) * (1 if dx > 0 else -1)
                else:
                    ny = shelf_y + (shelf_h*0.5 + player_radius) * (1 if dy > 0 else -1)

    # Wall collision system
    # Check if player is in corridor area
    if -HALL_HALF - 50 <= nx <= HALL_HALF + 50:  # Expanded corridor area for door access
        # In main corridor, keep within hallway bounds but allow door access
        if abs(nx) <= HALL_HALF:
            # Pure corridor - apply corridor end wall collision
            ny = clamp(ny, -HALL_LEN*0.5 + player_radius, HALL_LEN*0.5 - player_radius)
            nx = clamp(nx, -HALL_HALF + player_radius, HALL_HALF - player_radius)
            return nx, ny
        else:
            # Near room entrances - check for door access
            for room_y in ROOM_Y:
                # Check if trying to access left room door
                if (nx < -HALL_HALF and
                    room_y - door_half <= ny <= room_y + door_half):
                    # Clamp Y to door height
                    ny = clamp(ny, room_y - door_half, room_y + door_half)
                    return nx, ny

                # Check if trying to access right room door
                if (nx > HALL_HALF and
                    room_y - door_half <= ny <= room_y + door_half):
                    ny = clamp(ny, room_y - door_half, room_y + door_half)
                    return nx, ny

            # Not accessing door, push back to corridor
            if nx < -HALL_HALF:
                nx = -HALL_HALF + player_radius
            elif nx > HALL_HALF:
                nx = HALL_HALF - player_radius
            # Also apply corridor end wall collision here
            ny = clamp(ny, -HALL_LEN*0.5 + player_radius, HALL_LEN*0.5 - player_radius)
            return nx, ny

    # Check room boundaries and walls
    for room_y in ROOM_Y:
        # Left room boundary check
        if (LEFT_X - room_half <= nx <= LEFT_X + room_half and
            room_y - room_half <= ny <= room_y + room_half):

            # Keep player inside room with padding, but allow door exit
            room_left = LEFT_X - room_half + player_radius
            room_right = LEFT_X + room_half - player_radius
            room_bottom = room_y - room_half + player_radius
            room_top = room_y + room_half - player_radius

            # Allow exit through door
            if (nx >= LEFT_X + room_half - 30 and
                room_y - door_half <= ny <= room_y + door_half):
                # Exiting through door
                return nx, ny

            nx = clamp(nx, room_left, room_right)
            ny = clamp(ny, room_bottom, room_top)
            return nx, ny

        # Right room boundary check
        if (RIGHT_X - room_half <= nx <= RIGHT_X + room_half and
            room_y - room_half <= ny <= room_y + room_half):

            # Keep player inside room with padding, but allow door exit
            room_left = RIGHT_X - room_half + player_radius
            room_right = RIGHT_X + room_half - player_radius
            room_bottom = room_y - room_half + player_radius
            room_top = room_y + room_half - player_radius

            # Allow exit through door
            if (nx <= RIGHT_X - room_half + 30 and
                room_y - door_half <= ny <= room_y + door_half):
                # Exiting through door
                return nx, ny

            nx = clamp(nx, room_left, room_right)
            ny = clamp(ny, room_bottom, room_top)
            return nx, ny

    # Default: keep in corridor bounds
    nx = clamp(nx, -HALL_HALF + player_radius, HALL_HALF - player_radius)
    ny = clamp(ny, -HALL_LEN*0.5 + player_radius, HALL_LEN*0.5 - player_radius)

    return nx, ny





def draw_shaggy():
    # More detailed Shaggy with arms, legs, hands
    glPushMatrix()

    # Head
    glColor3f(1.0, 0.8, 0.6)  # skin color
    glPushMatrix()
    glTranslatef(0, 0, 70)
    draw_sphere(12)
    glPopMatrix()

    # Hair (messy brown)
    glColor3f(0.4, 0.2, 0.1)
    glPushMatrix()
    glTranslatef(0, 0, 78)
    glutSolidCube(18)
    glPopMatrix()

    # Torso
    glColor3f(0.2, 0.8, 0.2)  # green shirt
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glScalef(1.2, 0.8, 1.8)
    glutSolidCube(24)
    glPopMatrix()

    # Arms
    glColor3f(0.2, 0.8, 0.2)  # green sleeves
    for dx in (-18, 18):
        # Upper arm
        glPushMatrix()
        glTranslatef(dx, 0, 50)
        glRotatef(20 if dx < 0 else -20, 0, 1, 0)
        draw_cylinder(4, 4, 18)
        glPopMatrix()

        # Lower arm
        glColor3f(1.0, 0.8, 0.6)  # skin
        glPushMatrix()
        glTranslatef(dx + (8 if dx > 0 else -8), 0, 32)
        glRotatef(10 if dx < 0 else -10, 0, 1, 0)
        draw_cylinder(3.5, 3.5, 15)
        glPopMatrix()

        # Hand
        glPushMatrix()
        glTranslatef(dx + (12 if dx > 0 else -12), 0, 20)
        draw_sphere(4)
        glPopMatrix()
        glColor3f(0.2, 0.8, 0.2)  # reset to green

    # Legs
    glColor3f(0.4, 0.3, 0.1)  # brown pants
    for dx in (-6, 6):
        # Upper leg (thigh) - vertical cylinder going down
        glPushMatrix()
        glTranslatef(dx, 0, 20)  # start higher
        draw_cylinder(5, 5, 20)  # vertical cylinder (no rotation needed)
        glPopMatrix()

        # Lower leg (shin) - vertical cylinder going down
        glPushMatrix()
        glTranslatef(dx, 0, 0)  # lower position
        draw_cylinder(4, 4, 18)  # vertical cylinder (no rotation needed)
        glPopMatrix()

        # Feet
        glColor3f(0.1, 0.1, 0.1)  # black shoes
        glPushMatrix()
        glTranslatef(dx, 4, -15)  # slightly forward and down
        glScalef(1.5, 2.0, 0.8)
        glutSolidCube(8)
        glPopMatrix()
        glColor3f(0.4, 0.3, 0.1)  # reset to brown

    glPopMatrix()
