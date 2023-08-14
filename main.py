import random
import sys
import pygame
from pygame.locals import *

# global variables

FPS = 32
SCREENWIDTH = 289
SCREENHEIGH = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGH))
GROUNDY = SCREENHEIGH * 0.75
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'gallary/image/bird.png'
BACKGROUND = 'gallary/image/background2.png'
PILLER = 'gallary/image/piller.png'


def welcomescreen():
    playerx = int(SCREENWIDTH/20)
    playery = int((SCREENHEIGH - GAME_SPRITES['bird'].get_height())/2)
    massagex = int((SCREENWIDTH - GAME_SPRITES['massage'].get_height())/1.5)
    massagey = int(SCREENHEIGH*0.25)
    basex = -5
    while True:
        for event in pygame.event.get():
            # if user clicks the cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['bird'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['massage'], (massagex,  massagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
    pass


def iscollide(playerx, playery, upperpillers, lowerpillers):
    if playery > GROUNDY or playery < 0:
        GAME_SOUND['die'].play()
        return True

    for piller in upperpillers:
        pillerhight = GAME_SPRITES['piller'][0].get_height()
        if (playery < pillerhight + piller['y'] and abs(playerx - piller['x']) < GAME_SPRITES['piller'][0].get_width()):
            GAME_SOUND['die'].play()
            return True

    for piller in lowerpillers:
        if ( playery + GAME_SPRITES['bird'].get_height() > piller['y']) and abs(playerx - piller['x']) < GAME_SPRITES['piller'][0].get_width():
            GAME_SOUND['die'].play()
            return True

    return False


def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGH/2)
    basex = -5

    # create 2 pillers for blitting on the screen
    newpiller1 = getrandompiller()
    newpiller2 = getrandompiller()

    # my list of lower pipe
    upperpillers = [
        {'x': SCREENWIDTH+200, 'y': newpiller1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2.3), 'y': newpiller2[0]['y']}
    ]

    # my list of upper pipe
    lowerpillers = [
        {'x': SCREENWIDTH + 200, 'y': newpiller1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2.3), 'y': newpiller2[1]['y']}
    ]

    pillervilX = -4

    playervilY = -9
    playermaxvilY = 10
    playerminvilY = -8
    playeraccY = 1

    playerflapaccv = -8  # velocity while flapping
    playerflapped = False  # it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_UP):
                if playery > 0:
                    playervilY = playerflapaccv
                    playerflapped = True
                    GAME_SOUND['wing'].play()

        crashtest = iscollide(playerx, playery, upperpillers, lowerpillers)  # this function will ruturn true if player is crashed

        if crashtest:
            return

        # checking for score
        playermipos = playerx + GAME_SPRITES['bird'].get_width()/2
        for piller in upperpillers:
            pillermidpos = piller['x'] + GAME_SPRITES['piller'][0].get_width()/2
            if pillermidpos <= playermipos < pillermidpos + 4:
                score += 1
                print(f"your score is {score}")
                GAME_SOUND['point'].play()

        if playervilY < playermaxvilY and not playerflapped:
            playervilY += playeraccY

        if playerflapped:
            playerflapped = False
        playerheight = GAME_SPRITES['bird'].get_height()
        playery = playery + min(playervilY, int(GROUNDY))

        # moveing pipe left
        for upperpiller, lowerpiller in zip(upperpillers, lowerpillers):
            upperpiller['x'] += pillervilX
            lowerpiller['x'] += pillervilX

        # add a new pipe whent he first is about t0 cross the leftmost part of the screen
        if 0 < upperpillers[0]['x'] < 40:
            newpiller = getrandompiller()
            upperpillers.append(newpiller[0])
            lowerpillers.append(newpiller[1])

        # if the pipe is out of the screen, remove it
        if upperpillers[0]['x'] < GAME_SPRITES['piller'][0].get_width():
                upperpillers.pop(0)
                lowerpillers.pop(0)

        # lets blit our sprits
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpiller, lowerpiller in zip(upperpillers, lowerpillers):
            SCREEN.blit(GAME_SPRITES['piller'][0], (upperpiller['x'], upperpiller['y']))
            SCREEN.blit(GAME_SPRITES['piller'][1], (lowerpiller['x'], lowerpiller['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['bird'], (playerx, playery))
        mydigit = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigit:
            width += GAME_SPRITES['number'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in mydigit:
            SCREEN.blit(GAME_SPRITES['number'][digit], (xoffset, SCREENHEIGH*0.12))
            xoffset += GAME_SPRITES['number'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getrandompiller():
    # generate positions of two pipes (one bottem straight and one top rotated ) for blitting on the screen
    pillerhight = GAME_SPRITES['piller'][0].get_height()
    offset = SCREENHEIGH/3
    y2 = offset + random.randrange(0, int(SCREENHEIGH - GAME_SPRITES['base'].get_height() - 0.5*offset))
    pillerx = SCREENWIDTH + 10
    y1 = pillerhight - y2 + offset
    piller = [
        {'x': pillerx, 'y': -y1},  # upper piller
        {'x': pillerx, 'y': y2}   # lower piller
    ]
    return piller


if __name__ == '__main__':
    pygame.init()  # initalize all pygame's module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('game by ADITYA KUMAR')
    GAME_SPRITES['number'] = (
        pygame.transform.scale(pygame.image.load('gallary/image/no0.png').convert_alpha(), (30, 30)),  # convert alpha convert image for game
        pygame.transform.scale(pygame.image.load('gallary/image/no1.png').convert_alpha(), (30, 30)),  # convert image for quick blitting
        pygame.transform.scale(pygame.image.load('gallary/image/no2.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no3.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no4.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no5.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no6.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no7.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no8.png').convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load('gallary/image/no9.png').convert_alpha(), (30, 30)),
    )

    GAME_SPRITES['massage'] = pygame.transform.scale(pygame.image.load('gallary/image/message.png').convert_alpha(), (205, 200))  # (width,height)
    GAME_SPRITES['base'] = pygame.transform.scale(pygame.image.load('gallary/image/base.png').convert_alpha(), (350, 200))
    GAME_SPRITES['piller'] = (pygame.transform.scale(pygame.transform.rotate(pygame.image.load(PILLER).convert_alpha(), 180), (40,500)), pygame.transform.scale(pygame.image.load(PILLER).convert_alpha(), (40,500)))
    GAME_SPRITES['background'] = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (1000, 511))
    GAME_SPRITES['bird'] = pygame.transform.scale(pygame.image.load(PLAYER).convert_alpha(), (60, 45))

    # game sound

    GAME_SOUND['die'] = pygame.mixer.Sound('gallary/audio/die.mp3')
    GAME_SOUND['hit'] = pygame.mixer.Sound('gallary/audio/hit.mp3')
    GAME_SOUND['point'] = pygame.mixer.Sound('gallary/audio/point.mp3')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('gallary/audio/swoosh.mp3')
    GAME_SOUND['wing'] = pygame.mixer.Sound('gallary/audio/wing.mp3')

    while True:
        welcomescreen()  # Show welcome screen to the player until he presses a button
        maingame()    # This is the main game function
