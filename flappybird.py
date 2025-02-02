import pygame, sys, random

# Tạo cửa sổ game
pygame.init()
screen = pygame.display.set_mode((432,748))
icon = pygame.image.load('assests/ico/Flappy_Bird_icon_32x32.png')
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Create gravity
gravity = 0.25
bird_movement = 0

#Insert background
bg = pygame.image.load('assests/background-night.png')
bg = pygame.transform.scale2x(bg)

#Insert floor
floor = pygame.image.load('assests/floor.png')
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#Insert bird
bird = pygame.image.load('assests/yellowbird-midflap.png')
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 374))

#Insert pipe
pipe_surface = pygame.image.load('assests/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [250, 300, 350, 400, 450, 500]
#Create timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)

# Hàm tạo sàn
def draw_floor():
    screen.blit(floor,(floor_x_pos,640))
    screen.blit(floor,(floor_x_pos + 432,640))

# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-650))
    return bottom_pipe, top_pipe

# Hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Hàm vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 748:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)
    
# Vòng lặp game    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -11
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
    clock.tick(120) # FPS: 120
    screen.blit(bg,(0,0))

    # Tạo trọng lực cho bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird,bird_rect)

    # Ông
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)

    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos < -432:
        floor_x_pos = 0

    pygame.display.update()
pygame.quit()