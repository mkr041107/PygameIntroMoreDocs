import pygame, math 
from sys import exit 
from time import time

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
game_active = False 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
screen_rect = screen.get_rect()
bg_music = pygame.mixer.Sound("sounds/bg_music.mp3") 
bg_music.set_volume(.5) 
gameover_sound = pygame.mixer.Sound("sounds/gameover_sound.mp3") 
gameover_sound.set_volume(.7)
destruction_sound = pygame.mixer.Sound("sounds/destruction.mp3") 
destruction_sound.set_volume(1)
laser_sound = pygame.mixer.Sound("sounds/laser_sound.mp3") 
laser_sound.set_volume(.7)

def start_game():
    global player_group, obstacle_group, projectile_group, game_active
    projectile_group.empty()
    game_active = True
    player_group.sprite.reset()
    obstacle_group.empty()
    obstacle_group.add(Obstacle(screen_rect.midright))
    bg_music.play(-1) 

class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('images/spaceship.png').convert_alpha() 
        self.image = self.original_image 
        self.rect = self.image.get_rect(center = screen_rect.center) 
        self.mask = pygame.mask.from_surface(self.image) # add mask for detecting pixel perfect collision
        self.acceleration = 0
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.angular_velocity = 0
        self.drag_coefficient = 0.08

    def update(self): 
        self.rotate()
        self.accelerate()
        self.apply_drag()
        self.move()
    
    def rotate(self):
        self.angle = (self.angle + self.angular_velocity) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image) # set mask after rotating
    
    def accelerate(self):
        self.velocityX += math.cos(math.radians(self.angle))*self.acceleration
        self.velocityY += math.sin(math.radians(self.angle))*self.acceleration

    def apply_drag(self):
        self.velocityX -= self.velocityX*self.drag_coefficient
        self.velocityY -= self.velocityY*self.drag_coefficient

    def move(self):
        self.rect.x += self.velocityX
        self.rect.y -= self.velocityY

    def reset(self): 
        self.acceleration = 0
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.angular_velocity = 0
        self.image = self.original_image
        self.rect = self.image.get_rect(center = screen_rect.center) 
    
class Obstacle(pygame.sprite.Sprite): 
    def __init__(self, center):
        super().__init__()
        self.original_image = pygame.image.load('images/asteroid.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center = center)
        self.mask = pygame.mask.from_surface(self.image) # add mask for pixel perfect collision
        self.speed = 5

    def move(self):
        self.rect.x -= self.speed

    def update(self):
        self.move()

class Projectile(pygame.sprite.Sprite): 
    def __init__(self, center, angle):
        super().__init__()
        self.original_image = pygame.image.load('images/laser.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center = center)
        self.speed = 15
        self.angle = angle
        self.start_time = time() 
        self.time_limit = 5
        self.rotate()

    def update(self):
        if time() - self.start_time >= self.time_limit:
            self.kill()
        self.move()

    def move(self):
        self.rect.x += math.cos(math.radians(self.angle))*self.speed
        self.rect.y -= math.sin(math.radians(self.angle))*self.speed
    
    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

#-------- Game Active -----------------------
player_group = pygame.sprite.GroupSingle() 
player_group.add(Player()) 

obstacle_group = pygame.sprite.Group() 
obstacle_group.add(Obstacle(screen_rect.midright))

projectile_group = pygame.sprite.Group()
                                                                                

score_font = pygame.font.SysFont('Aptos', 36, False, False) 
score = 0 
score_display = score_font.render(f"Score: {score}", True, "white", None) 
score_display_rect = score_display.get_rect(topright = screen_rect.topright) 


#------- Game Inactive -------------------------------------


start_font = pygame.font.Font(None, 48) 
start_text = start_font.render("Start", True, "white", None) 
start_text_rect = start_text.get_rect() 
start_button = pygame.Surface((start_text_rect.width+50,start_text_rect.height+50)) 
start_button_rect = start_button.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)) 
start_text_rect = start_text.get_rect(center = (start_button_rect.width//2, start_button_rect.height//2)) 
start_button.fill("#0080FF") 
border_w = 3 
pygame.draw.ellipse(start_button,"#FFFFFF",(0,0,start_button_rect.w,start_button_rect.h))  
pygame.draw.ellipse(start_button,"#0000FF",(border_w,border_w,start_button_rect.w-border_w*2,start_button_rect.h-border_w*2)) 
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
                    laser_sound.play() 
                    projectile_group.add(Projectile(player_group.sprite.rect.center,player_group.sprite.angle))
                elif event.key == pygame.K_UP: 
                    player_group.sprite.acceleration = 1 
                elif event.key == pygame.K_RIGHT: 
                    player_group.sprite.angular_velocity = -10
                elif event.key == pygame.K_LEFT:
                    player_group.sprite.angular_velocity = 10
                
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_UP:
                    player_group.sprite.acceleration = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT: 
                    player_group.sprite.angular_velocity = 0

        obstacle_collisions = pygame.sprite.spritecollide(player_group.sprite, obstacle_group, False) # -> List<Obstacles>
        for obstacle in obstacle_collisions:
            diffy = obstacle.rect.top - player_group.sprite.rect.top # calculating the y offset 
            diffx = obstacle.rect.left - player_group.sprite.rect.left # calculating the x offset
            origin_diff = (diffx, diffy) # offset coordinate pair
            if player_group.sprite.mask.overlap(obstacle.mask, origin_diff): # check if masks overlap
                game_active = False
                bg_music.stop()
                gameover_sound.play()



        if pygame.sprite.groupcollide(obstacle_group, projectile_group, True, True):
            destruction_sound.play() 
            score += 1

        screen.fill((0,0,0))        
        score_display = score_font.render(f"Score: {score}", True, "white", None)
        score_display_rect = score_display.get_rect(topright = screen_rect.topright)
        screen.blit(score_display, score_display_rect) 
        
        player_group.update()  
        player_group.draw(screen) 

        obstacle_group.update() 
        obstacle_group.draw(screen) 

        projectile_group.update()
        projectile_group.draw(screen)

    
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
        
        

    clock.tick(30) 
    pygame.display.update()


