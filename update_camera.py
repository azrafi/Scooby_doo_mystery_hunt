from Scooby_doo_mystery_hunt.shared import *
from immersive_room_system import*
from achievements import*

def update_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, ASPECT, 0.1, 5000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    rad = math.radians(pdir)
    if camera_mode == CAM_TPS:
        # Look at the character from behind and above like the image
        tx, ty, tz = px, py, 40.0  # Look at player

        # --- Clamp camera distance if player is in a room ---
        cam_dist = TPS_DIST
        cam_height = TPS_HEIGHT
        room_idx = get_current_room()
        if room_idx is not None:
            # Get room center
            if room_idx < 3:
                room_cx = LEFT_X
                room_cy = ROOM_Y[room_idx]
            else:
                room_cx = RIGHT_X
                room_cy = ROOM_Y[room_idx - 3]
            room_half = ROOM_SIZE * 0.5
            # Compute max distance from player to wall in camera direction
            dx = -math.sin(rad)
            dy = -math.cos(rad)
            # Find intersection with room bounds
            max_dist = TPS_DIST
            for sign in [-1, 1]:
                # X wall
                if dx != 0:
                    wx = room_cx + sign * room_half
                    t = (wx - px) / dx
                    if t > 0:
                        wy = py + t * dy
                        if room_cy - room_half <= wy <= room_cy + room_half:
                            max_dist = min(max_dist, t)
                # Y wall
                if dy != 0:
                    wy = room_cy + sign * room_half
                    t = (wy - py) / dy
                    if t > 0:
                        wx = px + t * dx
                        if room_cx - room_half <= wx <= room_cx + room_half:
                            max_dist = min(max_dist, t)
            # Pull camera in if needed
            cam_dist = min(TPS_DIST, max_dist - 10.0)  # 10 units padding from wall
            cam_dist = max(40.0, cam_dist)  # Don't get too close

        cx = px - math.sin(rad) * cam_dist
        cy = py - math.cos(rad) * cam_dist
        cz = cam_height
        gluLookAt(cx, cy, cz, tx, ty, tz, 0, 0, 1)
    elif camera_mode == third_person_mode:
        # Birdview: camera orbits at set height and angle
        board_cx, board_cy = 0.0, 0.0  # Center of board
        orbit_radius = 800.0           # Distance from center
        rad_angle = math.radians(third_person_angle)
        cx = board_cx + math.cos(rad_angle) * orbit_radius
        cy = board_cy + math.sin(rad_angle) * orbit_radius
        cz = third_person_height
        tx, ty, tz = board_cx, board_cy, 0.0  # Look at center of board
        gluLookAt(cx, cy, cz, tx, ty, tz, 0, 0, 1)
    else:  # FPS camera
        # Place camera just in front of and above player's head
        cam_offset = 18.0  # forward from player center
        head_height = 70.0 # height of player's eyes
        cam_x = px + math.sin(rad) * cam_offset
        cam_y = py + math.cos(rad) * cam_offset
        cam_z = head_height
        # Look further ahead from camera position
        look_x = cam_x + math.sin(rad) * 40.0
        look_y = cam_y + math.cos(rad) * 40.0
        look_z = head_height
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)
