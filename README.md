
**Scooby_doo_mystery_hunt**

  Step into the haunted halls with Shaggy and Scooby in this Python OpenGL adventure! Explore eerie corridors and six mysterious rooms, uncover glowing clues, and        survive the monster’s chase as the difficulty rises with every discovery. Summon Scooby in Boost Mode to distract the creature and buy precious time, all while         managing health, strategy, and courage. Built entirely with PyOpenGL, this game blends classic Scooby-Doo suspense with arcade-inspired 3D visuals for a thrilling      mystery hunt!

**Features**
  
  **Haunted Hallway + Six-Room Layout**
  
  A single long corridor with 3 rooms per side, each room a simple 3D box with a doorway that faces the hall—perfect for quick exploration loops.

  **Glowing Clue Orbs (Pulsing)**

  Three collectible, pulsating orbs (one per room) that gently glow to guide players without extra assets or textures.

**Escalating Monster Pressure**

  A rarely-seen monster stalks Shaggy from the start; each collected clue increases both its speed and appearance duration, tightening the loop over time.

**Three Lives, Contact Damage**

  Shaggy survives three hits; contact briefly despawns the monster and grants a short invulnerability window—clean, readable fail states (and fast retries).

**Boost Mode: Scooby Distraction**

  After two clues, tap B to summon Scooby. The monster retargets and slows while Scooby “distracts,” buying space for clutch escapes.

**Multiple Camera Modes**

  Swap instantly between Third-Person, First-Person, and Top-Down for different reads on the space and threat direction. (Keys 1/2/3.)

**Door Arches with Idle Motion**

  Room door arches subtly oscillate (rotate) to hint interactivity and add life to the otherwise minimalistic environment.

**Fixed-Function Lighting**

  Simple directional lighting + color materials provide readable depth cues while staying within GL/GLU/GLUT constraints (no textures).

**Orthographic HUD Overlays**

  A clean heads-up display shows Lives, Clues (collected/total), Boost status, and—upon success—the Monster’s name, using the same ortho text overlay technique as   your scaffold.

**Readable Movement Model**

  W/S to move, A/D to rotate (plus Q/E strafe), with gentle acceleration-free control—ideal for tight corridors and room entries.

**Collision-Safe Corridor & Rooms**

  Player motion is clamped to the corridor or inside a room’s AABB; doorlines are passable, preventing accidental wall-sticking and out-of-bounds glitches.

**Smart(er) Chasing**

  The monster uses a simple steer-toward-target behavior; during Boost, it diverts to a Scooby proxy and moves slower—a crisp, tactical window.

**Adaptive Spawn Cadence**

  “Rarity” logic makes early encounters infrequent, then more present as clues accumulate—maintaining pacing without true randomness.

**Run Reset for Quick Iteration**

  Press R to reset: lives, boost, name reveal, and clue states return to baseline so playtesting is snappy. (Great for tuning.)

**Name Reveal Win Condition**

  Collect all six clues and the HUD reveals the monster’s identity—a lightweight narrative payoff that fits the import limits.

**Performance-Friendly Primitives**

  All actors (Shaggy, Scooby, monster, doors) are built from cubes/spheres/cylinders—fast to render, easy to tweak, fully fixed-function.

**Top-Down Recon Mode**

  A tactical camera that pops the whole hallway and adjacent rooms into view—great for planning routes when the monster pressure rises.

**Minimal Dependencies, Maximum Portability**

  Runs with OpenGL.GL / GLUT / GLU only; no textures, models, audio, or physics engines—just what your allowed file uses.
﻿
rahul06_
 
