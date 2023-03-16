import pygame as pg
import sys,math,time,os

#セーブデータの読み込み
savepath="game_make\savedate\main_save" #セーブデータのパス
if os.path.isfile(savepath) == False:
    with open(savepath, 'w', encoding='utf-8') as f_main:
        f_main.write('money 0')
        f_main.write('hit 0')

with open(savepath, 'r', encoding='utf-8') as f_main:
    lines = f_main.readlines()
    for line in lines:
        if "money" in line:
            money = int(line[6:])
        elif "hit" in line:
            hit = int(line[4:])


displayx,displayy=640,480
SCR_RECT = pg.Rect(0,0,displayx,displayy)
GAME=pg.display.set_mode((displayx,displayy))
pg.display.set_caption('ブロック崩し')

FPS = 30
fpsClock = pg.time.Clock()
vx = 5
vy = 5

class barsprite(pg.sprite.Sprite):
    # コンストラクタ（初期化メソッド）
    def __init__(self, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom - 20  # パドルのy座標

    def update(self):
        #跳ね返しバーのx座標を矢印キーで動かす
        if pressed_key[pg.K_RIGHT]:
            if self.rect.right < SCR_RECT.right:
                self.rect.centerx += (vx+5)
        elif pressed_key[pg.K_LEFT]:
            if self.rect.left > SCR_RECT.left:
                self.rect.centerx -= (vx+5)
        self.rect = self.rect.clamp(SCR_RECT)
    
    def draw(self, SCR_RECT):
        SCR_RECT.blit(self.image, self.rect)

class ballsprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pg.sprite.Sprite.__init__(self)
        self.image =  pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.vx = vx
        self.vy = vy
        self.update = self.start
        self.hit=0
    def move(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 :
            self.vy = -self.vy
        
        #バーにあたったときの処理
        if self.rect.colliderect(bar.rect):
            left,right=135,45
            x=self.rect.centerx
            tan=math.radians(left-((left - right) * (x - bar.rect.left) / bar.rect.width))
            spead = ((self.vx)**2 + (self.vy)**2)**(1/2)
            self.vx = spead * math.cos(tan)
            self.vy = -spead * math.sin(tan)
        
        #ボールを落とした時の処理
        if self.rect.bottom > SCR_RECT.height:
            self.update = self.start
        
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)

        #ブロックとの衝突時の処理
        blocks_collided = pg.sprite.spritecollide(self, blocks, True)
        if blocks_collided:
            oldrect = self.rect
            for block in blocks_collided:
                x=(block.rect.left-SCR_RECT.left-15)/block.rect.width
                y=(block.rect.top-SCR_RECT.top)/block.rect.height
                losttime=int(time.time())
                lostblocks.append([losttime,x,y])
                # ボールが左からブロックへ衝突した場合
                if oldrect.left < block.rect.left and oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.vx = -self.vx

                # ボールが右からブロックへ衝突した場合
                if block.rect.left < oldrect.left and block.rect.right < oldrect.right:
                    self.rect.left = block.rect.right
                    self.vx = -self.vx

                # ボールが上からブロックへ衝突した場合
                if oldrect.top < block.rect.top and oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.vy = -self.vy

                # ボールが下からブロックへ衝突した場合
                if block.rect.top < oldrect.top and block.rect.bottom < oldrect.bottom:
                    self.rect.top = block.rect.bottom
                    self.vy = -self.vy
            self.hit += 1
            # 衝突回数に応じてスコア加算
            score.add_score(self.hit * 10)
    
    def start(self):
        # ボールの初期位置
        # 跳ね返しバーの上、センタリング
        self.rect.centerx = bar.rect.centerx
        self.rect.bottom = bar.rect.top
        self.hit=0
        # スペースでボール発射
        if pressed_key[pg.K_SPACE]:
            spead = ((self.vx)**2 + (self.vy)**2)**(1/2)
            self.vx = 0
            self.vy = -spead
            self.update = self.move
    
    def draw(self, SCR_RECT):
        SCR_RECT.blit(self.image, self.rect)

class Blocksprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.image.load(filename).convert()
        self.rect = self.image.get_rect()
        # ブロックの左上座標
        self.rect.left = SCR_RECT.left + x * self.rect.width+15
        self.rect.top = SCR_RECT.top + y * self.rect.height

# スコアのクラス
class moneysprite():
    def __init__(self, x, y):
        self.sysfont = pg.font.SysFont(None, 20)
        self.score = money
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        img = self.sysfont.render("money " + str(self.score), True, (255, 255, 250))
        screen.blit(img, (self.x, self.y))

    def add_score(self, x):
        self.score += x
        with open(savepath, "w", encoding='utf-8') as f_main:
            f_main.write(f"money {self.score}")

screen = pg.display.set_mode(SCR_RECT.size)
pg.init()
idx=0
blocks = pg.sprite.Group()
lostblocks=[]

ball = ballsprite("game_make\image\_ball.png",100,100,vx,vy)
bar  = barsprite("game_make\image\_bar.png")
score=moneysprite(10,10)
Blocksprite.containers = blocks

for x in range(0, 20):
    for y in range(1, 9):
        Blocksprite("game_make\image\_block.png", x, y)

#option
regist=10 #消したブロックが蘇るまでの時間

while True:
    pg.init()
    GAME.fill((0, 0, 0))
    pressed_key = pg.key.get_pressed()
    nowtime=int(time.time())
    
    #タイトル画面
    if idx==0:
        button = pg.Rect(SCR_RECT.centerx-60, SCR_RECT.centery+20, 120,30 )
        text1 = pg.font.SysFont(None, 40).render("BLOCK BREAK", True, (55,255,255))
        text2 = pg.font.SysFont(None, 25).render("START", True, (0,0,0))
        pg.draw.rect(screen, (0, 255, 0), button)
        screen.blit(text1, (SCR_RECT.centerx-100,SCR_RECT.centery-10))
        screen.blit(text2, (SCR_RECT.centerx-30,SCR_RECT.centery+30))
        for event in pg.event.get():
            if event.type==pg.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    idx=1
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if pressed_key[pg.K_ESCAPE]:
                pg.quit()
                sys.exit()


    #GAME画面
    if idx==1:
        #消したブロックの復活
        for lostblock in lostblocks:
            if regist+lostblock[0]<nowtime:
                x,y=lostblock[1],lostblock[2]
                Blocksprite("game_make\image\_block.png", x, y)
                lostblocks.remove(lostblock)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if pressed_key[pg.K_ESCAPE]:
                pg.quit()
                sys.exit()

        # 基礎GAME画面
        ball.update()
        bar.update()
        blocks.update()
        ball.draw(screen)
        bar.draw(screen)
        blocks.draw(screen)
        score.draw(screen)
        


    # 画面更新
    pg.display.update()
    fpsClock.tick(FPS)