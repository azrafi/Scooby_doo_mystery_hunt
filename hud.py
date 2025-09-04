
from Scooby_doo_mystery_hunt.shared import *


# ---------- HUD ----------
def draw_hud():
    glDisable(GL_LIGHTING)
    # Lives and clues
    x0, y0 = 10, WIN_H - 30
    draw_text(x0, y0, f"Lives: {lives}")
    draw_text(x0, y0 - 28, f"Clues: {collected_clues()}/{TOTAL_CLUES}")
    draw_text(x0, y0 - 56, f"Difficulty: {DIFFICULTY.title()}")
    # Safety status
    if is_player_in_room():
        glColor3f(0.2, 1.0, 0.2)  # Green for safe
        draw_text(x0, y0 - 84, "STATUS: SAFE IN ROOM")
        glColor3f(1.0, 1.0, 1.0)  # Reset to white
    else:
        glColor3f(1.0, 0.3, 0.3)  # Red for danger
        draw_text(x0, y0 - 84, "STATUS: CORRIDOR (DANGER)")
        glColor3f(1.0, 1.0, 1.0)  # Reset to white

    # Boost status
    boost_str = "Ready" if boost_available() else ("Active" if scooby_active else f"CD: {scooby_cd_left:0.1f}s")
    draw_text(x0, y0 - 112, f"Boost: {boost_str}")

    # Instructions
    glColor3f(0.8, 0.8, 0.8)  # Gray for instructions
    draw_text(x0, y0 - 140, "WASD: Move  Arrows: Camera  1: TPS  2: FPS  U: Overhead  B: Boost  R: Restart")
    draw_text(x0, y0 - 168, "Enter rooms through doors for safety!")

    glColor3f(1.0, 1.0, 1.0)  # Reset to white

    # Monster name when revealed
    if m_name_revealed:
        draw_text(10, 20, f"Monster: {m_name}")

    # Recent achievements (show up to 3 most recently unlocked)
    unlocked_achievements = [name for name, data in achievements.items() if data['unlocked']]
    if unlocked_achievements:
        glColor3f(1.0, 1.0, 0.0)  # Yellow for achievements
        draw_text(x0, y0 - 196, f"Achievements: {len(unlocked_achievements)}/7")
        # Show last few unlocked
        for i, achievement_name in enumerate(unlocked_achievements[-3:]):
            achievement = achievements[achievement_name]
            draw_text(x0, y0 - 224 - i*20, f"✓ {achievement['name']}")
        glColor3f(1.0, 1.0, 1.0)  # Reset to white
    # ---------- GLUT glue ----------
def draw_text(x, y, text, font=None):
    """Draw text at screen coordinates using GLUT bitmap font"""
    if font is None:
        try:
            from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
            font = GLUT_BITMAP_HELVETICA_18
        except:
            # Fallback - disable text rendering if font unavailable
            return

    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top


    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    try:
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ord(ch))
    except:
        # Silently fail if font rendering doesn't work
        pass
