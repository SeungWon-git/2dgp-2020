import random
from pico2d import *

RES_DIR = '../res'

class Grass:
    def __init__(self):
        self.image = load_image(RES_DIR + '/grass.png')
    def draw(self):
        self.image.draw(400, 30)
    def update(self):
        pass

class Ball:
    balls = []
    def __init__(self, pos, delta):
        self.image = load_image(RES_DIR + '/ball21x21.png')
        self.pos = pos
        self.delta = delta
    def draw(self):
        self.image.draw(*self.pos)
    def update(self):
        x,y = self.pos
        dx,dy = self.delta
        self.pos = x+dx, y+dy
        gravity = 0.05
        self.delta = dx, dy - gravity

    
class Boy:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT): ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):  ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):    ( 0,  1),
        (SDL_KEYUP, SDLK_LEFT):    ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):   (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):    ( 0,  1),
        (SDL_KEYUP, SDLK_UP):      ( 0, -1),
    }
    KEYDOWN_SPACE = (SDL_KEYDOWN, SDLK_SPACE)

    #constructor
    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.delta = 0, 0
        self.fidx = random.randint(0, 7)
        self.image = load_image(RES_DIR + '/animation_sheet.png')
        self.action = 3

    def draw(self):
        sx = self.fidx * 100
        sy = self.action * 100
        self.image.clip_draw(sx, sy, 100, 100, *self.pos)

    def update(self):
        x,y = self.pos
        dx,dy = self.delta
        self.pos = x+dx, y+dy
        self.fidx = (self.fidx + 1) % 8

    def ballDelta(self):
        dxs = [ -3, 3, -1, 1 ]
        mag = dxs[self.action]
        dx,dy = self.delta
        return mag+dx, 2+dy

    def fire(self):
        ball = Ball(self.pos, self.ballDelta())
        Ball.balls.append(ball)
        print('Ball count = %d' % len(Ball.balls))

    def updateDelta(self, ddx, ddy):
        dx,dy = self.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.action = \
                0 if dx < 0 else \
                1 if dx > 0 else \
                2 if ddx > 0 else 3
        self.delta = dx, dy

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Boy.KEY_MAP:
            self.updateDelta(*Boy.KEY_MAP[pair])
        elif pair == Boy.KEYDOWN_SPACE:
            self.fire()

if __name__ == "__main__":
	print("Running test code ^_^")
