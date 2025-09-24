import pygame, math 
from sys import exit 

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
game_active = False 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()
def start_game(): 
    global spaceship_acceleration, spaceship_velocity, spaceship_angle, spaceship_rotation_speed, spaceship_rect, asteroid_rect, game_active
    game_active = True
    spaceship_acceleration = 0
    spaceship_velocity = [0,0]
    spaceship_angle = 0
    spaceship_rotation_speed = 0
    spaceship_rect = spaceship.get_rect(center = screen_rect.center)
    asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)

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


start_font = pygame.font.Font(None, 48) # font for button text 
start_text = start_font.render("Start", True, "white", None) # set colors with their name
start_text_rect = start_text.get_rect() # get rect for text surface
start_button = pygame.Surface((start_text_rect.width+10,start_text_rect.height+10)) # create button surface, 10px wider and taller than text surface
start_button_rect = start_button.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)) # get start_button_rect set to center of screen
start_text_rect = start_text.get_rect(center = (start_button_rect.width//2, start_button_rect.height//2)) # set the center of the text rect to the center of the start button 
                                                                                                          # using the start_button_rect's width and height
start_button.fill("#0000FF") # set color with a hexidecimal string "#RRGGBB"
start_button.blit(start_text,start_text_rect) # blit the text_surface onto the button surface
                                              # you won't need to worry about bliting the text again since it's on the button surface
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
            if event.type == pygame.MOUSEBUTTONDOWN: # mouse button down event
                if event.button == 1 and start_button_rect.collidepoint(event.pos): # check if mouse position, event.pos, is in start_button_rect with rect.collidepoint
                    start_game() # call start_game()
        screen.fill((0,128,255)) # Set color by integer values, 0-255
        screen.blit(start_button, start_button_rect)  # Blit Start Button to screen
        
        

    clock.tick(30) 
    pygame.display.update()


