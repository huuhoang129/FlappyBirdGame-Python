import pygame

# Tạo cửa sổ game
pygame.init()
screen = pygame.display.set_mode((432,748))
icon = pygame.image.load('assets/ico/Flappy_Bird_icon_32x32.png')
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

while True:
    clock.tick(120) # FPS: 120

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
pygame.quit()