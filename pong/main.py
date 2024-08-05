import pygame, sys, random

#ruch piłki
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    #player score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
    #opponent score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(loose_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()
 
    #kolizja pilki z paletka gracza
    if ball.colliderect(player) and ball_speed_x > 0: #sprawdza czy nastapila kolizja
        pygame.mixer.Sound.play(pong_sound)  
        if abs(ball.right - player.left) < 10:  #sprawdza z ktroej strony
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
    #kolizja pilki z przeciwnikiem
    if  ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:  #sprawdza z ktroej strony
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1

#ruch gracza
def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >=screen_height:
        player.bottom = screen_height

#ruch przeciwnik
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

#reset pilki
def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()  #bierzemy czas
    ball.center = (screen_width/2, screen_height/2)  

    if current_time - score_time < 700:
        number_three = game_font.render("3",False,yellow)
        screen.blit(number_three,(screen_width/2 - 7, screen_height/2 + 30))
    
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2",False,yellow)
        screen.blit(number_two,(screen_width/2 - 7, screen_height/2 + 30))   
    
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1",False,yellow)
        screen.blit(number_one,(screen_width/2 - 7, screen_height/2 + 30))  
    
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0    # jezeli czas jest mniejszy niz 2.1s to kulka sie nie rusza
    
    else:
        ball_speed_y = 5 * random.choice((1,-1))   # jak jest wiekszy to pilka leci w randomowym kierunku
        ball_speed_x = 5 * random.choice((1,-1))
        score_time = None


#general setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

#setup okienka
screen_width = 720
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

#rectangle 
ball = pygame.Rect(screen_width/2 - 10,screen_height/2 - 10, 17,17)
player =  pygame.Rect(screen_width - 20,screen_height/2 - 70, 10,140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

#kolorki
bg_color = pygame.Color(41, 43, 43)
green = pygame.Color(6, 120, 10)
yellow = pygame.Color(204, 250, 0)

#predkosci 
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))
player_speed = 0
opponent_speed = 5

#tekst zmienne
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 25)

#sounds
pong_sound = pygame.mixer.Sound("odbicie.mp3")
score_sound = pygame.mixer.Sound("success.mp3")
loose_sound = pygame.mixer.Sound("loose.mp3")

#timer
score_time = True

#main loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 5
            if event.key == pygame.K_UP:
                player_speed -= 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 5
            if event.key == pygame.K_UP:
                player_speed += 5

    #logika
    ball_animation()
    player_animation()
    opponent_ai()

    

    #visuals
    screen.fill(bg_color)   #sam dol ekranu
    pygame.draw.rect(screen,green,player)
    pygame.draw.rect(screen,green,opponent)
    pygame.draw.ellipse(screen,green,ball)
    pygame.draw.aaline(screen, green, (screen_width/2,0), (screen_width/2,screen_height))  # na samej gorze ekranu
    
    
    if score_time:
        ball_restart()

    #punkty gracz
    player_text = game_font.render(f"{player_score}", False, yellow)
    screen.blit(player_text,(373,10))

    #punkty przeciwnik
    opponent_text = game_font.render(f"{opponent_score}", False, yellow)
    screen.blit(opponent_text,(335,10))

    #ograniczenie do 60 odswierzen na sekunde
    pygame.display.flip()
    clock.tick(60)




