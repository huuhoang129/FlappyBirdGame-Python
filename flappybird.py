import pygame, sys, random

# Tạo cửa sổ game
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
screen = pygame.display.set_mode((432,748))
icon = pygame.image.load('assests/ico/Flappy_Bird_icon_32x32.png')
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(icon)
game_font = pygame.font.Font('font/04B_19.TTF', 40)
clock = pygame.time.Clock()

# Create bien game
gravity = 0.23
bird_movement = 0
game_active = True
score = 0
high_score = 0


#Insert background
bg = pygame.image.load('assests/background-night.png')
bg = pygame.transform.scale2x(bg)

#Insert floor
floor = pygame.image.load('assests/floor.png')
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#Insert bird
bird_down = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-downflap.png'))
bird_mid = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-midflap.png'))
bird_up = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-upflap.png'))
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 374))

birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

#Insert pipe
pipe_surface = pygame.image.load('assests/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [250, 300, 350, 400, 450, 500]
#Create timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)

# Tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assests/message.png'))
game_over_rect = game_over_surface.get_rect(center =(216, 374))

# Chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_coutdown = 210
# Hàm tạo sàn
def draw_floor():
    screen.blit(floor,(floor_x_pos,640))
    screen.blit(floor,(floor_x_pos + 432,640))

# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (480, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (480, random_pipe_pos-720))
    return bottom_pipe, top_pipe

# Hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes

# Hàm vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 748:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)

# Ham xu ly va cham
def check_collision(pipes):
    for pipe in pipes: 
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 640:
        return False
    return True

# Ham xoay chim
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

# Ham chuyen dong cho chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_react = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_react

# Ham hien thi diem
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f"Score: {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216, 600))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
# Vòng lặp game
passed_pipes = []
previous_score = 0  # Ban đầu đặt khác điểm số thực tế    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,374)
                bird_movement = 0
                score = 0
                previous_score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        bird, bird_rect = bird_animation()
    clock.tick(120) # FPS: 120
    screen.blit(bg,(0,0))

    if game_active:
        # Tạo trọng lực cho bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)

        game_active = check_collision(pipe_list)

        # Ông
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        score_display('main game')

        # Kiểm tra điểm khi chim vượt qua giữa hai cột
        for pipe in pipe_list:
            if pipe.bottom >= 748 and pipe not in passed_pipes:  # Kiểm tra cột dưới
                if bird_rect.left > pipe.right:  # Chim đã vượt qua cột
                    score += 1
                    score_sound.play()
                    passed_pipes.append(pipe)

        if int(score) > previous_score and int(score) % 1 == 0:
            score_sound.play()
            previous_score = int(score)
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos < -432:
        floor_x_pos = 0

    pygame.display.update()
pygame.quit()