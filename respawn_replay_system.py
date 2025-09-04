from Scooby_doo_mystery_hunt.shared import *


def reset_game():
    global px, py, pdir, lives, invuln_t, game_won
    global mx, my, m_visible, m_spawn_timer, m_visible_timer
    global m_name, m_name_revealed
    global scooby_active, scooby_timer, scooby_cd_left
    global TPS_DIST, TPS_HEIGHT
    # DO NOT reset DIFFICULTY, monster_speed_mult, clue_switch_rate here!

    for c in clues:
        c['got'] = False
    px, py = 0.0, -HALL_LEN * 0.25
    pdir = 0.0
    lives = 3
    invuln_t = 0.0
    game_won = False
    m_visible = False
    m_spawn_timer = 1.0
    m_visible_timer = 0.0
    m_name_revealed = False
    m_name = "???"
    scooby_active = False
    scooby_cd_left = 0.0


    # Camera settings
    TPS_DIST = 250.0
    TPS_HEIGHT = 80.0
