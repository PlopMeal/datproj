import math
import sys

import pygame

# Runtime / pacing
WIDTH, HEIGHT = 960, 540
FPS = 30
DURATION_SECONDS = 30
TOTAL_FRAMES = FPS * DURATION_SECONDS

# Colors
BG_SKY = (28, 23, 48)
BG_FLOOR = (58, 43, 38)
MOON = (232, 225, 189)
TEXT = (245, 245, 245)
BLAIR_SKIN = (229, 190, 150)
BLAIR_SHIRT = (50, 145, 197)
BLAIR_PANTS = (40, 55, 70)
ALIEN_SKIN = (116, 224, 186)
ALIEN_GARMENT = (140, 85, 170)
SPARK = (255, 250, 170)
HOUSE = (94, 70, 65)
DOOR = (60, 40, 38)
WINDOW = (255, 216, 130)
APPENDAGE_MAIN = (120, 206, 170)
APPENDAGE_CAP = (164, 242, 206)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def ease_out_quad(t):
    t = clamp(t, 0.0, 1.0)
    return 1.0 - (1.0 - t) * (1.0 - t)


def draw_background(surface, frame):
    surface.fill(BG_SKY)
    pygame.draw.circle(surface, MOON, (130, 110), 50)

    for i in range(18):
        x = 40 + i * 50
        y = 30 + (i * 37) % 140
        tw = (math.sin(frame * 0.06 + i) + 1) * 0.5
        r = 1 + int(tw * 2)
        pygame.draw.circle(surface, (200 + int(tw * 55),) * 3, (x, y), r)

    pygame.draw.rect(surface, BG_FLOOR, (0, HEIGHT - 140, WIDTH, 140))


def draw_house(surface):
    base = pygame.Rect(70, 160, 390, 260)
    pygame.draw.rect(surface, HOUSE, base, border_radius=8)
    roof = [(50, 170), (265, 65), (490, 170)]
    pygame.draw.polygon(surface, (72, 52, 50), roof)

    door = pygame.Rect(225, 280, 90, 140)
    pygame.draw.rect(surface, DOOR, door, border_radius=4)
    pygame.draw.circle(surface, (180, 150, 90), (295, 352), 5)

    for wx in (110, 340):
        w = pygame.Rect(wx, 225, 70, 55)
        pygame.draw.rect(surface, WINDOW, w)
        pygame.draw.rect(surface, (80, 60, 56), w, 4)
        pygame.draw.line(surface, (80, 60, 56), (wx + 35, 225), (wx + 35, 280), 3)
        pygame.draw.line(surface, (80, 60, 56), (wx, 252), (wx + 70, 252), 3)


def draw_blair(surface, x, y, panic=0.0, run=0.0):
    stride = math.sin(run * 8.0) * 12
    lean = panic * 12 + run * 15

    torso = pygame.Rect(int(x - 18), int(y - 70), 36, 56)
    pygame.draw.rect(surface, BLAIR_SHIRT, torso, border_radius=8)

    head_center = (int(x - lean * 0.3), int(y - 94))
    pygame.draw.circle(surface, BLAIR_SKIN, head_center, 16)

    eye_wide = 2 + int(panic * 3)
    pygame.draw.circle(surface, (0, 0, 0), (head_center[0] - 6, head_center[1] - 2), eye_wide)
    pygame.draw.circle(surface, (0, 0, 0), (head_center[0] + 6, head_center[1] - 2), eye_wide)

    mouth_w = 8 + int(panic * 8)
    pygame.draw.arc(surface, (90, 40, 40), (head_center[0] - mouth_w // 2, head_center[1] + 4, mouth_w, 8), math.pi, 2 * math.pi, 2)

    arm_raise = panic * 30
    pygame.draw.line(surface, BLAIR_SKIN, (x - 14, y - 56), (x - 34, y - 30 - arm_raise), 6)
    pygame.draw.line(surface, BLAIR_SKIN, (x + 14, y - 56), (x + 35, y - 34 - arm_raise), 6)

    l1 = (x - 10, y - 14)
    l2 = (x - 8 - stride, y + 30)
    r1 = (x + 10, y - 14)
    r2 = (x + 8 + stride, y + 30)
    pygame.draw.line(surface, BLAIR_PANTS, l1, l2, 8)
    pygame.draw.line(surface, BLAIR_PANTS, r1, r2, 8)


def draw_alien_cub(surface, x, y, sway=1.0, shock=0.0, shredded=0.0, appendage_flip=0.0):
    offset = math.sin(sway * 6.0) * 8
    body_center = (int(x + offset), int(y - 45))

    # body (standing on ground)
    pygame.draw.ellipse(surface, ALIEN_SKIN, (body_center[0] - 24, body_center[1] - 22, 48, 54))
    pygame.draw.circle(surface, ALIEN_SKIN, (body_center[0], body_center[1] - 34), 17)

    pygame.draw.circle(surface, (20, 30, 25), (body_center[0] - 6, body_center[1] - 36), 3)
    pygame.draw.circle(surface, (20, 30, 25), (body_center[0] + 6, body_center[1] - 36), 3)

    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] - 20, body_center[1] - 8), (body_center[0] - 35, body_center[1] + 5), 5)
    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] + 20, body_center[1] - 8), (body_center[0] + 35, body_center[1] + 5), 5)
    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] - 10, body_center[1] + 28), (body_center[0] - 10, body_center[1] + 46), 6)
    pygame.draw.line(surface, ALIEN_SKIN, (body_center[0] + 10, body_center[1] + 28), (body_center[0] + 10, body_center[1] + 46), 6)

    if shredded < 1.0:
        g_h = int(26 * (1.0 - 0.4 * shredded))
        g_y = body_center[1] + 4
        pygame.draw.ellipse(surface, ALIEN_GARMENT, (body_center[0] - 21, g_y, 42, g_h))

    if shredded > 0.2:
        for i in range(5):
            dx = -15 + i * 7
            dy = int(12 + i * 2)
            tlen = int(8 + 20 * shredded)
            pygame.draw.line(surface, ALIEN_GARMENT, (body_center[0] + dx, body_center[1] + dy), (body_center[0] + dx - 4, body_center[1] + dy + tlen), 2)

    # Fantasy appendage: thick trunk + mushroom-like cap + two orbs
    base = (body_center[0], body_center[1] + 20)
    if appendage_flip > 0.0:
        ang = -1.5 + appendage_flip * 1.9
    else:
        ang = 1.2

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


def draw_caption(surface, text, alpha=255, y=24):
    if not text:
        return
    font = pygame.font.SysFont("arial", 28, bold=True)
    img = font.render(text, True, TEXT)
    img.set_alpha(alpha)
    rect = img.get_rect(center=(WIDTH // 2, y))
    surface.blit(img, rect)


def draw_fin(surface, frame):
    pulse = 0.75 + 0.25 * math.sin(frame * 0.2)
    color = (int(240 * pulse), int(240 * pulse), int(240 * pulse))
    font = pygame.font.SysFont("arial", 92, bold=True)
    txt = font.render("FIN", True, color)
    rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(txt, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fantasy Flash-Style Animation")
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

        draw_background(screen, frame)
        draw_house(screen)

        t = frame / FPS

        caption = ""
        if t < 8:
            caption = "Blair babysits through a quiet fantasy night..."
            draw_alien_cub(screen, 620, 355, sway=t * 0.35, shock=0.0, shredded=0.0, appendage_flip=0.0)
            draw_blair(screen, 300, 390, panic=0.0, run=0.0)

        elif t < 15:
            p = (t - 8) / 7
            caption = "He notices the cub's huge alien appendage... and freezes."
            draw_alien_cub(screen, 620, 355, sway=t * 0.8, shock=0.0, shredded=0.0, appendage_flip=0.0)
            draw_blair(screen, 300 + 40 * p, 390, panic=ease_out_quad(p) * 0.6, run=0.0)

        elif t < 20:
            p = (t - 15) / 5
            caption = "A sudden arc of magic-electric shock crackles!"
            draw_alien_cub(screen, 620, 355, sway=t * 1.2, shock=p, shredded=0.0, appendage_flip=0.0)
            draw_blair(screen, 350, 390, panic=0.6 + 0.4 * ease_out_quad(p), run=0.0)

        elif t < 24:
            p = (t - 20) / 4
            caption = "The garment shreds, and the appendage snaps upward!"
            draw_alien_cub(screen, 620, 355, sway=t * 1.5, shock=1.0 - p * 0.8, shredded=p, appendage_flip=p)
            draw_blair(screen, 350, 390, panic=1.0, run=0.0)

        elif t < 28:
            p = (t - 24) / 4
            blair_x = 350 - int(560 * p)
            caption = "Blair panics and bolts out of the house!"
            draw_alien_cub(screen, 620, 355, sway=t * 1.8, shock=0.0, shredded=1.0, appendage_flip=1.0)
            if blair_x > -80:
                draw_blair(screen, blair_x, 390, panic=1.0, run=p * 1.8)
        else:
            draw_fin(screen, frame)

        if t < 28:
            draw_caption(screen, caption, 240)

        pygame.display.flip()
        clock.tick(FPS)
        frame += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
