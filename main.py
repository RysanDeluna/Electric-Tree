import pygame as pg
import math, time


# ================ CONFIG ================
WIDTH, HEIGHT = 128, 128
SCALE = 5
FPS = 10
ONDA_P_SEG = 0.5

# ================= INIT =================
pg.init()
clock = pg.time.Clock()
t = 0.0
screen = pg.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
running = True

# ================= LOOP =================
while running:
    dt = clock.tick(FPS) * .0001 * FPS
    t = pg.time.get_ticks() * .0001

    # ================ EVENTOS ================
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # ================ DESENHO ================
    screen.fill((0,0,0))

    points = []
    for x in range(WIDTH):
        y = math.ceil(math.sin(x*0.25 + (t * ONDA_P_SEG * 60)) * (0.8 * HEIGHT/2) + ((HEIGHT/2)-1))
        points.append((x,y))
    
    for i in range(len(points) -1): 
        x0,y0 = points[i]
        x1,y1 = points[i+1]
        if abs(y0 - y1) > 1:
            step = 1 if y0 < y1 else -1
            for y in range(y0, y1, step):
                points.append((x0, y))
    
    for point in points: pg.draw.rect(screen, (0,255,0), (point[0]*SCALE, point[1]*SCALE, SCALE, SCALE))
            
    # ================ UPDATE ================
    pg.display.flip()

pg.quit()
