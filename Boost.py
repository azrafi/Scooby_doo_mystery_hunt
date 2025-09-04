
# ---------- Scooby (Boost) ----------
scooby_active = False
scooby_timer = 0.0
scooby_dur = 6.0
scooby_cd_left = 0.0
scooby_cd = 10.0

# Boost becomes available after 1 clue (since we only have 3 total now)
def boost_available():
    return collected_clues() >= 1 and scooby_cd_left <= 0.0 and not scooby_active
