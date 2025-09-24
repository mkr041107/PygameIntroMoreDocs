import pygame, math 
from sys import exit 

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
game_active = False 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()
bg_music = pygame.mixer.Sound("sounds/bg_music.mp3") # add background music
bg_music.set_volume(.5) # set background music volume
gameover_sound = pygame.mixer.Sound("sounds/gameover_sound.mp3") # add gameover sound
gameover_sound.set_volume(.7)
destruction_sound = pygame.mixer.Sound("sounds/destruction.mp3") # add destruction sound
destruction_sound.set_volume(.7)
laser_sound = pygame.mixer.Sound("sounds/laser_sound.mp3") # add laser sound
laser_sound.set_volume(.7)

def start_game(): # function for starting/resetting the game
    global spaceship_acceleration, spaceship_velocity, spaceship_angle, spaceship_rotation_speed, spaceship_rect, asteroid_rect, game_active
    game_active = True
    spaceship_acceleration = 0
    spaceship_velocity = [0,0]
    spaceship_angle = 0
    spaceship_rotation_speed = 0
    spaceship_rect = spaceship.get_rect(center = screen_rect.center)
    asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)
    bg_music.play(-1) # -1 to loop forever

#-------- Game Active -----------------------
spaceship = pygame.image.load('images/spaceship.png').convert_alpha() 
spaceship_rect = spaceship.get_rect(center = screen_rect.center)
spaceship_acceleration = 0
spaceship_velocity = [0,0]
spaceship_angle = 0 

spaceship_rotation_speed = 0
spaceship_drag_coefficient = .08 
                                                                                
asteroid = pygame.image.load('images/asteroid.png').convert_alpha()
asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)

asteroid_speed = 5 

score_font = pygame.font.SysFont('Aptos', 36, False, False) 
score = 0 
score_display = score_font.render(f"Score: {score}", True, "white", None) 
score_display_rect = score_display.get_rect(topright = screen_rect.topright) 


#------- Game Start -------------------------------------


start_font = pygame.font.Font(None, 48) 
start_text = start_font.render("Start", True, "white", None) 
start_text_rect = start_text.get_rect() 
start_button = pygame.Surface((start_text_rect.width+50,start_text_rect.height+50)) # increased surface size
start_button_rect = start_button.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)) 
start_text_rect = start_text.get_rect(center = (start_button_rect.width//2, start_button_rect.height//2)) 
start_button.fill("#0080FF") #Fill surface with background color
border_w = 3 # width for button border                                                  
pygame.draw.ellipse(start_button,"#FFFFFF",(0,0,start_button_rect.w,start_button_rect.h))  # draw white elipse to first to be a border
pygame.draw.ellipse(start_button,"#0000FF",(border_w,border_w,start_button_rect.w-border_w*2,start_button_rect.h-border_w*2)) # draw blue elipse for button bg, rect adjusted by border value
start_button.blit(start_text,start_text_rect) 
                                              
#--------- Main Loop ------------------------------- 

clock = pygame.time.Clock() 


while True:
    if game_active:                       
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() 
                exit() 

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    laser_sound.play() # play laser sound
                    pass 
                elif event.key == pygame.K_UP: 
                    spaceship_acceleration = 1 
                elif event.key == pygame.K_RIGHT: 
                    spaceship_rotation_speed = -10
                elif event.key == pygame.K_LEFT:
                    spaceship_rotation_speed = 10
                
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_UP:
                    spaceship_acceleration = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT: 
                    spaceship_rotation_speed = 0

        if spaceship_rect.colliderect(asteroid_rect): 
            game_active = False
            bg_music.stop() # stop background music
            gameover_sound.play() # play game over sound when hit

        spaceship_angle = (spaceship_angle + spaceship_rotation_speed) % 360 
        
        rotated_spaceship = pygame.transform.rotate(spaceship, spaceship_angle) 
        rotated_spaceship_rect = rotated_spaceship.get_rect(center=spaceship_rect.center) 
                                                                                        

        screen.fill((0,0,0)) 
        screen.blit(rotated_spaceship, rotated_spaceship_rect)
        screen.blit(asteroid, asteroid_rect)
        asteroid_rect.x -= asteroid_speed 
        screen.blit(score_display, score_display_rect) 
        spaceship_velocity[0] += math.cos(math.radians(spaceship_angle))*spaceship_acceleration 
        spaceship_velocity[1] += math.sin(math.radians(spaceship_angle))*spaceship_acceleration
        spaceship_velocity[0] -= spaceship_velocity[0]*spaceship_drag_coefficient
        spaceship_velocity[1] -= spaceship_velocity[1]*spaceship_drag_coefficient 
        spaceship_rect.x += spaceship_velocity[0]
        spaceship_rect.y -= spaceship_velocity[1]
    
    else: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1 and start_button_rect.collidepoint(event.pos):
                    if start_button_rect.collidepoint(event.pos): 
                        start_game() 
        screen.fill((0,128,255)) 
        screen.blit(start_button, start_button_rect)  
        pygame.draw.line(screen, "white", (0,0), pygame.mouse.get_pos(),3) # draw line from top left to cursor
        
        

    clock.tick(30) 
    pygame.display.update()


