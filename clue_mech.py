from Scooby_doo_mystery_hunt.shared import *



def draw_clues_and_pickup():
    pulse = 0.5 + 0.5 * abs(0.5 - saw01(1.5)) * 2.0  # glow 0..1
    picked = 0
    for i, c in enumerate(clues):
        if not c['got']:
            # Different colors for each clue based on room
            colors = [
                (1.0, 0.2, 0.2),  # red
                (0.2, 1.0, 0.2),  # green
                (0.2, 0.2, 1.0),  # blue
                (1.0, 1.0, 0.2),  # yellow
                (1.0, 0.2, 1.0),  # magenta
                (0.2, 1.0, 1.0),  # cyan
            ]
            color = colors[i % len(colors)]

            # Draw floating, rotating clue - BIGGER AND MORE VISIBLE
            glPushMatrix()
            glTranslatef(c['x'], c['y'], 20 + 8 * abs(0.5 - saw01(2.0)))  # higher floating motion
            glRotatef(glutGet(GLUT_ELAPSED_TIME) * 0.05 * (i + 1), 0, 0, 1)  # rotation

            # Main clue body - MUCH BIGGER
            glColor3f(color[0] * pulse, color[1] * pulse, color[2] * pulse)
            draw_sphere(15)  # Much bigger clue sphere

            # Sparkle effect - BIGGER
            glColor3f(1.0, 1.0, 1.0)
            for angle in range(0, 360, 45):  # More sparkles
                glPushMatrix()
                glRotatef(angle, 0, 0, 1)
                glTranslatef(20, 0, 0)  # Further out sparkles
                draw_sphere(4)  # Bigger sparkles
                glPopMatrix()

            glPopMatrix()

            # pickup check (no sqrt) - MUCH BIGGER pickup range for easier collection
            if dist2(px, py, c['x'], c['y']) < sqr(35.0):  # Much larger pickup range
                c['got'] = True
                picked += 1
    return 
def switch_clues():
    """Randomly move unclamed clues to a new room."""
    available_rooms = []
    for i, y in enumerate(ROOM_Y):
        available_rooms.append(('left', i))
        available_rooms.append(('right', i))
    for c in clues:
        if not c['got']:
            # Pick a random room different from current
            while True:
                side, idx = random.choice(available_rooms)
                if (side == 'left' and c['x'] != LEFT_X) or (side == 'right' and c['x'] != RIGHT_X):
                    break
            if side == 'left':
                c['x'] = LEFT_X
                c['y'] = ROOM_Y[idx]
            else:
                c['x'] = RIGHT_X
                c['y'] = ROOM_Y[idx]

# ---------- Clues ----------
def collected_clues():
    return sum(1 for c in clues if c['got'])
global clue_switch_timer
new_pickups = draw_clues_and_pickup.__wrapped_pickups if hasattr(draw_clues_and_pickup, '__wrapped_pickups') else 0
clue_switch_timer -= dt
if clue_switch_timer <= 0.0:
        switch_clues()
        clue_switch_timer = CLUE_SWITCH_BASE / clue_switch_rate