from Scooby_doo_mystery_hunt.shared import *



def draw_scooby():
    # More detailed Scooby with legs and collar
    glPushMatrix()

    # Body
    glColor3f(0.6, 0.35, 0.15)  # brown body
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(1.6, 1.0, 0.8)
    draw_sphere(12)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(16, 0, 34)
    draw_sphere(8)
    glPopMatrix()

    # Ears
    glColor3f(0.5, 0.25, 0.1)  # darker brown
    for dy in (-6, 6):
        glPushMatrix()
        glTranslatef(20, dy, 38)
        glRotatef(45, 1, 0, 0)
        glScalef(0.6, 1.5, 0.4)
        glutSolidCube(6)
        glPopMatrix()

    # Collar
    glColor3f(0.0, 0.4, 0.8)  # blue collar
    glPushMatrix()
    glTranslatef(12, 0, 32)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(5, 5, 8)
    glPopMatrix()

    # Collar tag
    glColor3f(0.8, 0.8, 0.0)  # yellow tag
    glPushMatrix()
    glTranslatef(12, 0, 28)
    glutSolidCube(3)
    glPopMatrix()

    # Legs
    glColor3f(0.6, 0.35, 0.15)  # brown legs
    for dx, dy in [(-8, 8), (8, 8), (-8, -8), (8, -8)]:
        glPushMatrix()
        glTranslatef(dx, dy, 10)
        glRotatef(90, 1, 0, 0)
        draw_cylinder(3, 3, 12)
        glPopMatrix()

        # Paws
        glColor3f(0.1, 0.1, 0.1)  # black paws
        glPushMatrix()
        glTranslatef(dx, dy, 0)
        draw_sphere(4)
        glPopMatrix()
        glColor3f(0.6, 0.35, 0.15)  # reset to brown

    # Tail
    glPushMatrix()
    glTranslatef(-16, 0, 30)
    glRotatef(35, 0, 1, 0)
    draw_cylinder(2, 1, 16)
    glPopMatrix()

    glPopMatrix()
