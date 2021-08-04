# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 20:16:56 2021

@author: Julia
"""
import pygame
import math
import random
from words import words_h

#setup display
pygame.init()
WIDTH, HEIGHT = 800,500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman Game")

#load and resize images
images = []
for i in range(7):
    image = pygame.image.load("h_"+str(i)+".png")
    image = pygame.transform.scale(image, (216,216))
    images.append(image)

#button variables
RADIUS = 20
GAP = 15
letters=[]
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13)/2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP*2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i//13) * (GAP + RADIUS *2))
    letters.append([x,y, chr(A + i), True])

#fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#word selection
def rand_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()
        
#game variables
hangman_status = 0
word = rand_word(words_h)
guessed = []

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)

#setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True
print(word)



def draw():
    win.fill(WHITE)
    #draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    #draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else: 
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400,200))
    
    #draw buttons
    for letter in letters:
        x,y,ltr,visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3)
            text = LETTER_FONT.render(ltr,1,BLACK)
            win.blit(text, (x-text.get_width()/2,y-text.get_height()/2))
        
    win.blit(images[hangman_status], (100,100))
    pygame.display.update()
    
    
def display_message(word,message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text1 = WORD_FONT.render(f"The word was {word}", 1, BLACK)
    text2 = WORD_FONT.render(message, 1, BLACK)
    win.blit(text1, (WIDTH/2 - text1.get_width()/2, HEIGHT/2 -text1.get_height()/2))
    win.blit(text2, (WIDTH/2 - text2.get_width()/2, HEIGHT/2 -text2.get_height()/2 - 50))
    pygame.display.update()
    pygame.time.delay(3000)
    
    
while run:
    clock.tick(FPS)
    
    draw()
    
    for event in pygame.event.get():
        
        #closing down the game
        if event.type == pygame.QUIT:
            run = False
            
        #getting the xy position of the mouse in the window
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x,m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x-m_x)**2 + (y - m_y) **2)
                    if dist <= RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status +=1
    won = True 
                       
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won:
        display_message(word,"You won!")
        break
        
    if hangman_status == 6:
        display_message(word,"You lost!")
        break
    
pygame.quit()