import pygame, math 
from sys import exit 

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()

def start_game(): # function for starting/resetting the game
    global spaceship_acceleration, spaceship_velocity, spaceship_angle, spaceship_rotation_speed, spaceship_rect, asteroid_rect, game_active, screen_rect
    game_active = True
    spaceship_acceleration = 0
    spaceship_velocity = [0,0]
    spaceship_angle = 0
    spaceship_rotation_speed = 0
    spaceship_rect = spaceship.get_rect(center = screen_rect.center)
    asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)

spaceship = pygame.image.load('images/spaceship.png').convert_alpha() 
spaceship_rect = spaceship.get_rect(center = screen_rect.center)
spaceship_acceleration = 0
spaceship_velocity = [0,0]
spaceship_angle = 0 

spaceship_rotation_speed = 0
spaceship_drag_coefficient = .08 # added coefficient of friction
                                                                                
asteroid = pygame.image.load('images/asteroid.png').convert_alpha()
asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)

asteroid_speed = 5 # Set speed for asteroids



score_font = pygame.font.SysFont('Aptos', 36, False, False) 
score = 0 
score_display = score_font.render(f"Score: {score}", True, "white", None) 
score_display_rect = score_display.get_rect(topright = screen_rect.topright) 

game_active = False 
start_font = pygame.font.Font(None, 64) 
start_display = start_font.render("Press Space to begin", True, "white", None) 
start_display_rect = start_display.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)) 
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

        if spaceship_rect.colliderect(asteroid_rect): # if asterod collides with spaceship
            game_active = False # set game active to false

        spaceship_angle = (spaceship_angle + spaceship_rotation_speed) % 360 
        
        rotated_spaceship = pygame.transform.rotate(spaceship, spaceship_angle) 
        rotated_spaceship_rect = rotated_spaceship.get_rect(center=spaceship_rect.center) 
                                                                                        

        screen.fill((0,0,0)) 
        screen.blit(rotated_spaceship, rotated_spaceship_rect)
        screen.blit(asteroid, asteroid_rect)
        asteroid_rect.x -= asteroid_speed # move astroid down
        screen.blit(score_display, score_display_rect) 
        spaceship_velocity[0] += math.cos(math.radians(spaceship_angle))*spaceship_acceleration 
        spaceship_velocity[1] += math.sin(math.radians(spaceship_angle))*spaceship_acceleration
        spaceship_velocity[0] -= spaceship_velocity[0]*spaceship_drag_coefficient
        spaceship_velocity[1] -= spaceship_velocity[1]*spaceship_drag_coefficient 
        spaceship_rect.x += spaceship_velocity[0]
        spaceship_rect.y -= spaceship_velocity[1]
            
    
    else: 
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game()
                    
        screen.blit(start_display, start_display_rect)
        

    clock.tick(30) 
    pygame.display.update()


