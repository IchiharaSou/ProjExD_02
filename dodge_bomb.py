import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5,0),
} #練習３

accs = [a for a in range(1, 11)]

def check_bound(rect: pg.rect) -> tuple[bool,bool]: #練習４
        """
    こうかとんRect，爆弾Rectが画面外 or 画面内かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向，縦方向の判定結果タプル（True：画面内／False：画面外）
    """
        yoko, tate = True, True
        if rect.left < 0 or WIDTH < rect.right: #横方向判定
            yoko = False
        if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向判定
            tate = False
        return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_gyaku = pg.transform.flip(kk_img, True, False)
    muki = {
    (0, 0): kk_img,
    (-5, 0): kk_img,
    (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
    (0, -5): pg.transform.rotozoom(kk_gyaku, 90, 1.0),
    (+5, -5): pg.transform.rotozoom(kk_gyaku, 45, 1.0),
    (+5, 0): kk_gyaku,
    (+5, +5): pg.transform.rotozoom(kk_gyaku, -45, 1.0),
    (0, +5): pg.transform.rotozoom(kk_gyaku, -90, 1.0),
    (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0), 
    }                                                     #演習１
    '''
    キーの値にこうかとんの画像を読み込んで角度を変更する。
    右向きの画像は元画像を反転させたものを読み込んでいる。
    '''
    kk_imgs = muki
    kk_img = kk_imgs[(0,0)]
    kk_rct = kk_img.get_rect() #練習３
    kk_rct.center = 900, 400
    bb = pg.Surface((20, 20)) #練習１
    pg.draw.circle(bb, (255, 0, 0), (10, 10), 10)
    bb.set_colorkey((0, 0, 0))
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    bb_rct = bb.get_rect()
    bb_rct.center = x, y
    vx, vy = +5, +5 #練習２

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        

        if kk_rct.colliderect(bb_rct): #練習５
            print("ゲームオーバー")
            return
        
        key_lst = pg.key.get_pressed() #練習３
        sum_mv = [0, 0]
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #練習４
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs[tuple(sum_mv)]
        
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct) #練習３
        bb_rct.move_ip(vx, vy) #練習２
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()