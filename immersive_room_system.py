from shared import *
from Scooby_doo_mystery_hunt.shared import *


def draw_floor_and_hall():
    # Main house floor - larger area (match corridor length)
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glColor3f(0.5, 0.3, 0.1)  # darker wooden floor
    glScalef(1000, HALL_LEN + 200, 5)  # Make floor match corridor length plus buffer
    glutSolidCube(1.0)
    glPopMatrix()

    # House exterior walls - match corridor length
    wall_height = 150
    wall_thick = 15
    house_width = 1000
    house_length = HALL_LEN + 100  # Slightly longer than corridor for walls

    # Front and back walls (corridor end walls)
    for z_pos in [-house_length/2, house_length/2]:
        glPushMatrix()
        glTranslatef(0, z_pos, wall_height/2)
        glColor3f(0.8, 0.8, 0.7)  # exterior wall color
        glScalef(house_width, wall_thick, wall_height)
        glutSolidCube(1.0)
        glPopMatrix()

    # Left and right walls
    for x_pos in [-house_width/2, house_width/2]:
        glPushMatrix()
        glTranslatef(x_pos, 0, wall_height/2)
        glColor3f(0.8, 0.8, 0.7)
        glScalef(wall_thick, house_length, wall_height)
        glutSolidCube(1.0)
        glPopMatrix()

    # House ceiling (removed when NO_ROOF is True)
    if not NO_ROOF:
        glPushMatrix()
        glTranslatef(0, 0, wall_height + 10)
        glColor3f(0.9, 0.9, 0.9)  # white ceiling
        glScalef(house_width - 30, house_length - 30, 20)
        glutSolidCube(1.0)
        glPopMatrix()

    # Hallway floor (match corridor length)
    glPushMatrix()
    glTranslatef(0, 0, 2)
    glColor3f(0.6, 0.4, 0.2)  # lighter hallway floor
    glScalef(HALL_HALF * 2, HALL_LEN, 3)  # Make hallway floor match corridor length
    glutSolidCube(1.0)
    glPopMatrix()


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

def draw_all_rooms():
    for y in ROOM_Y:
        # left and right rooms
        glPushMatrix(); draw_room_box(LEFT_X, y); glPopMatrix()
        glPushMatrix(); draw_room_box(RIGHT_X, y); glPopMatrix()

