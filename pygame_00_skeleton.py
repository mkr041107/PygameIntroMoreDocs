import pygame # imports the module

# -- Set up --
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 #Constants for window size
pygame.init() # pygame must be initialized before it can be used

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
''' ^ Creates a window with a pygame surface ^
    The return value is a pygame surface
'''
clock = pygame.time.Clock() # used to manage the timing and frame rate of your game

running = True # flag to keep game running

# -- Main Loop --
while running:

    # Before events

    # --- Handle Events --- (keyboard, mouse, window close, etc.)
    events = pygame.event.get() # gets the current events
    for event in events: # loop through events

        if event.type == pygame.QUIT: # 'x' button of window pressed
            running = False # set running to false
            break # break loop

        elif event.type == pygame.KEYDOWN: # keyboard input event
            if event.key == pygame.K_SPACE: # event will only have a key attribute in keyboard events
                pass # Space button was pressed


    #After events
    # --- Update & Draw ---
    # (game logic, movement, rendering)

    clock.tick(30) # 30 frames per second

    pygame.display.update() # updates the display

pygame.quit() # Quit pygame safely

