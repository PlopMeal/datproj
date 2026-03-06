import math
import sys

import pygame

WIDTH, HEIGHT = 960, 540
FPS = 30
DURATION_SECONDS = 30
TOTAL_FRAMES = FPS * DURATION_SECONDS

SKY = (90, 170, 220)
GRASS = (70, 155, 75)
PATH = (195, 175, 145)
TEXT = (245, 245, 245)
TREE_TRUNK = (110, 76, 46)
TREE_LEAF = (63, 135, 73)
BENCH = (129, 82, 52)
BLAIR_SKIN = (229, 190, 150)
BLAIR_SHIRT = (50, 145, 197)
BLAIR_PANTS = (40, 55, 70)
MAN_SHIRT = (175, 80, 70)
MAN_PANTS = (55, 60, 90)
ALIEN_SKIN = (116, 224, 186)
ALIEN_GARMENT = (140, 85, 170)
SPARK = (255, 250, 170)
APPENDAGE_MAIN = (120, 206, 170)
APPENDAGE_CAP = (164, 242, 206)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def ease_out_quad(t):
    t = clamp(t, 0.0, 1.0)
    return 1.0 - (1.0 - t) * (1.0 - t)


def draw_park(surface, frame):
    surface.fill(SKY)
    pygame.draw.rect(surface, GRASS, (0, HEIGHT - 210, WIDTH, 210))
    pygame.draw.rect(surface, PATH, (0, HEIGHT - 125, WIDTH, 90))

    # trees
    for x in (110, 260, 750, 860):
        pygame.draw.rect(surface, TREE_TRUNK, (x, HEIGHT - 270, 26, 110))
        sway = int(math.sin(frame * 0.04 + x) * 3)
        pygame.draw.circle(surface, TREE_LEAF, (x + 14 + sway, HEIGHT - 295), 45)

    # bench
    pygame.draw.rect(surface, BENCH, (390, HEIGHT - 205, 180, 18), border_radius=4)
    pygame.draw.rect(surface, BENCH, (405, HEIGHT - 228, 150, 16), border_radius=4)
    pygame.draw.rect(surface, BENCH, (415, HEIGHT - 175, 14, 52))
    pygame.draw.rect(surface, BENCH, (531, HEIGHT - 175, 14, 52))


def draw_person(surface, x, y, skin, shirt, pants, panic=0.0, run=0.0):
    stride = math.sin(run * 8.0) * 12
    lean = panic * 12 + run * 15

    pygame.draw.rect(surface, shirt, (int(x - 18), int(y - 70), 36, 56), border_radius=8)
    head_center = (int(x - lean * 0.3), int(y - 94))
    pygame.draw.circle(surface, skin, head_center, 16)

    eye_wide = 2 + int(panic * 3)
    pygame.draw.circle(surface, (0, 0, 0), (head_center[0] - 6, head_center[1] - 2), eye_wide)
    pygame.draw.circle(surface, (0, 0, 0), (head_center[0] + 6, head_center[1] - 2), eye_wide)

    mouth_w = 8 + int(panic * 8)
    pygame.draw.arc(surface, (90, 40, 40), (head_center[0] - mouth_w // 2, head_center[1] + 4, mouth_w, 8), math.pi, 2 * math.pi, 2)

    arm_raise = panic * 30
    pygame.draw.line(surface, skin, (x - 14, y - 56), (x - 34, y - 30 - arm_raise), 6)
    pygame.draw.line(surface, skin, (x + 14, y - 56), (x + 35, y - 34 - arm_raise), 6)

    pygame.draw.line(surface, pants, (x - 10, y - 14), (x - 8 - stride, y + 30), 8)
    pygame.draw.line(surface, pants, (x + 10, y - 14), (x + 8 + stride, y + 30), 8)


def draw_alien_cub(surface, x, y, sway=1.0, shock=0.0, shredded=0.0, appendage_flip=0.0):
    offset = math.sin(sway * 6.0) * 8
    body_center = (int(x + offset), int(y - 45))

    pygame.draw.ellipse(surface, ALIEN_SKIN, (body_center[0] - 24, body_center[1] - 22, 48, 54))
    pygame.draw.circle(surface, ALIEN_SKIN, (body_center[0], body_center[1] - 34), 17)
    pygame.draw.circle(surface, (20, 30, 25), (body_center[0] - 6, body_center[1] - 36), 3)
    pygame.draw.circle(surface, (20, 30, 25), (body_center[0] + 6, body_center[1] - 36), 3)

    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] - 20, body_center[1] - 8), (body_center[0] - 35, body_center[1] + 5), 5)
    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] + 20, body_center[1] - 8), (body_center[0] + 35, body_center[1] + 5), 5)
    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] - 10, body_center[1] + 28), (body_center[0] - 10, body_center[1] + 46), 6)
    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] + 10, body_center[1] + 28), (body_center[0] + 10, body_center[1] + 46), 6)

    if shredded < 1.0:
        pygame.draw.ellipse(surface, ALIEN_GARMENT, (body_center[0] - 21, body_center[1] + 4, 42, int(26 * (1.0 - 0.4 * shredded))))

    if shredded > 0.2:
        for i in range(5):
            dx = -15 + i * 7
            dy = int(12 + i * 2)
            pygame.draw.line(surface, ALIEN_GARMENT, (body_center[0] + dx, body_center[1] + dy), (body_center[0] + dx - 4, body_center[1] + dy + int(8 + 20 * shredded)), 2)

    base = (body_center[0], body_center[1] + 20)
    ang = (-1.5 + appendage_flip * 1.9) if appendage_flip > 0.0 else 1.2
    tip = (body_center[0] + int(math.cos(ang) * 30), body_center[1] + 20 + int(math.sin(ang) * 30))
    pygame.draw.line(surface, APPENDAGE_MAIN, base, tip, 9)
    pygame.draw.ellipse(surface, APPENDAGE_CAP, (tip[0] - 9, tip[1] - 6, 18, 12))
    pygame.draw.ellipse(surface, APPENDAGE_MAIN, (base[0] - 11, base[1] + 2, 10, 12))
    pygame.draw.ellipse(surface, APPENDAGE_MAIN, (base[0] + 1, base[1] + 2, 10, 12))

    if shock > 0.0:
        for i in range(7):
            phase = i * 0.8
            sx = body_center[0] + int(math.cos(phase + shock * 8) * (26 + i * 2))
            sy = body_center[1] + int(math.sin(phase + shock * 7) * (22 + i * 2))
            ex = sx + int(math.cos(phase * 2.1) * 14)
            ey = sy + int(math.sin(phase * 1.9) * 14)
            pygame.draw.line(surface, SPARK, (sx, sy), (ex, ey), 2)


def draw_caption(surface, text):
    if not text:
        return
    font = pygame.font.SysFont("arial", 28, bold=True)
    img = font.render(text, True, TEXT)
    rect = img.get_rect(center=(WIDTH // 2, 26))
    surface.blit(img, rect)


def draw_fin(surface, frame):
    pulse = 0.75 + 0.25 * math.sin(frame * 0.2)
    color = (int(240 * pulse),) * 3
    font = pygame.font.SysFont("arial", 92, bold=True)
    txt = font.render("FIN", True, color)
    surface.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fantasy Flash-Style Park Scene")
    clock = pygame.time.Clock()

    frame = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        if frame > TOTAL_FRAMES:
            running = False

        draw_park(screen, frame)
        t = frame / FPS

        caption = ""
        blair_x = 230
        man_x = 870
        man_visible = False
        man_panic = 0.0
        man_run = 0.0

        if t < 8:
            caption = "In the park, Blair watches over the alien cub..."
            draw_alien_cub(screen, 540, 360, sway=t * 0.35)

        elif t < 15:
            p = (t - 8) / 7
            caption = "A man walks over to ask what is going on."
            man_visible = True
            man_x = 870 - int(240 * p)
            draw_alien_cub(screen, 540, 360, sway=t * 0.8)

        elif t < 20:
            p = (t - 15) / 5
            caption = "Magic shock surges and the outfit starts to rip!"
            man_visible = True
            man_x = 630
            man_panic = 0.5 + 0.5 * p
            draw_alien_cub(screen, 540, 360, sway=t * 1.1, shock=p)

        elif t < 24:
            p = (t - 20) / 4
            caption = "The appendage snaps upward suddenly!"
            man_visible = True
            man_x = 630
            man_panic = 1.0
            draw_alien_cub(screen, 540, 360, sway=t * 1.5, shock=1.0 - p * 0.8, shredded=p, appendage_flip=p)

        elif t < 28:
            p = (t - 24) / 4
            caption = "The man screams and runs away!"
            man_visible = True
            man_panic = 1.0
            man_run = p * 2.0
            man_x = 630 + int(460 * p)
            draw_alien_cub(screen, 540, 360, sway=t * 1.8, shredded=1.0, appendage_flip=1.0)

        else:
            draw_fin(screen, frame)

        if t < 28:
            draw_person(screen, blair_x, 395, BLAIR_SKIN, BLAIR_SHIRT, BLAIR_PANTS, panic=0.2)
            if man_visible and man_x < WIDTH + 80:
                draw_person(screen, man_x, 395, BLAIR_SKIN, MAN_SHIRT, MAN_PANTS, panic=man_panic, run=man_run)
            draw_caption(screen, caption)

        pygame.display.flip()
        clock.tick(FPS)
        frame += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
