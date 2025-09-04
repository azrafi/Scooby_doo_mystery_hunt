from Scooby_doo_mystery_hunt.shared import *


def update(dt):

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
