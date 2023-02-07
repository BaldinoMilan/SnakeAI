import pygame, random

snake_asset_files = (
     "apple.png",
     "body_bottomleft.png", "body_bottomright.png",
     "body_horizontal.png", "body_topleft.png",
     "body_topright.png",   "body_vertical.png",
     "head_down.png",       "head_left.png",
     "head_right.png",      "head_up.png",
     "tail_down.png",       "tail_left.png",
     "tail_right.png",      "tail_up.png"
)

square_colors = ((50, 200, 50), (20, 220, 20))


def load_asset(filepath):
    name = filepath.split('/')[1]
    name = name.split('.')[0]

    return name, pygame.image.load(filepath)

class Snack:
    def __init__(self, body, rows):
        found = False
        while not found:
            found = self.generate(body, rows)

    def generate(self, body, rows):
        self.pos = (random.randint(0, rows-1), random.randint(0, rows-1))
    
        for cube in body:
            if cube.pos == self.pos:
                return False
            
        return True

    def draw(self, surface, sprite):
        surface.blit(sprite, (self.pos[0]*sprite.get_width(), self.pos[1]*sprite.get_height()))


class Body:
    def __init__(self, pos, dire):
        self.pos = (pos[0], pos[1])
        self.dir = (dire[0], dire[1])

    def draw(self, surface, sprite):
        surface.blit(sprite, (self.pos[0]*sprite.get_width(), self.pos[1]*sprite.get_height()))

    def update(self):
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])


class Snake:
    def __init__(self, start_pos, start_dir, rows):
        second_pos = (start_pos[0] - start_dir[0], start_pos[1] - start_dir[1])     
        self.body = [Body(start_pos, start_dir), Body(second_pos, start_dir)]    
        self.rows = rows

        self.assets = dict()
        for file in snake_asset_files:
            name, asset = load_asset("assets/" + file)
            self.assets[name] = asset

        self.snack = Snack(self.body, self.rows)
        
    def update(self):
        for i in reversed(range(1, len(self.body))):
            self.body[i].update()
            self.body[i].dir = self.body[i - 1].dir

        self.body[0].update()

    def collideSnack(self):
        if self.snack.pos == self.body[0].pos:
            self.extendBody()
            self.snack = Snack(self.body, self.rows)
            return True
        
        return False

    def checkLoss(self):
        head = self.body[0]
        if head.pos[0] < 0 or head.pos[0] >= self.rows or head.pos[1] < 0 or head.pos[1] >= self.rows:
            return True

        for cube in self.body[3:]:
            if cube.pos == head.pos:
                return True
        return False
        
    
    def draw(self, surface):
        offset_w = surface.get_width()//self.rows
        offset_h = surface.get_height()//self.rows

        self.drawGrid(surface)

        sprite = pygame.transform.scale(self.assets["apple"].copy(), (offset_w, offset_h))
        self.snack.draw(surface, sprite)
        
        sprite = pygame.transform.scale(self.getHeadAsset(), (offset_w, offset_h))
        self.body[0].draw(surface, sprite)

        for i in range(1, len(self.body)-1):
            sprite = pygame.transform.scale(self.getBodyAsset(i), (offset_w, offset_h))
            self.body[i].draw(surface, sprite)

        sprite = pygame.transform.scale(self.getTailAsset(), (offset_w, offset_h))
        self.body[-1].draw(surface, sprite)

    def changeDir(self, new_dir):
        head = self.body[0]
        if new_dir[0] != -head.dir[0] and new_dir[1] != -head.dir[1]:
            head.dir = new_dir

    def extendBody(self):
        tail = self.body[-1]
        pos = (tail.pos[0] - tail.dir[0], tail.pos[1] - tail.dir[1])
        self.body.append(Body(pos, tail.dir))

    def drawGrid(self, surface):
        offset_w = surface.get_width()/self.rows
        offset_h = surface.get_height()/self.rows
        for i in range(self.rows):
            for j in range(self.rows):
                rect = pygame.rect.Rect(i*offset_w, j*offset_h, offset_w, offset_h)
                pygame.draw.rect(surface, square_colors[(i+j)%2], rect)

    def getHeadAsset(self):
        head = self.body[0]
        if head.dir[0] ==  1:
            return self.assets["head_right"].copy()
        if head.dir[0] == -1:
            return self.assets["head_left"].copy()
        if head.dir[1] == -1:
            return self.assets["head_up"].copy()
        if head.dir[1] ==  1:
            return self.assets["head_down"].copy()
    
    def getBodyAsset(self, index):
        next_ = self.body[index+1]
        prev_ = self.body[index]
        
        if next_.dir[0] != 0 and prev_.dir[0] != 0:
            return self.assets["body_horizontal"].copy()
        if next_.dir[1] != 0 and prev_.dir[1] != 0:
            return self.assets["body_vertical"].copy()
        if (next_.dir[0] == 1 and prev_.dir[1] == 1) or (next_.dir[1] == -1 and prev_.dir[0] == -1):
            return self.assets["body_bottomleft"].copy()
        if (next_.dir[0] == -1 and prev_.dir[1] == 1) or (next_.dir[1] == -1 and prev_.dir[0] == 1):
            return self.assets["body_bottomright"].copy()
        if (next_.dir[0] == 1 and prev_.dir[1] == -1) or (next_.dir[1] == 1 and prev_.dir[0] == -1):
            return self.assets["body_topleft"].copy()
        if (next_.dir[0] == -1 and prev_.dir[1] == -1) or (next_.dir[1] == 1 and prev_.dir[0] == 1):
            return self.assets["body_topright"].copy()
    
    def getTailAsset(self):
        tail = self.body[-1]
        if tail.dir[0] ==  1:
            return self.assets["tail_left"].copy()
        if tail.dir[0] == -1:
            return self.assets["tail_right"].copy()
        if tail.dir[1] == -1:
            return self.assets["tail_down"].copy()
        if tail.dir[1] ==  1:
            return self.assets["tail_up"].copy()

    
    


        
