import os
import pygame as pg
import random 

WIDTH = 500
HEIGHT = 800

dir = '/home/hariaot/Documentos/Seccomp/IAFlappyBird/imgs'
print(dir)

IMG_PIPE = pg.transform.scale2x(pg.image.load(os.path.join(dir, 'pipe.png')))
IMG_FLOOR = pg.transform.scale2x(pg.image.load(os.path.join(dir, 'base.png')))
IMG_BG = pg.transform.scale2x(pg.image.load(os.path.join(dir, 'bg.png')))
IMG_BIRD = [ 
        pg.transform.scale2x(pg.image.load(os.path.join(dir, 'bird1.png'))),
        pg.transform.scale2x(pg.image.load(os.path.join(dir, 'bird2.png'))),
        pg.transform.scale2x(pg.image.load(os.path.join(dir, 'bird3.png')))
        ]

pg.font.init()
FONT_SCORE = pg.font.SysFont('arial', 25)

class Bird:
    IMGS = IMG_BIRD
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    TIME_ANIMATION = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.cont_img = 0
        self.img = self.IMGS[0]

    def fly(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1
        deslc = 1.5 * (self.time**2) + self.speed*self.time

        if deslc > 16:
            deslc = 16 
        elif deslc < 0:
            deslc -= 2

        self.y += deslc
        
        if deslc < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
               self.angle -= self.ROTATION_SPEED
    
    def draw (self, screen):
        self.cont_img += 1

        if self.cont_img < self.TIME_ANIMATION:
            self.img = self.IMGS[0]
        elif self.cont_img < self.TIME_ANIMATION*2:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TIME_ANIMATION*3:
            self.img = self.IMGS[2]
        elif self.cont_img < self.TIME_ANIMATION*4:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TIME_ANIMATION*4+1:
            self.img = self.IMGS[0]
            self.cont_img = 0
        if self.angle <= -80:
            self.img = self.IMGS[1]
            self.cont_img = self.TIME_ANIMATION*2

        img_rot = pg.transform.rotate(self.img, self.angle)
        after_cntr_img = self.img.get_rect(topleft=(self.x, self.y)).center
        retangle = img_rot.get_rect(center=after_cntr_img)
        screen.blit(img_rot, retangle.topleft)

    def get_mask(self):
        return pg.mask.from_surface(self.img)

    
class Pipe:
    DISTANCE = 200
    SPEED = 5    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_bot = 0
        self.TOP_PIPE = pg.transform.flip(IMG_PIPE, False, True)
        self.BOT_PIPE = IMG_PIPE
        self.passed = False
        self.defi_height()

    def defi_height(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.TOP_PIPE.get_height()
        self.pos_bot = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.BOT_PIPE, (self.x, self.pos_bot))
        screen.blit(self.TOP_PIPE, (self.x, self.pos_top))

    def colision(self, Bird):
        bird_mask = Bird.get_mask()
        top_mask = pg.mask.from_surface(self.TOP_PIPE)
        bot_mask = pg.mask.from_surface(self.BOT_PIPE)

        bird_top_distance = (self.x - Bird.x, self.pos_top - round(Bird.y))
        bird_bot_distance = (self.x - Bird.x, self.pos_bot - round(Bird.y))

        top_colision_point = bird_mask.overlap(top_mask, bird_top_distance)
        bot_colision_point = bird_mask.overlap(bot_mask, bird_bot_distance)

        if bot_colision_point or top_colision_point:
            return True
        else:
            return False

class Floor:
    SPEED = 5
    LENGTH = IMG_FLOOR.get_width()
    IMG = IMG_FLOOR
    
    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LENGTH

    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        if self.x0 + self.LENGTH < 0:
            self.x0 = self.x1 + self.LENGTH
        if self.x1 + self.LENGTH < 0:
            self.x1 = self.x0 + self.LENGTH
        
    def draw(self, screen):
        screen.blit(self.IMG, (self.x0, self.y))
        screen.blit(self.IMG, (self.x1, self.y))

def draw_screen(screen, birds, pipes, floor, score):
    screen.blit(IMG_BG, (0,0))

    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)
    
    floor.draw(screen)
    text = FONT_SCORE.render(f"Score: {score}", 1,(255, 255, 255))
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))
        
    pg.display.update()

def main():
    birds = [Bird(230, 250)]
    floor = Floor(730)
    pipes = [Pipe(700)]

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    score = 0

    clock = pg.time.Clock()

    flying = True
    while flying:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flying = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    for bird in birds:
                        bird.fly()
        for bird in birds:
            bird.move()
        floor.move()
        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colision(bird):
                    birds.pop(i)
                    main()
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if(bird.y + bird.img.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                main()

        draw_screen(screen, birds, pipes, floor, score)

if __name__ == '__main__':
    main()