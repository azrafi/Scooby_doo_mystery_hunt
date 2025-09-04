from shared import *

def draw_scooby():
    """Draw Scooby Doo character"""
    # Scooby's body - more dog-like than Shaggy
    glPushMatrix()

    # Main body (larger, more rounded)
    glColor3f(0.6, 0.4, 0.2)  # Brown fur
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(1.8, 1.2, 1.0)
    draw_sphere(12)
    glPopMatrix()

    # Head (dog-like)
    glColor3f(0.7, 0.5, 0.3)  # Lighter brown for head
    glPushMatrix()
    glTranslatef(0, -15, 35)
    glScalef(1.2, 1.4, 1.0)
    draw_sphere(10)
    glPopMatrix()

    # Snout
    glColor3f(0.5, 0.3, 0.1)  # Darker brown
    glPushMatrix()
    glTranslatef(0, -22, 33)
    glScalef(0.8, 1.0, 0.6)
    draw_sphere(6)
    glPopMatrix()

    # Ears (floppy dog ears)
    glColor3f(0.5, 0.3, 0.2)
    for ear_x in [-8, 8]:
        glPushMatrix()
        glTranslatef(ear_x, -10, 42)
        glRotatef(ear_x * 3, 0, 0, 1)  # Slight rotation
        glScalef(0.6, 1.2, 2.0)
        draw_sphere(5)
        glPopMatrix()

    # Eyes
    glColor3f(0, 0, 0)
    for eye_x in [-4, 4]:
        glPushMatrix()
        glTranslatef(eye_x, -20, 38)
        draw_sphere(1.5)
        glPopMatrix()

    # Nose
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, -25, 33)
    draw_sphere(2)
    glPopMatrix()

    # Collar (Scooby's signature blue collar)
    glColor3f(0.0, 0.3, 0.8)  # Blue collar
    glPushMatrix()
    glTranslatef(0, -8, 28)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(8, 8, 4)
    glPopMatrix()

    # Collar tag
    glColor3f(0.8, 0.8, 0.2)  # Gold tag
    glPushMatrix()
    glTranslatef(0, -12, 28)
    draw_sphere(2)
    glPopMatrix()

    # Legs (four legs, dog-like)
    glColor3f(0.6, 0.4, 0.2)
    leg_positions = [(-6, -8), (6, -8), (-6, 8), (6, 8)]
    for leg_x, leg_y in leg_positions:
        glPushMatrix()
        glTranslatef(leg_x, leg_y, 8)
        glScalef(0.6, 0.6, 1.2)
        draw_sphere(4)
        glPopMatrix()

    # Paws
    glColor3f(0.4, 0.2, 0.1)
    for leg_x, leg_y in leg_positions:
        glPushMatrix()
        glTranslatef(leg_x, leg_y, 2)
        draw_sphere(3)
        glPopMatrix()

    # Tail (wagging)
    glColor3f(0.6, 0.4, 0.2)
    tail_wag = math.sin(glutGet(GLUT_ELAPSED_TIME) / 200.0) * 20
    glPushMatrix()
    glTranslatef(0, 12, 25)
    glRotatef(tail_wag, 0, 0, 1)
    glScalef(0.5, 1.5, 0.8)
    draw_sphere(5)
    glPopMatrix()

    glPopMatrix()

def draw_clues_and_pickup():
    """Draw clues and handle pickup when player gets close"""
    pickup_dist = 30.0
    
    for i, clue in enumerate(clues):
        if clue['got']:
            continue
            
        cx, cy = clue['x'], clue['y']
        
        # Check if player is close enough to pick up
        dist = math.sqrt((px - cx)**2 + (py - cy)**2)
        if dist < pickup_dist:
            clue['got'] = True
            print(f"Clue {i+1} collected! Total: {collected_clues()}/{TOTAL_CLUES}")
            continue
        
        # Draw the clue with animation
        t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        bob_height = 20 + 8 * math.sin(t * 2 + i)
        glow = 0.7 + 0.3 * math.sin(t * 3 + i)
        
        glPushMatrix()
        glTranslatef(cx, cy, bob_height)
        
        # Outer glow
        glColor3f(1.0 * glow, 1.0 * glow, 0.2)
        draw_sphere(12)
        
        # Inner core
        glColor3f(1.0, 0.8, 0.0)
        draw_sphere(8)
        
        # Center sparkle
        glColor3f(1.0, 1.0, 1.0)
        draw_sphere(4)
        
        glPopMatrix()

def collected_clues():
    """Return number of clues collected"""
    return sum(1 for c in clues if c['got'])

def switch_clues():
    """Periodically move clues to new locations"""
    uncollected = [i for i, c in enumerate(clues) if not c['got']]
    
    for idx in uncollected:
        # Randomly relocate uncollected clues
        if random.random() < 0.3:  # 30% chance to move each clue
            room_idx = random.randint(0, 2)
            side = random.choice([LEFT_X, RIGHT_X])
            
            clues[idx]['x'] = side + random.uniform(-ROOM_SIZE*0.3, ROOM_SIZE*0.3)
            clues[idx]['y'] = ROOM_Y[room_idx] + random.uniform(-ROOM_SIZE*0.3, ROOM_SIZE*0.3)

def check_achievements():
    """Check and unlock achievements based on current game state"""
    global achievements, achievement_times
    
    # Achievement: First clue
    if not achievements['first_clue'] and collected_clues() >= 1:
        achievements['first_clue'] = True
        achievement_times['first_clue'] = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        print("Achievement Unlocked: First Clue!")
    
    # Achievement: All clues
    if not achievements['all_clues'] and collected_clues() >= TOTAL_CLUES:
        achievements['all_clues'] = True
        achievement_times['all_clues'] = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        print("Achievement Unlocked: Mystery Solver!")
    
    # Achievement: Survivor (no damage taken)
    if not achievements['survivor'] and exploration_stats['damage_taken'] == 0 and collected_clues() >= 2:
        achievements['survivor'] = True
        achievement_times['survivor'] = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        print("Achievement Unlocked: Survivor!")
    
    # Achievement: Speedrun (all clues in under 2 minutes)
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    if not achievements['speedrun'] and collected_clues() >= TOTAL_CLUES and (current_time - exploration_stats['start_time']) < 120:
        achievements['speedrun'] = True
        achievement_times['speedrun'] = current_time
        print("Achievement Unlocked: Speed Demon!")
    
    # Achievement: Explorer (visit all rooms)
    if not achievements['explorer'] and len(exploration_stats['rooms_visited']) >= 6:
        achievements['explorer'] = True
        achievement_times['explorer'] = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        print("Achievement Unlocked: Explorer!")
    
    # Achievement: Pro Gamer (hard difficulty + all clues + no deaths)
    if not achievements['pro_gamer'] and DIFFICULTY == 'hard' and collected_clues() >= TOTAL_CLUES and lives == 3:
        achievements['pro_gamer'] = True
        achievement_times['pro_gamer'] = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        print("Achievement Unlocked: Pro Gamer!")

def update_achievement_stats(dt):
    """Update statistics for achievement tracking"""
    global exploration_stats
    
    # Track room visits
    current_room = get_current_room()
    if current_room is not None:
        exploration_stats['rooms_visited'].add(current_room)

def draw_hud():
    """Draw heads-up display with game information"""
    # Switch to 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WIN_W, WIN_H, 0, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    # Background panel
    glColor3f(0.0, 0.0, 0.0)  # Black background
    glBegin(GL_QUADS)
    glVertex2f(10, 10)
    glVertex2f(300, 10)
    glVertex2f(300, 120)
    glVertex2f(10, 120)
    glEnd()
    
    # Border
    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(10, 10)
    glVertex2f(300, 10)
    glVertex2f(300, 120)
    glVertex2f(10, 120)
    glEnd()
    
    # Text information
    glColor3f(1.0, 1.0, 1.0)  # White text
    
    # Lives
    draw_text(20, 30, f"Lives: {lives}")
    
    # Clues
    draw_text(20, 50, f"Clues: {collected_clues()}/{TOTAL_CLUES}")
    
    # Difficulty
    draw_text(20, 70, f"Difficulty: {DIFFICULTY.title()}")
    
    # Boost status
    if scooby_cd_left > 0:
        draw_text(20, 90, f"Boost CD: {scooby_cd_left:.1f}s")
    elif boost_available():
        draw_text(20, 90, "Boost: READY (Space)")
    
    # Monster identity (if revealed)
    if m_name_revealed:
        draw_text(20, 110, f"Monster: {m_name}")
    
    # Game status
    if game_won:
        glColor3f(0.0, 1.0, 0.0)  # Green for win
        draw_text(WIN_W//2 - 60, WIN_H//2, "YOU WON!")
        draw_text(WIN_W//2 - 80, WIN_H//2 + 20, "Press R to restart")
    elif lives <= 0:
        glColor3f(1.0, 0.0, 0.0)  # Red for game over
        draw_text(WIN_W//2 - 60, WIN_H//2, "GAME OVER")
        draw_text(WIN_W//2 - 80, WIN_H//2 + 20, "Press R to restart")
    
    # Controls help
    glColor3f(0.8, 0.8, 0.8)
    help_y = WIN_H - 100
    draw_text(WIN_W - 200, help_y, "Controls:")
    draw_text(WIN_W - 200, help_y + 20, "WASD - Move")
    draw_text(WIN_W - 200, help_y + 40, "Q/E - Turn")
    draw_text(WIN_W - 200, help_y + 60, "Space - Boost")
    draw_text(WIN_W - 200, help_y + 80, "C - Camera")
    
    # Achievement notifications (show recent unlocks)
    achievement_y = WIN_H - 200
    unlocked_achievements = [name for name, unlocked in achievements.items() if unlocked]
    if unlocked_achievements:
        glColor3f(1.0, 1.0, 0.0)  # Yellow for achievements
        draw_text(WIN_W - 250, achievement_y, f"Achievements: {len(unlocked_achievements)}/6")
        
        # Show last few unlocked
        for i, achievement_name in enumerate(unlocked_achievements[-3:]):
            draw_text(WIN_W - 250, achievement_y + 20 + i*20, f"✓ {achievement_name.replace('_', ' ').title()}")
    
    # Restore 3D rendering
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text(x, y, text, font=None):
    """Draw 2D text at screen coordinates"""
    if font is None:
        font = GLUT_BITMAP_HELVETICA_12
    
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

def boost_available():
    """Check if boost is available (not on cooldown)"""
    return scooby_cd_left <= 0
