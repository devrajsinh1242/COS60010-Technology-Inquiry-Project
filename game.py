import pygame #import pygame
from pygame.locals import *
import random #import the random function



pygame.init() #initialise the initialise function of pygame
clock = pygame.time.Clock() #allows us to change the FPS of the game
running = True #initialise the running variable for the game
screen_width = 1024 #set the screen width to the size of the BG picture
screen_height = 768 #set the screen height to the size of the BG picture
screen = pygame.display.set_mode((screen_width, screen_height)) #the set_mode attribute draws the screen with width and height
#display the screen with the preset width and height

#load bg picture
bg = pygame.image.load("bg.png")

#load the balloon image
balloon_list = [] #balloon list to store multiple balloon
balloon_img = pygame.image.load("10_balloon.png") #balloon object variable


#draw all the objects together

#keep all the drawing outside of the MAIN GAME LOOP

#def is used to define a function
#then you need to call the function, call it at the end of the main game loop
#

#global turns a variable so that we can change this variable if we need to access in a function and outside the function



#Creating multiple balloons
for balloon in range (5):
    balloon_loc = balloon_img.get_rect()


    balloon_loc[0] = random.randint(100, screen_width - 100) #random X coordinate between 100, and screen width minus the length of the balloon
    balloon_loc[1] = random.randint(-100, screen_height - 100) #random Y coordinate between 10 outside of the screen and the screen height minus the 100
    balloon_list.append(balloon_loc) #update the list of balloons with random positions


#load the pop image
pop = pygame.image.load("10_pop.png")

#load the sound
hit_sound = pygame.mixer.Sound("hit.wav")

#variable for the score
score = 0

#text to show the game score
pygame.font.init()
my_font = pygame.font.SysFont("Roboto", 30) #choose a font from the system

#GAME LOOP - 3 main sections
while running: #all of the events below happen when the game is running

    #SECTION 1 Capturing Events - listening for user input
    for event in pygame.event.get():
        if event.type == QUIT: #if pressing on QUIT, the game quits
            running = False #the game stops running
        
        if event.type == MOUSEBUTTONDOWN: #if the event is mouse clicked
            for balloon in balloon_list: #for balloon in the balloon list
                mouse_pos = pygame.mouse.get_pos() #get the mouse position
                collide = balloon.collidepoint(mouse_pos[0], mouse_pos[1]) #this variable determines if mouse position X&Y are inside the balloon location
                if collide: #if this condition is true
                    score += 1
                    screen.blit(pop, balloon)
                    pygame.display.update()
                    pygame.mixer.Sound(hit_sound).play()
                    clock.tick(7)
                    balloon[1] = screen_height + 10 #a new balloon [inside the list] (location) 'appears' under the screen 10px 
                    balloon[0] = random.randint (100, screen_width - 100) #a random X coordinate minus the balloon width so we can always see the balloon on the screen




    #SECTION 3 Refreshing the screen and start again - redraw a stage and redraw a balloon
    screen.fill("pink")
    screen.blit(bg, [0,0]) #display the background image
    score_text = my_font.render("Your score: " + str(score), False, "black")
    screen.blit(score_text, [20,220]) #draw on the screen object
    
    for balloon in balloon_list:

        screen.blit(balloon_img, [balloon[0], balloon[1]]) #display the balloon with the location

        #SECTION 2 Game Logic - the balooon flies
        balloon[1] -= 5 #1 represents Y coordinates and 0 represent X coordinates
        if balloon[1] < -300: #when the ballon Y coordinates is 300px outside of the height
            score -= 1
            balloon[1] = screen_height + 10 #a new balloon (location) 'appears' under the screen (screen height)+10px 
            balloon[0] = random.randint (100, screen_width - 100) #a random X coordinate minus the balloon width (100px) so we can always see the balloon on the screen

    pygame.display.update() #update the screen with the new images
    
    
    clock.tick(30) #set the FPS for the game - 30 Frame per second

















pygame.quit() #the quit function for pygame