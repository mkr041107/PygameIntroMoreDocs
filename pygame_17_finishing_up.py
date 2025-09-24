import pygame
from random import randint
from math import sin, cos, radians, pow, sqrt
from sys import exit 
from time import time

# Idea: improve screen wrapping by dividing the surface when it is at the edge of the screen
#       and make part of the object appear on both sides


#---------- Global Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 
highest_level = 0
game_active = False 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

score_font = pygame.font.SysFont('Aptos', 36, False, False) 
score = 0 
score_display = score_font.render(f"Score: {score}", True, "white", None) 
score_display_rect = score_display.get_rect(topright = screen_rect.topright) 

bg_music = pygame.mixer.Sound("sounds/bg_music.mp3") 
bg_music.set_volume(.5) 
gameover_sound = pygame.mixer.Sound("sounds/gameover_sound.mp3") 
gameover_sound.set_volume(.7)
destruction_sound = pygame.mixer.Sound("sounds/destruction.mp3") 
destruction_sound.set_volume(1)
laser_sound = pygame.mixer.Sound("sounds/laser_sound.mp3") 
laser_sound.set_volume(.7)

#------------ Functions -----------------
def start_game():
    global player_group, obstacle_group, projectile_group, game_active, score, difficulty, difficulty_timer
    projectile_group.empty() # remove all projectiles from group
    obstacle_group.empty() # remove all obstacles from group
    game_active = True
    player_group.sprite.reset() # reset player
    bg_music.play(-1) 
    score = 0 # reset score
    difficulty = 1
    difficulty_timer = time()

#------------- Classes -----------------
class GameObject(pygame.sprite.Sprite): # create base class for game objects for shared functionality
    def __init__(self):
        super().__init__()
        

    def screen_wrap(self): # screen wrap function, makes sprite appear on other side of screen
        if self.rect.bottom < 0:
            self.rect = self.image.get_rect(midtop = (self.rect.centerx, SCREEN_HEIGHT))
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect = self.image.get_rect(midbottom = (self.rect.centerx, 0))
        if self.rect.right < 0:
            self.rect = self.image.get_rect(midleft = (SCREEN_WIDTH, self.rect.y))
        elif self.rect.left > SCREEN_WIDTH:
            self.rect = self.image.get_rect(midright = (0, self.rect.y))

class Player(GameObject): 
    def __init__(self):
        super().__init__() 
        self.original_image = pygame.image.load('images/spaceship.png').convert_alpha() 
        self.image = self.original_image 
        self.rect = self.image.get_rect(center = screen_rect.center) 
        self.mask = pygame.mask.from_surface(self.image)
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
        self.screen_wrap() # add screen wrap
    
    def rotate(self):
        self.angle = (self.angle + self.angular_velocity) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    
    def accelerate(self):
        self.velocityX += cos(radians(self.angle))*self.acceleration
        self.velocityY += sin(radians(self.angle))*self.acceleration

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
    
class Obstacle(GameObject):
    def __init__(self, origin, angle, size = 0, speed = 5, angular_velocity = 5):
        super().__init__()
        self.original_image = pygame.image.load('images/asteroid_16.png').convert_alpha()
        self.scaled_image = pygame.transform.scale_by(self.original_image, pow(2,size))
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = origin)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.angle = angle  # angle for movement
        self.image_angle = 0 # angle for image rotation
        self.angular_velocity = angular_velocity # image roatation velocity
        self.size = size # size of asteroid

    def update(self):
        self.rotate()
        self.move()
        self.screen_wrap() # add screen wrap

    def rotate(self): # rotate asteroid image, using scaled image as the reference image
        self.image_angle = (self.image_angle + self.angular_velocity) % 360
        self.image = pygame.transform.rotate(self.scaled_image, self.image_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self): # move asteroid by 2 dimensional components
        self.rect.x += cos(radians(self.angle))*self.speed
        self.rect.y -= sin(radians(self.angle))*self.speed

    def destroy(self): # spawn obstacles destroy self
        if self.size > 0: self.spawn() # only spawn if size is greater than 0
        self.kill()

    def spawn(self):
        global obstacle_group
        theta = randint(0,359) # get random angle in degrees
        for _ in range(int(pow(2,self.size))): # loop 2^self.size times
            pointX = self.rect.centerx -(sin(radians(theta))*16*pow(2,self.size-1)) # calculate spawn position x
            pointY = self.rect.centery -(cos(radians(theta))*16*pow(2,self.size-1)) # calculate spawn position y
            obstacle_group.add(Obstacle((pointX,pointY), theta, self.size -1, 6 - self.size, randint(-5,5))) # add obstacle 1 size smaller to group
            theta = (theta+(360//pow(2,self.size))) % 360 # increase angle by 2pi divided by 2^self.size
                                                         # size 1: 360/2^1 = 180
                                                         # size 2: 360/2^2 = 90
                                                         # size 3: 360/2^4 = 45

    def move_to_perimeter(self): # move to random point on perimenter
        perimeter = 2*(SCREEN_WIDTH+SCREEN_HEIGHT) # calculat perimeter size
        r = randint(0,perimeter-1)                 # get random value from 0 to perimeter -1
        if r < SCREEN_HEIGHT:                      # if random value is less than screen height, the point is on the left
            point = (0, r)                         # x = 0 for left side of screen, y is r value
            self.rect = self.image.get_rect(midleft = point) # place midleft at r
        elif r < SCREEN_WIDTH + SCREEN_HEIGHT:     # if random value is less than screen height + screen width, the point is on the bottom
            point = (r-SCREEN_HEIGHT, SCREEN_HEIGHT) # y = screen height for bottom of screen, x is r value - screen height
            self.rect = self.image.get_rect(midtop = point) # place midtop at r
        elif r < 2*SCREEN_HEIGHT + SCREEN_WIDTH:   # if random value is less than 2*screen height + screen width, the point is on the right
            point = (SCREEN_WIDTH, r-(SCREEN_WIDTH+SCREEN_HEIGHT)) # x = screen width for right side, y = r - (screen width + screen height)
            self.rect = self.image.get_rect(midright = point) # place mid right at point
        else:                                      # if it reaches here the point is on the top
            point = (r-(2*SCREEN_HEIGHT+SCREEN_WIDTH), 0) # y = 0 for top, x = r - (2 * screen height + screen width)

class Projectile(GameObject): # inherits from game object now
    def __init__(self, center, angle, initial_v): # add spaceships velocity 
        super().__init__()
        self.original_image = pygame.image.load('images/laser.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center = center)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 15 + sqrt(pow(initial_v[0],2) + pow(initial_v[1],2))
        self.angle = angle
        self.start_time = time() 
        self.time_limit = .8
        self.rotate() 

    def update(self):
        if time() - self.start_time >= self.time_limit:
            self.kill()
        self.move()
        self.screen_wrap() # add screen wrap

    def move(self):
        self.rect.x += cos(radians(self.angle))*self.speed
        self.rect.y -= sin(radians(self.angle))*self.speed
    
    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

#-------- Game Active Constants-----------------------
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

obstacle_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()

difficulty = 0 # int for difficulty level
difficulty_timer = time() # timer for incresing difficulty
difficulty_time_increment = 10 # time increment difficulty increases by

level_display = score_font.render(f"Level: {difficulty}", True, "white")
level_display_rect = level_display.get_rect(topleft = (0,0))



#------- Start Screen Constants-------------------------------------

start_font = pygame.font.Font(None, 48) 
instruction_text = start_font.render("Press 's' to start", True, "white", None) # add starting instruction text
instruction_rect = instruction_text.get_rect(midtop = (SCREEN_WIDTH//2,SCREEN_HEIGHT//4))

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
                    projectile_group.add(Projectile(player_group.sprite.rect.center,player_group.sprite.angle,(player_group.sprite.velocityX, player_group.sprite.velocityY)))
                elif event.key == pygame.K_UP or event.key == pygame.K_w: 
                    player_group.sprite.acceleration = 1 
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                    player_group.sprite.angular_velocity = -10
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player_group.sprite.angular_velocity = 10
                
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player_group.sprite.acceleration = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_d: 
                    player_group.sprite.angular_velocity = 0

        if time() - difficulty_timer >= difficulty_time_increment: # if the time increment has passed
            difficulty += 1 # increase difficulty
            difficulty_timer = time() # reset timer

        if len(obstacle_group) < difficulty + 1: #spawn if there are fewer obstacles than the difficulty level
            obstacle = Obstacle((0,0), randint(0,359), randint(0, (difficulty//3 if difficulty < 9 else 3)), randint(2,4), randint(-5,5))
            obstacle.move_to_perimeter()
            obstacle_group.add(obstacle) # add obstacle to group
            
        obstacle_collisions = pygame.sprite.spritecollide(player_group.sprite, obstacle_group, False)
        for obstacle in obstacle_collisions:
             origin_diff = (obstacle.rect.left - player_group.sprite.rect.left, obstacle.rect.top - player_group.sprite.rect.top)
             if player_group.sprite.mask.overlap(obstacle.mask, origin_diff):   
                game_active = False
                bg_music.stop()
                gameover_sound.play() 
                
        projectile_collisions = pygame.sprite.groupcollide(obstacle_group, projectile_group, False, False)
        for obstacle, projectiles in projectile_collisions.items():
            for p in projectiles:
                origin_diff = (p.rect.left - obstacle.rect.left, p.rect.top - obstacle.rect.top)
                if obstacle.mask.overlap(p.mask, origin_diff):
                    obstacle.destroy()
                    p.kill()
                    destruction_sound.play()
                    score += int(pow(2,obstacle.size))
                    break

        screen.fill((0,0,0))

        score_display = score_font.render(f"Score: {score}", True, "white", None)
        score_display_rect = score_display.get_rect(topright = screen_rect.topright)       
        screen.blit(score_display, score_display_rect) 

        level_display = score_font.render(f"Level: {difficulty}", True, "white", None)
        level_display_rect = level_display.get_rect(topleft = (0,0))       
        screen.blit(level_display, level_display_rect) 
        
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
                if event.key == pygame.K_s:
                    start_game()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1 and start_button_rect.collidepoint(event.pos):
                    if start_button_rect.collidepoint(event.pos): 
                        start_game() 
        screen.fill((0,128,255)) 
        screen.blit(instruction_text, instruction_rect)
        screen.blit(start_button, start_button_rect)

        if score: # display score on start/gameover screen
            score_display = score_font.render(f"Your score: {score}", True, "white", None) # update score text 
            score_display_rect = score_display.get_rect(midtop = (start_button_rect.midbottom[0], start_button_rect.midbottom[1] + 20)) # update score rect
            screen.blit(score_display, score_display_rect)  
        
    clock.tick(30) 
    pygame.display.update()


