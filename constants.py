"""
Global constants
"""

# --------------- Colors -----------------

BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255)
GREY     = ( 128, 128, 128)
BLUE     = (   0,   0, 255)

# ---------- Screen Dimensions -----------

SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 900

# ---------- Player Walk Frames ----------

PLAYER_ONE = [(2, 4, 31, 43),
              (39, 4, 30, 43),
              (73, 4, 35, 42),
              (0, 53, 35, 43),
              (36, 54, 36, 42),
              (73, 55, 35, 42),
              (111, 55, 31, 43)
]

PLAYER_TWO = [(2, 4, 29, 42),
              (38, 4, 28, 42),
              (74, 4, 28, 41),
              (0, 51, 33, 41),
              (36, 51, 33, 42),
              (71, 52, 33, 41),
              (108, 52, 29, 43)
]

# ------------- Player Attributes --------------

PLAYER_ONE_AT = {'spritesheet':'p1_spritesheet.png',
                 'frozen_spritesheet':'p1_frozen_spritesheet.png',
                 'walk_images':PLAYER_ONE,
                 'direction':'R',
                 'name':'p1'
}

PLAYER_TWO_AT = {'spritesheet':'p2_spritesheet.png',
                 'frozen_spritesheet':'p2_frozen_spritesheet.png',
                 'walk_images':PLAYER_TWO,
                 'direction':'L',
                 'name':'p2'
}

# -------------- Enemy Walk Frames -------------

WALKER = [(5, 1, 66, 92),
          (79, 0, 66, 92),
          (146, 0, 72, 92),
          (0, 98, 71, 92),
          (73, 100, 71, 92),
          (146, 101, 70, 92),
          (222, 102, 67,93)
]

# -------------- Enemy Attributes ---------------

WALKER_AT = {'spritesheet':'walker1.png',
             'walk_images':WALKER,
             'change_x':4,
             'change_y':0,
             'health':2
}

COLOR_VARIANT = [ ('walker1.png'),
                  ('walker2.png'),
                  ('walker3.png'),
                  ('walker4.png'),
                  ('walker5.png'),
                  ('walker6.png'),
                  ('walker7.png')
]

# ------- Scoreboard Sprite Sheet Data -------

NUMBERS = [ (8, 78, 30, 30),
            (48, 79, 13, 29),
            (73, 78, 20, 31),
            (106, 78, 20, 30),
            (139, 78, 21, 30),
            (172, 78, 16, 30),
            (203, 78, 18, 30),
            (234, 78, 18, 31),
            (264, 78, 21, 31),
            (297, 78, 21, 30),
]
