from Scooby_doo_mystery_hunt.shared import *
# from core_engine import *
# from Scooby_doo_mystery_hunt.environment import *
# from gameplay import *
from achievements import *
from player_movement_and_rotation import *
from input_handling import *
from respawn_replay_system import *
from Boost import*
from trapping_system import*
from immersive_room_system import*
from monster_and_detection import*
from monsterreveal import*
from hud import*
from scooby_npc import* 
from clue_mech import*
from update_camera import*
from multiple_room_layout import*

def update(dt):
    global invuln_t, m_spawn_timer, m_visible_timer, scooby_timer, scooby_active, scooby_cd_left, m_name, m_name_revealed, game_won
    if lives <= 0 or game_won:
        return
    update_player(dt)
    update_traps(dt)  # Add trap system update
    update_achievement_stats(dt)  # Track achievements
    # Clues
    global clue_switch_timer
    new_pickups = draw_clues_and_pickup.__wrapped_pickups if hasattr(draw_clues_and_pickup, '__wrapped_pickups') else 0
    clue_switch_timer -= dt
    if clue_switch_timer <= 0.0:
        switch_clues()
        clue_switch_timer = CLUE_SWITCH_BASE / clue_switch_rate
    # Monster spawning/logic
    try_spawn_monster(dt)
    update_monster(dt)
    # Collision
    check_player_hit()
    if invuln_t > 0.0: invuln_t -= dt
    # Scooby timers
    if scooby_active:
        scooby_timer -= dt
        if scooby_timer <= 0.0:
            scooby_active = False
    if scooby_cd_left > 0.0:
        scooby_cd_left -= dt
    # Reveal name when all clues collected
    if not m_name_revealed and collected_clues() >= TOTAL_CLUES:
        m_name_revealed = True
        m_name = "Old Man Jenkins"
        game_won = True  # Player wins when monster identity is revealed!

    # Check for achievements
    check_achievements()

def display():
    # compute dt
    global t_prev_frame
    import time
    t_now = time.time()
    if 't_prev_frame' not in globals():
        t_prev_frame = t_now
    dt = t_now - t_prev_frame
    t_prev_frame = t_now
    
    update(dt)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    update_camera()

    # Draw environment
    draw_floor_and_hall()
    draw_all_rooms()
    draw_house_decorations()

    # Draw traps
    draw_traps()

    # Draw clues
    draw_clues_and_pickup_wrapper()

    # Draw characters
    draw_shaggy()
    if scooby_active:
        draw_scooby()
    
    # Draw monster
    if m_visible:
        glPushMatrix()
        glTranslatef(mx, my, 0)
        draw_monster()
        glPopMatrix()

    # Draw HUD
    draw_hud()

    glutSwapBuffers()
    glutPostRedisplay()

def draw_clues_and_pickup_wrapper():
    draw_clues_and_pickup()

def reshape(w, h):
    global WIN_W, WIN_H, ASPECT
    WIN_W, WIN_H = w, h
    ASPECT = WIN_W / float(WIN_H)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Scooby Doo: Mystery Hunt - OpenGL Prototype (Overhead 'U', No Roof)")

    init_gl()
    reset_game()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_down)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_down)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)

    glutMainLoop()

if __name__ == '__main__':
    main()
