from classes.Game import *

# ================ CONFIG ================
WIDTH, HEIGHT = 64, 64
SCALE = 5
FPS = 10
ONDA_P_SEG = 1

# ================= MAIN ====================

if __name__ == "__main__":
    game = Demo((WIDTH,HEIGHT), FPS, SCALE, ONDA_P_SEG)
    game.run()