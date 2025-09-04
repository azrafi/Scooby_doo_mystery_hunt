from shared import *
from Scooby_doo_mystery_hunt.shared import *


def get_current_room():
    """Get which room player is currently in (0-5) or None if in corridor"""
    for i, y in enumerate(ROOM_Y):
        # Check left rooms
        if (abs(px - LEFT_X) < ROOM_SIZE/2 and abs(py - y) < ROOM_SIZE/2):
            return i
        # Check right rooms
        if (abs(px - RIGHT_X) < ROOM_SIZE/2 and abs(py - y) < ROOM_SIZE/2):
            return i + 3
    return None

def is_player_in_room():
    """Check if player is safely inside any room (not just at the door)"""
    half = ROOM_SIZE * 0.5
    door_threshold = 25  # Distance from door where player is still vulnerable

    for y in ROOM_Y:
        # Left room
        if (LEFT_X - half <= px <= LEFT_X + half) and (y - half <= py <= y + half):
            # Check if player is deep inside room (away from door)
            if py < y + half - door_threshold:
                return True

        # Right room
        if (RIGHT_X - half <= px <= RIGHT_X + half) and (y - half <= py <= y + half):
            # Check if player is deep inside room (away from door)
            if py < y + half - door_threshold:
                return True

    return False
