# Pacman in Python with PyGame
# https://github.com/hbokmann/Pacman

import pygame
import json
from logzero import logger
from models.wall import Wall
from models.player import Player
from models.ghost import Ghost
from models.dot import Dot

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

Trollicon = pygame.image.load('images/Trollman.png')
pygame.display.set_icon(Trollicon)


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    logger.debug("Loading walls file...")
    walls = json.load(open("walls.json", "r"))

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


logger.debug("Loading directions file...")
directions = json.load(open("directions.json", "r"))
pinky_directions = directions["pinky"]
blinky_directions = directions["blinky"]
inky_directions = directions["inky"]
clyde_directions = directions["clyde"]

pl = len(pinky_directions)-1
bl = len(blinky_directions)-1
il = len(inky_directions)-1
cl = len(clyde_directions)-1

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Hacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)


clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# default locations for Pacman and monstas
w = 303-16  # Width
p_h = (7*60)+19  # Pacman height
m_h = (4*60)+19  # Monster height
b_h = (3*60)+19  # Binky height
i_w = 303-16-32  # Inky width
c_w = 303+(32-16)  # Clyde width


def startGame():
    logger.info("Starting game...")

    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)
    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    # Create the player paddle object
    Pacman = Player(w, p_h, "images/Trollman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky = Ghost(w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(i_w, m_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(c_w, m_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    # Draw the grid
    for row in range(19):
        for column in range(19):
            if ((row == 7 or row == 8) and
                    (column == 8 or column == 9 or column == 10)):
                continue
            else:
                block = Dot(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30*column+6)+26
                block.rect.y = (30*row+6)+26

                b_collide = pygame.sprite.spritecollide(
                    block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(
                    block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

    bll = len(block_list)
    score = 0
    done = False

    while done is False:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.setspeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.setspeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.setspeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.setspeed(0, 30)

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT:
            #         Pacman.changespeed(30, 0)
            #     if event.key == pygame.K_RIGHT:
            #         Pacman.changespeed(-30, 0)
            #     if event.key == pygame.K_UP:
            #         Pacman.changespeed(0, 30)
            #     if event.key == pygame.K_DOWN:
            #         Pacman.changespeed(0, -30)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        Pacman.update(wall_list, gate)

        returned = Pinky.changespeed(
            pinky_directions, False, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(pinky_directions, False, p_turn, p_steps, pl)
        Pinky.update(wall_list, False)

        returned = Blinky.changespeed(
            blinky_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(blinky_directions, False, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)

        returned = Inky.changespeed(
            inky_directions, False, i_turn, i_steps, il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changespeed(inky_directions, False, i_turn, i_steps, il)
        Inky.update(wall_list, False)

        returned = Clyde.changespeed(
            clyde_directions, "clyde", c_turn, c_steps, cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changespeed(clyde_directions, "clyde", c_turn, c_steps, cl)
        Clyde.update(wall_list, False)

        # See if the Pacman block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Score: "+str(score)+"/"+str(bll), True, red)
        screen.blit(text, [10, 10])

        if score == bll:
            doNext("Congratulations, you won!", 145, all_sprites_list,
                   block_list, monsta_list, pacman_collide, wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(
            Pacman, monsta_list, False)

        if monsta_hit_list:
            doNext("Game Over", 235, all_sprites_list, block_list,
                   monsta_list, pacman_collide, wall_list, gate)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, monsta_list,
           pacman_collide, wall_list, gate):
    logger.info("Showing message box...")

    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    startGame()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)                # alpha level
        w.fill((128, 128, 128))           # this fills the entire surface
        screen.blit(w, (100, 200))    # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


logger.info("Starting hacman!")
startGame()
pygame.quit()
