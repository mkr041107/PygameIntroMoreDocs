import pygame, math # math for sin and cos
from sys import exit 


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()
spaceship = pygame.image.load('images/spaceship.png').convert_alpha() 
spaceship_rect = spaceship.get_rect(midleft = screen_rect.midleft)
spaceship_speed = 0
spaceship_angle = 0 # Added initial angle to rotate space ship
spaceship_rotation_speed = 0 # Spaceship rotation speed causes spaceship to rotate
                                                                                
asteroid = pygame.image.load('images/asteroid.png').convert_alpha()
asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)

projectile = pygame.Surface((16,4))
projectile_rect = projectile.get_rect(midleft = spaceship_rect.midright) 
projectile.fill('white') 
projectile_speed = 8 

score_font = pygame.font.SysFont('Aptos', 36, False, False) 
score = 0 
score_display = score_font.render(f"Score: {score}", True, "white", None) 
score_display_rect = score_display.get_rect(topright = screen_rect.topright) 
                                                                         

clock = pygame.time.Clock() 


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit() 
            exit() 

        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: 
                pass 
            elif event.key == pygame.K_UP: 
                spaceship_speed = 10
            elif event.key == pygame.K_RIGHT: # rotate clock wise
                spaceship_rotation_speed = -10
            elif event.key == pygame.K_LEFT:
                spaceship_rotation_speed = 10 # rotate counter clock wise
        
        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_UP:
                spaceship_speed = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT: #check if either key is released
                spaceship_rotation_speed = 0  # stop rotation

    
    if asteroid_rect.colliderect(projectile_rect): 
        print("Projectile Asteroid Collision")

    spaceship_angle = (spaceship_angle + spaceship_rotation_speed) % 360 # add rotation_speed to angle '% 360' keeps angle in range
    # Rotate the surface
    rotated_spaceship = pygame.transform.rotate(spaceship, spaceship_angle) # create new rotated surface
    rotated_spaceship_rect = rotated_spaceship.get_rect(center=spaceship_rect.center) # get rotated surface's rect
                                                                                      # set the center to original rect center

    screen.fill((0,0,0)) 
    screen.blit(rotated_spaceship, rotated_spaceship_rect) # blit the rotated surface with the rotated rect instead of the original
    screen.blit(projectile, projectile_rect) 
    screen.blit(asteroid, asteroid_rect) 
    screen.blit(score_display, score_display_rect) 
    projectile_rect.x += projectile_speed 
    spaceship_rect.y -= math.sin(math.radians(spaceship_angle))*spaceship_speed # move the space ship by taking the cos and sin of the angle 
    spaceship_rect.x += math.cos(math.radians(spaceship_angle))*spaceship_speed # subtracting the sin from y, and the cos from x

    clock.tick(30) 
    pygame.display.update()


