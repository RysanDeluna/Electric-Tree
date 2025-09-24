import pygame as pg
import math
 
class Game:
    running = True
    clock = pg.time.Clock()

    def __init__(self, res=(640,640), fps=10):
        self.resolution = res
        self.fps = fps
        self.screen = pg.display.set_mode(self.resolution)

        pg.init()

    def kill():
        pg.quit()

    def handle_input(self, *args, **kwargs):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        self.screen.fill((0,0,0))

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) * .0001 * self.fps
            self.handle_input(dt)
            self.update(dt)
            self.render(dt)
        print("ENDED")
        self.kill

class Demo(Game):
    def __init__(self, res=(640, 640), fps=10, scale=5, wave_speed = 1):
        super().__init__((res[0]*scale, res[1]*scale), fps)
        self.res = res
        self.wave_speed = wave_speed
        self.t = .0
        self.scale = scale

    def handle_input(self, *args, **kwargs):
        super().handle_input(args, kwargs)
        for event in pg.event.get():
            pass

    def update(self, *args, **kwargs):
        dt = args[0]
        self.t += dt

        self.points = []
        for x in range(self.resolution[0]):
            y = math.ceil(math.sin(x*(1/4) + (self.t * self.wave_speed * 4)) 
                          * (0.8 * self.res[1]/2) + ((self.res[1]/2)-1))
            self.points.append((x,y))
    
        for i in range(len(self.points) -1): 
            x0,y0 = self.points[i]
            x1,y1 = self.points[i+1]
            if abs(y0 - y1) > 1:
                step = 1 if y0 < y1 else -1
                for y in range(y0, y1, step):
                    self.points.append((x0, y))
    
    def render(self, *args, **kwargs):
        super().render(args, kwargs)
        for point in self.points: 
            pg.draw.rect(
                self.screen, 
                (0,255,0), 
                (
                    point[0]*self.scale,
                    point[1]*self.scale,
                    self.scale,
                    self.scale
                )
            )
        pg.display.flip()