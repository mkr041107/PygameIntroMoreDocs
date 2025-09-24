import pygame
from sys import exit 


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()
spaceship = pygame.image.load('images/spaceship.png').convert_alpha() 
spaceship_rect = spaceship.get_rect(midleft = screen_rect.midleft)
spaceship_speed = 0
                                                                                
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

        elif event.type == pygame.KEYDOWN: # key is pressed event 
            if event.key == pygame.K_SPACE: #compare key
                pass 
            elif event.key == pygame.K_UP: # set spaceship speed to 10
                spaceship_speed = 10
        
        elif event.type == pygame.KEYUP: # key is released
            if event.key == pygame.K_UP:
                spaceship_speed = 0       # set spaceship speed to 0

    
    if asteroid_rect.colliderect(projectile_rect): 
        print("Projectile Asteroid Collision")

    screen.fill((0,0,0)) 
    screen.blit(spaceship, spaceship_rect) 
    screen.blit(projectile, projectile_rect) 
    screen.blit(asteroid, asteroid_rect) 
    screen.blit(score_display, score_display_rect) 
    projectile_rect.x += projectile_speed 
    spaceship_rect.x += spaceship_speed # decrement speaceship_rect by spaceship speed

    clock.tick(30) 
    pygame.display.update()


