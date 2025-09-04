from shared import *
from Scooby_doo_mystery_hunt.shared import *


def draw_traps():
    """Draw all active traps with visual effects"""
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0

    for trap in traps:
        if not trap['active']:
            continue

        glPushMatrix()
        glTranslatef(trap['x'], trap['y'], 0)

        if trap['type'] == "spike":
            # Animated spike trap
            if trap['triggered']:
                # Spikes extended - red danger
                glColor3f(1.0, 0.2, 0.2)
                spike_height = 25
            else:
                # Spikes retracted - brown floor
                glColor3f(0.6, 0.4, 0.2)
                spike_height = 5

            # Base plate
            glPushMatrix()
            glTranslatef(0, 0, 2)
            glScalef(2.0, 2.0, 0.2)
            glutSolidCube(15)
            glPopMatrix()

            # Spikes (4 corners)
            for dx, dy in [(-8, -8), (8, -8), (-8, 8), (8, 8)]:
                glPushMatrix()
                glTranslatef(dx, dy, spike_height/2)
                glScalef(0.3, 0.3, spike_height/15)
                glutSolidCube(15)
                glPopMatrix()

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
    global traps
    traps = []
    # Corridor traps
    for i in range(3):
        x = random.uniform(-HALL_HALF + 20, HALL_HALF - 20)
        y = random.uniform(-HALL_LEN * 0.4, HALL_LEN * 0.4)
        create_trap(x, y, "spike")
    # Room traps for medium/hard
    if DIFFICULTY in ("medium", "hard"):
        for side in [LEFT_X, RIGHT_X]:
            for y in ROOM_Y:
                for i in range(2):  # 2 traps per room
                    rx = side + random.uniform(-ROOM_SIZE*0.3, ROOM_SIZE*0.3)
                    ry = y + random.uniform(-ROOM_SIZE*0.3, ROOM_SIZE*0.3)
                    create_trap(rx, ry, "spike")


def update_traps(dt):
    """Update trap states and check collisions"""
    global px, py, health, trap_spawn_timer

    # Randomly spawn new traps over time (max 6 traps at once)
    # As difficulty increases, traps spawn more frequently
    trap_spawn_timer += dt * clue_switch_rate
    if trap_spawn_timer > 5.0 and len(traps) < 6:
        x = random.uniform(-HALL_HALF + 20, HALL_HALF - 20)
        y = random.uniform(-HALL_LEN * 0.4, HALL_LEN * 0.4)
        create_trap(x, y, "spike")
        trap_spawn_timer = 0.0

    for trap in traps:
        if not trap['active']:
            continue

        trap['timer'] += dt

        # Check player collision
        dx, dy = px - trap['x'], py - trap['y']
        dist_sq = dx*dx + dy*dy

        # Mark if player is actually stepping on the trap (tight collision)
        if dist_sq < 20*20:  # Actually on the trap
            trap['player_on'] = True
        else:
            trap['player_on'] = False

        if dist_sq < 30*30:  # Close to trap
            if trap['type'] == "spike":
                # Trigger spikes with a delay
                if not trap['triggered'] and trap['timer'] > 0.5:
                    trap['triggered'] = True
                    # Damage player if still on trap when triggered
                    if dist_sq < 20*20:
                        # Track close call if player at low health
                        if lives == 1:
                            achievement_stats['close_calls'] += 1

                        # lives -= 1
                        # if lives <= 0:
                        #     reset_game()
        else:
            # Reset trap when player moves away
            if trap['triggered']:
                trap['triggered'] = False
                trap['timer'] = 0.0
                # Player successfully avoided triggered trap
                achievement_stats['traps_avoided'] += 1

