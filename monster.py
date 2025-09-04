def draw_monster():
    # Monster transformation stages - ALL STAGES AS TOWERING GIANTS
    clue_count = collected_clues()

    # Stage 1: Shadow Giant (0 clues) - GIANT SIZE
    if clue_count == 0:
        glPushMatrix()
        glColor3f(0.2, 0.2, 0.2)  # dark shadow
        glTranslatef(0, 0, 80)  # Much taller - giant height

        # Giant head
        draw_sphere(35)  # Massive head

        # Giant torso
        glTranslatef(0, 0, -50)
        glScalef(1.8, 1.8, 3.0)  # Wide and tall torso
        glutSolidCube(40)

        # Giant arms
        glLoadIdentity()
        glTranslatef(mx, my, 60)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 60, 0, 0)  # Wide arm span
            glColor3f(0.15, 0.15, 0.15)  # darker arms
            glScalef(1.2, 1.2, 4.0)  # Long giant arms
            glutSolidCube(25)
            glPopMatrix()

        # Giant legs
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 25, 0, -80)  # Deep leg position
            glColor3f(0.1, 0.1, 0.1)  # dark legs
            glScalef(1.5, 1.5, 4.0)  # Massive legs
            glutSolidCube(30)
            glPopMatrix()
        glPopMatrix()

    # Stage 2: Purple Ghost Giant (1 clue) - GIANT SIZE
    elif clue_count == 1:
        glPushMatrix()
        glColor3f(0.4, 0.1, 0.6)  # purple
        glTranslatef(0, 0, 100)  # Even taller giant

        # Giant ghost head
        draw_sphere(45)  # Massive ghost head

        # Giant ghost body
        glTranslatef(0, 0, -60)
        glColor3f(0.5, 0.2, 0.7)
        glScalef(2.2, 2.2, 3.5)  # Huge ghost body
        glutSolidCube(45)

        # Massive ghostly trail
        glLoadIdentity()
        glTranslatef(mx, my, 20)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.3, 0.1, 0.5)
        draw_cylinder(40, 20, 80)  # Enormous trail
        glPopMatrix()

    # Stage 3: Menacing Phantom Giant (2 clues) - GIANT SIZE
    elif clue_count == 2:
        glPushMatrix()
        glColor3f(0.4, 0.1, 0.6)  # darker purple
        glTranslatef(0, 0, 120)  # Towering height

        # Giant head with glowing effect
        pulse = 1.0 + 0.3 * math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.003)
        glScalef(pulse, pulse, pulse)
        draw_sphere(50)  # Massive pulsing head

        # Giant middle body
        glScalef(1.0/pulse, 1.0/pulse, 1.0/pulse)  # reset scale
        glTranslatef(0, 0, -70)
        glColor3f(0.5, 0.2, 0.7)
        glScalef(2.5, 2.5, 4.0)  # Enormous body
        glutSolidCube(50)

        # Giant arms with threatening pose
        glLoadIdentity()
        glTranslatef(mx, my, 80)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 80, 0, 0)  # Wide threatening arm span
            glRotatef(side * 20, 0, 0, 1)  # Angled threatening pose
            glColor3f(0.3, 0.1, 0.5)
            glScalef(1.5, 1.5, 5.0)  # Long menacing arms
            glutSolidCube(30)
            glPopMatrix()

        # Massive ghostly trail
        glTranslatef(0, 0, -100)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.2, 0.05, 0.4)
        draw_cylinder(50, 25, 100)  # Enormous swirling trail
        glPopMatrix()

    # Stage 4: Revealed Giant Villain - Old Man Jenkins (3+ clues) - GIANT SIZE
    else:
        glPushMatrix()
        # Giant Human Villain - Old Man Jenkins revealed as GIANT
        glColor3f(0.8, 0.7, 0.6)  # human skin tone
        glTranslatef(0, 0, 140)  # Towering giant height

        # Giant head - more human proportions but massive
        draw_sphere(40)  # Enormous head

        # Giant torso
        glTranslatef(0, 0, -80)  # Much bigger body spacing
        glColor3f(0.3, 0.3, 0.8)  # blue clothing
        glScalef(3.0, 2.5, 5.0)  # Massive giant body
        glutSolidCube(35)  # Huge cube

        # Giant arms - menacing pose
        glLoadIdentity()
        glTranslatef(mx, my, 100)  # Very high position for giant
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 70, 0, 0)  # Very wide giant arm span
            glRotatef(side * 15, 0, 0, 1)  # Slight angle for menacing look
            glColor3f(0.8, 0.7, 0.6)  # skin
            glScalef(2.0, 2.0, 6.0)  # Massive giant arms
            glutSolidCube(25)  # Huge arm cubes
            glPopMatrix()

        # Giant legs
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 35, 0, -120)  # Much wider stance, deeper position
            glColor3f(0.2, 0.2, 0.2)  # dark pants
            glScalef(2.5, 2.5, 6.0)  # Enormous giant legs
            glutSolidCube(30)  # Massive leg cubes
            glPopMatrix()

        # Giant hands/fists for extra intimidation
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 90, 0, 60)  # At end of arms
            glColor3f(0.7, 0.6, 0.5)  # slightly darker skin for hands
            draw_sphere(15)  # Big threatening fists
            glPopMatrix()
        glPopMatrix()

    # Giant eyes - different colors and sizes based on stage
    if clue_count < 3:
        glColor3f(1.0, 0.0, 0.0)  # red glowing eyes
        eye_size = 8  # Bigger glowing eyes for giants
        eye_height = 80 + (clue_count * 20)  # Higher for each stage
        eye_spacing = 25  # Wider spacing for giant heads
    else:
        glColor3f(0.8, 0.8, 1.0)  # normal human eyes
        eye_size = 6  # Still big for giant human
        eye_height = 140  # At giant head level
        eye_spacing = 30  # Wide spacing for giant human head

    for dx in (-eye_spacing, eye_spacing):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(mx + dx, my, eye_height)
        draw_sphere(eye_size)
        glPopMatrix()
