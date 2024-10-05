#thư viện pygame
import pygame, random
pygame.mixer.pre_init(frequency=44100, size = -16, channels=2, buffer=512)
pygame.init ()

#các biến khởi tạo trong game
p = 0.1 #Hằng trọng lực
bird_y = 0 #toạn độ y của chim
score = 0 #điểm ban đầu
game_play = True
high_score = 0

#tiêu đề và icon
pygame.display.set_caption('Game 1')
icon = pygame.image.load(r'assets/yellowbird-downflap.png')
pygame.display.set_icon(icon)

#thêm background
bg = pygame.image.load(r'assets/background-night.png')
bg = pygame.transform.scale2x(bg)

#thêm sàn
fl = pygame.image.load(r'assets/floor.png')
fl = pygame.transform.scale2x(fl)
fl_x = 0
#thêm bird
bird_down = pygame.image.load(r'assets/yellowbird-downflap.png')
bird_down = pygame.transform.scale2x(bird_down)
bird_mid = pygame.image.load(r'assets/yellowbird-midflap.png')
bird_mid = pygame.transform.scale2x(bird_mid)
bird_up = pygame.image.load(r'assets/yellowbird-upflap.png')
bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_down, bird_mid, bird_up]
bird_id = 0
bird = bird_list[bird_id]
bird = pygame.transform.scale2x(bird)
bird_hcn = bird.get_rect(center=(100,286))
#tạo timer cho bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200) #200 ms

#tạo ống
pipe_sf = pygame.image.load(r'assets/pipe-green.png')
pipe_sf = pygame.transform.scale2x(pipe_sf)
pipe_list = []
#hàm tạo ống và di chuyển ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_sf.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_sf.get_rect(midtop = (500,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 786:
            screen.blit(pipe_sf,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_sf,False,True) #muốn lật đầu nào thì True ở đó (x,y)
            screen.blit(flip_pipe, pipe)
#tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1500)
pipe_height = [300, 400, 500]

#score
game_font = pygame.font.Font('04B_19.TTF',40)
def score_view():
    if game_play == True:
        score_font = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_hcn = score_font.get_rect(center=(200,100))
        screen.blit(score_font,score_hcn)
    if game_play == False:
        #Điểm chơi vòng hiện tại
        
        score_font = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_hcn = score_font.get_rect(center=(200,100))
        screen.blit(score_font,score_hcn)
        #Điểm cao nhất

        hscore_font = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        hscore_hcn = hscore_font.get_rect(center=(200,40))
        screen.blit(hscore_font,hscore_hcn)
        

#màn hình game over
screen_kt = pygame.image.load(r'assets/message.png')
screen_kt = pygame.transform.scale2x(screen_kt)
screen_kt_hcn = screen_kt.get_rect(center=(216,334))


#hàm check va chạm với sàn, trời và cột
def check_vacham(pipes):
    for pipe in pipes:
        if bird_hcn.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_hcn.bottom >= 668 or bird_hcn.top <= -75 :
        return False
    else:
        return True

#hàm xoay con chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_y*4 , 1)
    return new_bird
#bird animation
def bird_animation():
    new_bird = bird_list[bird_id]
    new_bird_rect = new_bird.get_rect(center = (100, bird_hcn.centery))
    return new_bird, new_bird_rect 

#chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_count = 100
#cửa sổ game
screen = pygame.display.set_mode((432,786)) 

#vòng lặp
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_play == True:
                bird_y = 0
                bird_y = -5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_play == False:
                game_play = True
                bird_y = 0
                bird_hcn.center = (100,286)
                score = 0
        if(event.type == spawnpipe):
            pipe_list.extend(create_pipe())
        if(event.type == bird_flap):
            if bird_id < 2:
                bird_id += 1
            else:
                bird_id = 0
            bird, bird_hcn = bird_animation()
            
    screen.blit(bg,(0,0))   
    
    #xử lý ống
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)
    
    #xử lý sàn
    fl_x -= 1
    screen.blit(fl,(fl_x,600))
    screen.blit(fl,(fl_x+432,600))
    if fl_x == -432:
        fl_x = 0
    
    if game_play:
    #xử lý bird
        rotated_bird = rotate_bird(bird) #xoay con chim
        screen.blit(rotated_bird , bird_hcn)
        bird_y += p
        bird_hcn.centery += bird_y
        score += 0.01  
        if score > high_score:
            high_score = score
        score_view()
        score_sound_count-=1
        if score_sound_count <= 0:
            score_sound.play()
            score_sound_count = 100
        game_play = check_vacham(pipe_list ) 
    else:
        screen.blit(screen_kt,screen_kt_hcn) 
        score_view()
    pygame.display.update()
        