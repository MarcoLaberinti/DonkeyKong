import game2d
from actor import Actor, Arena
from dk_elements import map_elements
from random import randint

class Jumper(Actor):

    def __init__(self, arena, x, y):
        self._w, self._h = 15, 16
        self._speed = 3
        self._max_speed = 3
        self._gravity =0.4
        self._x, self._y = x, y
        self._dx, self._dy = 0, 0
        self._jx = 197
        self._jy = 3
        self._fx = 158
        self._fy = 3
        self._gl = 1
        self._bl = False
        self._gr = 1
        self._br = False
        self._landed = False
        self._climbing = False
        self._ladder = None
        self._arena = arena
        self._GameOver = False
        arena.add(self)

    def move(self):

        if self._bl == True:
            if self._gl < 81:
                self._gl = self._gl + 10
            if self._gl == 81:
                self._gl = 1
                
        if self._br == True:
            if self._gr < 81:
                self._gr = self._gr + 10
            if self._gr == 81:
                self._gr = 1

        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._dx != 0 and self._climbing:
            self._climbing = False
            self._dy = 0
        if not (self._landed or self._climbing):
            self._dy += self._gravity
            self._dy = min(self._dy, self._max_speed)

        self._landed = False

        if self._ladder != None:
            bx, by, bw, bh = self.rect()  # jumper's pos
            wx, wy, ww, wh = self._ladder.rect() # ladder's pos
            if not (wy <= by + bh <= wy + wh and wx < bx + bw // 2 < wx + ww):
                if self._climbing:
                    self._y -= self._dy
                else:
                    self._ladder = None

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w

    def jump(self):
        if self._landed:
            self._dy = -self._max_speed
            self._landed = False
        
    def go_left(self):
        self._br = False
        self._bl = True
        self._jx = 94
        self._jy = 3
        self._fx = 136
        self._fy = 3
        self._dx = -self._speed
        
    def go_right(self):
        self._br = True
        self._bl = False
        self._jx = 197
        self._jy = 3
        self._fx = 158
        self._fy = 3
        self._dx = +self._speed

    def go_up(self):
        if self._ladder and (self._climbing or self._landed):
            self._climbing = True
            self._dy = -self._speed
        
    def go_down(self):
        if self._ladder and (self._climbing or self._landed):
            self._climbing = True
            self._dy = self._speed

    def stay(self):
        self._br = False
        self._bl = False
        self._dx = 0
        self._dy = 0

    def collide(self, other):
        bx, by, bw, bh = self.rect()  # jumper's pos
        wx, wy, ww, wh = other.rect() # other's pos
        if (isinstance(other, Ladder) and
            wy <= by + bh <= wy + wh and wx < bx + bw // 2 < wx + ww):
            self._ladder = other
            
        elif isinstance(other, Platform) and not self._climbing:
            if by + bh < wy + wh:
                self._y = wy - bh
                self._landed = True
            
        elif isinstance(other, Barrel) and wy <= by + bh // 2 <= wy + wh:
            self._arena.remove(self)
            self._GameOver = True
            
    
            
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._climbing:
            return 124, 24

        if self._landed == False:
            return self._jx, self._jy

        if self._br == True:
            if 1 <= self._gr < 21:
                return 158, 3
            if 21 <= self._gr < 41:
                return 176, 3
            if 41 <= self._gr < 61:
                return 197, 3
            if 61 <= self._gr < 81:
                return 176, 3
            
        if self._bl == True:
            if 1 <= self._gl < 21:
                return 136, 3
            if 21 <= self._gl < 41:
                return 115, 3
            if 41 <= self._gl < 61:
                return 94, 3
            if 61 <= self._gl < 81:
                return 115, 3
            
        if self._bl == False and self._br == False:
            return self._fx, self._fy

class Mario(Jumper):
    pass


class Barrel(Actor):

    def __init__(self, arena, x, y):
        self._gravity =0.4
        self._x, self._y = x, y
        self._dx, self._dy = 0, 0
        self._landed = False
        self._climbing = False
        self._w, self._h = 12, 10
        self._speed, self._max_speed = 2, 4
        self._left = False
        self._right = True
        self._ladder = None
        self._arena = arena
        self._l = 0
        self._r = 0
        self._c = 0
        self.going_right()
        arena.add(self)

    def collide(self, other):
        bx, by, bw, bh = self.rect()  # jumper's pos
        wx, wy, ww, wh = other.rect() # other's pos
        n=randint(0, 1)
        if (isinstance(other, Ladder) and
            wy <= by + bh <= wy + wh and wx < bx + bw // 2 < wx + ww):
            self._ladder = other
           
            if n == 1:
                Barrel.going_down()
                self._speed = -self._speed 
                
        elif isinstance(other, Platform) and not self._climbing:
            if by + bh < wy + wh:
                self._y = wy - bh
                self._landed = True
            
    def rect(self):
        return self._x, self._y, self._w, self._h
        
    def move(self):
        if self._c < 8:
            self._c = self._c + 1
        if self._c == 8:
            self._c = 0
        aw, ah = self._arena.size()
        if self._x + self._w >= aw:
            self._right = False
            self._left = True
            self.going_left()
        elif self._x <= 0:
            self._right = True
            self._left = False
            self.going_right()
            if self._y + self._h * 2 > ah:
                self._arena.remove(self)

        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._dx != 0 and self._climbing:
            self._climbing = False
            self._dy = 0
        if not (self._landed or self._climbing):
            self._dy += self._gravity
            self._dy = min(self._dy, self._max_speed)

        self._landed = False

        if self._ladder != None:
            bx, by, bw, bh = self.rect()  # jumper's pos
            wx, wy, ww, wh = self._ladder.rect() # ladder's pos
            if not (wy <= by + bh <= wy + wh and wx < bx + bw // 2 < wx + ww):
                if self._climbing:
                    self._y -= self._dy
                else:
                    self._ladder = None

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w

    def going_left(self):
        self._dx = -self._speed

    def going_right(self):
        self._dx = +self._speed

    def going_down(self):
        if self._ladder and (self._climbing or self._landed):
            self._dx = 0
            self._dy = self._speed

    def symbol(self):
        if self._right == True:
            if 0 <= self._c < 2:
                return 66, 258
            if 2 <= self._c < 4:
                return 81, 258
            if 4 <= self._c < 6:
                return 81, 270
            if 6 <= self._c < 8:
                return 66, 270
        if self._left == True:
            if 0 <= self._c < 2:
                return 66, 258
            if 2 <= self._c < 4:
                return 66, 270
            if 4 <= self._c < 6:
                return 81, 270
            if 6 <= self._c < 8:
                return 81, 258

   
class Peach(Actor):

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 15, 22
        self._cp = 0.1
        self._arena = arena
        arena.add(self)

    def move(self):
        self._cp = self._cp + 0.5
        if self._cp > 25.1:
            self._cp = 0.1

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if 0.1 <= self._cp < 17.1:
            return 158,126
        if 17.1 <= self._cp < 18.1:
            return 184, 126
        if 18.1 <= self._cp < 19.1:
            return 158, 126
        if 19.1 <= self._cp < 20.1:
            return 184, 126
        if 20.1 <= self._cp < 21.1:
            return 158, 126
        if 21.1 <= self._cp < 22.1:
            return 184, 126
        if 22.1 <= self._cp < 23.1:
            return 158, 126
        if 23.1 <= self._cp < 24.1:
            return 184, 126
        if 24.1 <= self._cp <= 25.1:
            return 158, 126

    def victory(self):
        pass

class FireBall(Jumper):

    def __init__(self, arena, x, y):
        Jumper.__init__(self, arena, x, y)
        self._w, self._h = 13, 16
        self._speed, self._max_speed = 2, 4
        self._left = False
        self._right = True
        self._ladder = None
        self._arena = arena
        self._l = 0
        self._r = 0
        self._c = 0
        self.going_right()

    def collide(self, other):
        bx, by, bw, bh = self.rect()  # jumper's pos
        wx, wy, ww, wh = other.rect() # other's pos
        n=randint(0, 1)
        if (isinstance(other, Ladder)) and wy <= by + bh <= wy + wh and wx < bx + bw // 2 < wx + ww:
            self._ladder = other
            FireBall.go_up()
            self._speed = -self._speed 
                
        elif isinstance(other, Platform) and not self._climbing:
            if by + bh < wy + wh:
                self._y = wy - bh
                self._landed = True
            
    def rect(self):
        return self._x, self._y, self._w, self._h
        
    def move(self):
        self._c += 1
        if self._c >= 4:
            self._c = 0

        aw, ah = self._arena.size()
        if self._x + self._w >= aw:
            self._right = False
            self._left = True
            self.going_left()
        elif self._x <= 0:
            self._right = True
            self._left = False
            self.going_right()
        Jumper.move(self)

    def going_left(self):
        self._dx = -self._speed

    def going_right(self):
        self._dx = +self._speed

    def symbol(self):
        if self._right == True:
            if 0 <= self._c < 2:
                return 158, 221
            if 2 <= self._c <= 4:
                return 180, 221
        if self._left == True:
            if 0 <= self._c < 2:
                return 112, 221
            if 2 <= self._c <= 4:
                return 133, 221

       

class OIL(Actor):

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 16, 24
        self._op = 0
        self._arena = arena
        arena.add(self)

    def move(self):
        self._op = self._op + 1
        if self._op > 3:
            self._op = 0

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if 0 <= self._op <= 1:
            return 125, 256
        if 2 <= self._op <= 3:
            return 144, 256

    def victory(self):
        pass

class StaticBarrels(Actor):

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 10, 16
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 113, 264

    def victory(self):
        pass
                             
class Kong(Actor):

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 47, 34
        self._kb = 1            #contatore animazione kong che lancia i barili
        self._ks = 0
        self._b = False         #contatore momento esatto di kong che lascia il barile 
        self._n = 0             #conattore generatore random barili
        self._DropBarrel = False
        self._arena = arena
        arena.add(self)

    def move(self):
        
        if self._DropBarrel == False:
           self._n = randint (0, 50)

        if self._n==1:
            self._kb +=1
            if self._kb > 30:
                self._kb = 0
        else:
            self._ks +=1
            self._kb=100
            if self._ks==20:
                self._ks=0
           


    def collide(self, other):
        pass

        
    def rect(self):
        return self._x, self._y, self._w, self._h


    def symbol(self):
        if self._n==1:
            if 0 <= self._kb < 5:
                self._b = True               #donkeykong in posizione di riposo
                self._DropBarrel = True  
                return 108, 149
            if 5 <= self._kb < 15:      #donkeykong prende il barile
                return 8, 149
            if 15 <= self._kb < 20:     #donkeykong in posizione di riposo con il barile  
                return 157, 149
            if 20 <= self._kb <= 30:    #viene gerato il barile e donkeykong lo lancia
                if self._b:
                    self._b = False
                    Barrel(arena, 60, 74)
                if self._kb == 30:
                    self._DropBarrel = False
                return 253, 149
        else:                           #kong batte i pugni sul petto
            if 0 <= self._ks < 10:
                  return 57, 149
            if 10 <= self._ks <= 20:
                return 202, 149
            
    def victory(self):
        pass
                             
class Platform(Actor):

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 16, 8
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return -1, -1

    def victory(self):
        pass

class Ladder(Actor):

    def __init__(self, arena, x, y, h):
        self._x, self._y = x, y
        self._w, self._h = 8, h
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return -1, -1        

    def victory(self):
        pass
                             
def update():
    arena.move_all()

    n=randint(0, 200)
    if n==1:
        fireball = FireBall(arena, 20, 219)
 
    game2d.image_blit(background, (0, 0))
    for a in arena.actors():
        x, y, w, h = a.rect()
        xs, ys = a.symbol()
        if xs >= 0 and ys >= 0:
            game2d.image_blit(sprites, (x, y), area=(xs, ys, w, h))
            
            
def keydown(code):
    if code == "Space":
        mario.jump()
    elif code == "ArrowLeft":
        mario.go_left()
    elif code == "ArrowRight":
        mario.go_right()
    elif code == "ArrowUp":
        mario.go_up()
    elif code == "ArrowDown":
        mario.go_down()

def keyup(code):
    if code in ("ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"):
        mario.stay()

def main():
    global arena, mario, sprites, background
    
    arena = Arena(224, 256)
    peach = Peach(arena, 88, 34)
    oil = OIL(arena, 16, 224)
    staticbarrels = [StaticBarrels(arena, 0, 68),
                     StaticBarrels(arena, 10, 68),
                     StaticBarrels(arena, 0, 52),
                     StaticBarrels(arena, 10, 52)]
    kong= Kong(arena, 20, 51)    
    mario = Mario(arena, 50, 232)
    

    for t, x, y, w, h in map_elements:
        if t == "Platform":
            Platform(arena, int(x), int(y))
        elif t == "Ladder":
            Ladder(arena, int(x), int(y), int(h))

    game2d.canvas_init(arena.size())
    sprites = game2d.image_load("dk_sprites.png")
    background = game2d.image_load("dk_background.png")

    game2d.handle_keyboard(keydown, keyup)
    game2d.set_interval(update, 1000 // 30)
    
main()
