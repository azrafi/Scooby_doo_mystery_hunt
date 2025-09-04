# ---------- Achievement System ----------
achievements = {
    'first_clue': {'unlocked': False, 'name': 'First Clue', 'desc': 'Found your first clue'},
    'speed_demon': {'unlocked': False, 'name': 'Speed Demon', 'desc': 'Used Scooby boost 5 times'},
    'survivor': {'unlocked': False, 'name': 'Survivor', 'desc': 'Survived 30 seconds without taking damage'},
    'trap_dodger': {'unlocked': False, 'name': 'Trap Dodger', 'desc': 'Avoided 3 traps in one game'},
    'mystery_solver': {'unlocked': False, 'name': 'Mystery Solver', 'desc': 'Solved the mystery (collected all clues)'},
    'room_hopper': {'unlocked': False, 'name': 'Room Hopper', 'desc': 'Visited all 6 rooms'},
    'close_call': {'unlocked': False, 'name': 'Close Call', 'desc': 'Escaped from monster when at 1 health'}
}

achievement_stats = {
    'boost_count': 0,
    'damage_free_time': 0.0,
    'traps_avoided': 0,
    'rooms_visited': set(),
    'close_calls': 0
}

def check_achievements():
    """Check and unlock achievements based on game state"""
    global achievement_stats

    # First clue
    if collected_clues() >= 1:
        achievements['first_clue']['unlocked'] = True

    # Speed demon - 5 boosts used
    if achievement_stats['boost_count'] >= 5:
        achievements['speed_demon']['unlocked'] = True

    # Survivor - 30 seconds without damage
    if achievement_stats['damage_free_time'] >= 30.0:
        achievements['survivor']['unlocked'] = True

    # Trap dodger - avoided 3 traps
    if achievement_stats['traps_avoided'] >= 3:
        achievements['trap_dodger']['unlocked'] = True

    # Mystery solver - all clues collected
    if collected_clues() >= TOTAL_CLUES:
        achievements['mystery_solver']['unlocked'] = True

    # Room hopper - visited all rooms
    if len(achievement_stats['rooms_visited']) >= 6:
        achievements['room_hopper']['unlocked'] = True

    # Close call - escaped at 1 health
    if achievement_stats['close_calls'] >= 1:
        achievements['close_call']['unlocked'] = True

def update_achievement_stats(dt):
    """Update achievement tracking statistics"""
    global achievement_stats

    # Track damage-free time
    if invuln_t <= 0:  # Not recently damaged
        achievement_stats['damage_free_time'] += dt
    else:
        achievement_stats['damage_free_time'] = 0.0  # Reset on damage

    # Track room visits
    current_room = get_current_room()
    if current_room is not None:
        achievement_stats['rooms_visited'].add(current_room)

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
