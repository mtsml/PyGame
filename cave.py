import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE, K_RETURN

pygame.init()
pygame.key.set_repeat(5,5)
SURFACE = pygame.display.set_mode((1000,600))
FPSCLOCK = pygame.time.Clock()

def main():
    walls = 50
    ship_y = 250
    velocity = 0
    score = 0
    slope = randint(5, 6)
    sysfont = pygame.font.SysFont(None, 36)
    ship_image=pygame.image.load("ship.png")
    bang_image=pygame.image.load("bang.png")
    holes = []
    bg_color = [0, 255, 0]
    fps = 15
    inflate = 0

    for xpos in range(walls):
        holes.append(Rect(xpos * 20, 100, 20, 400))

    game_over=False

    while True:
        is_space_down=False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down=True

        #自機を移動
        if not game_over:
            score += 10
            if score >= 3000 and score < 6000 :
                bg_color[0] = 0
                bg_color[1] = 0
                bg_color[2] = 255
                fps = 20
                inflate = -20
            
            elif score >= 6000:
                bg_color[0] = 255
                bg_color[1] = 0
                bg_color[2] = 0
                inflate = 20                

            velocity += -3 if is_space_down else 3
            ship_y += velocity

            #洞窟をスクロール
            edge = holes[-1].copy()
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(5, 6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, inflate)
            edge.move_ip(20, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-20, 0) for x in holes]

            #衝突?
            if holes[0].top > ship_y or holes[0].bottom < ship_y + 30:
                game_over = True
        else:
            return

        #描画
        SURFACE.fill((bg_color[0], bg_color[1], bg_color[2]))
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)

        SURFACE.blit(ship_image, (0, ship_y))
        score_image = sysfont.render("Score Is {}".format(score), True, (0, 0, 225))
        SURFACE.blit(score_image, (600, 20))

        if game_over:
            SURFACE.blit(bang_image, (0, ship_y))

        pygame.display.update()
        FPSCLOCK.tick(fps)

if __name__ == '__main__':
    main()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    main()
