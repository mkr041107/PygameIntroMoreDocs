import pygame, math 
from sys import exit 


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()
spaceship = pygame.image.load('images/spaceship.png').convert_alpha() 
spaceship_rect = spaceship.get_rect(midleft = screen_rect.midleft)
spaceship_speed = 0
spaceship_angle = 0 
spaceship_rotation_speed = 0 
                                                                                
asteroid = pygame.image.load('images/asteroid.png').convert_alpha()
asteroid_rect = asteroid.get_rect(midright = screen_rect.midright)

asteroid_list = [(asteroid, asteroid_rect)] # list of <asteroid (surface), rect>

projectile = pygame.Surface((16,4))
projectile_rect = projectile.get_rect(midleft = spaceship_rect.midright) 
projectile.fill('white') 
projectile_speed = 8 

projectile_list = [(projectile, projectile_rect)] # list of <projectile (surface), rect>

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
            elif event.key == pygame.K_RIGHT: 
                spaceship_rotation_speed = -10
            elif event.key == pygame.K_LEFT:
                spaceship_rotation_speed = 10 
        
        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_UP:
                spaceship_speed = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT: 
                spaceship_rotation_speed = 0  

    if asteroid and projectile: # ensure asteroid and projectile still exists
        if asteroid_rect.colliderect(projectile_rect):
            pos_list = [asteroid_rect.topleft, asteroid_rect.topright, asteroid_rect.bottomleft, asteroid_rect.bottomright] # positions for smaller asteroids
            projectile_list.pop() # destroy projectile
            projectile = None
            projectile_rect = None
            asteroid_list.pop() # remove original asteroid from list
            asteroid_rect
            for p in pos_list: # create 4 new asteroids and add to ateroid list
                new_asteroid = pygame.transform.scale(asteroid,(asteroid_rect.width//2,asteroid_rect.height//2))
                new_asteroid_rect = new_asteroid.get_rect(center = p)
                asteroid_list.append((new_asteroid,new_asteroid_rect))
            asteroid = None #destroy asteroid artifacts
            asteroid_rect = None

    spaceship_angle = (spaceship_angle + spaceship_rotation_speed) % 360 
    
    rotated_spaceship = pygame.transform.rotate(spaceship, spaceship_angle) 
    rotated_spaceship_rect = rotated_spaceship.get_rect(center=spaceship_rect.center) 
                                                                                      

    screen.fill((0,0,0)) 
    screen.blit(rotated_spaceship, rotated_spaceship_rect)

    for p in projectile_list: # loop through projectile list draw and move projectile
        screen.blit(p[0], p[1])
        p[1].x += projectile_speed 

    for a in asteroid_list: # loop through and draw asteroids in list
        screen.blit(a[0], a[1])

    screen.blit(score_display, score_display_rect) 
    spaceship_rect.y -= math.sin(math.radians(spaceship_angle))*spaceship_speed 
    spaceship_rect.x += math.cos(math.radians(spaceship_angle))*spaceship_speed 

    clock.tick(30) 
    pygame.display.update()


