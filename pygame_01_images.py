import pygame
from sys import exit #sys exit to escape program


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

spaceship = pygame.image.load('images/spaceship.png').convert_alpha() # create image surface from imported images
asteroid = pygame.image.load('images/asteroid.png').convert_alpha() # create image surface for asteroid
projectile = pygame.Surface((16,4)) # create surface of 16 width, 4 height
projectile.fill('white') # fill surface with white color
pygame.font.Font()
font = pygame.font.SysFont('Aptos', 36, False, False) # create a font
score = 0 # score value
score_display = font.render(f"Score: {score}", True, "white", None) #create surface with text 

clock = pygame.time.Clock() 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit() 
            exit() #call exit to escape program

        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: 
                pass 

    screen.blit(spaceship, (32,(SCREEN_HEIGHT//2)-16)) # blit space ship image surface to screen
    screen.blit(projectile, ((SCREEN_WIDTH//2)-8,(SCREEN_HEIGHT//2)-2)) # blit color surface to screen
    screen.blit(asteroid, (SCREEN_WIDTH-64, (SCREEN_HEIGHT//2)-32)) # blit asteroid image surface to screen
    screen.blit(score_display, (0,0)) # blit text to screen
    

    clock.tick(30) 
    pygame.display.update()


