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


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# Set the title of the window
pygame.display.set_caption('Hacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
background = background.convert()
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


class Game:
    start_time = 0

    def __init__(self):
        logger.info("Creating new game...")

        self.all_sprites_list = pygame.sprite.RenderPlain()
        self.dot_list = pygame.sprite.RenderPlain()
        self.ghost_list = pygame.sprite.RenderPlain()
        self.player_collide = pygame.sprite.RenderPlain()

        self.walls = setupRoomOne(self.all_sprites_list)
        self.gate = setupGate(self.all_sprites_list)

        # Load the ghost directions from the file
        logger.debug("Loading directions file...")
        directions = json.load(open("directions.json", "r"))

        # Create sprites
        self.player = Player(w, p_h, "images/Trollman.png")
        self.all_sprites_list.add(self.player)
        self.player_collide.add(self.player)

        self.blinky = Ghost(w, b_h, "images/Blinky.png")
        self.blinky.directions = directions["blinky"]
        self.all_sprites_list.add(self.blinky)
        self.ghost_list.add(self.blinky)

        self.pinky = Ghost(w, m_h, "images/Pinky.png")
        self.pinky.directions = directions["pinky"]
        self.all_sprites_list.add(self.pinky)
        self.ghost_list.add(self.pinky)

        self.inky = Ghost(i_w, m_h, "images/Inky.png")
        self.inky.directions = directions["inky"]
        self.all_sprites_list.add(self.inky)
        self.ghost_list.add(self.inky)

        self.clyde = Ghost(c_w, m_h, "images/Clyde.png")
        self.clyde.directions = directions["clyde"]
        self.all_sprites_list.add(self.clyde)
        self.ghost_list.add(self.clyde)

        self.draw_grid()

    def draw_grid(self):
        for row in range(19):
            for column in range(19):
                if ((row == 7 or row == 8) and
                        (column == 8 or column == 9 or column == 10)):
                    continue
                else:
                    dot = Dot(yellow, 4, 4)

                    # Set a random location for the block
                    dot.rect.x = (30*column+6)+26
                    dot.rect.y = (30*row+6)+26

                    b_collide = pygame.sprite.spritecollide(
                        dot, self.walls, False)
                    p_collide = pygame.sprite.spritecollide(
                        dot, self.player_collide, False)
                    if b_collide:
                        continue
                    elif p_collide:
                        continue
                    else:
                        # Add the block to the list of objects
                        self.dot_list.add(dot)
                        self.all_sprites_list.add(dot)

    def elapsed_time(self):
        return round((pygame.time.get_ticks() - self.start_time) / 1000, 1)

    def do_update(self):
        # Update player location
        self.player.update(self.walls, self.gate)

        # Update ghost locations
        self.pinky.changespeed(False)
        self.pinky.changespeed(False)
        self.pinky.update(self.walls, False)

        self.blinky.changespeed(False)
        self.blinky.changespeed(False)
        self.blinky.update(self.walls, False)

        self.inky.changespeed(False)
        self.inky.changespeed(False)
        self.inky.update(self.walls, False)

        self.clyde.changespeed("clyde")
        self.clyde.changespeed("clyde")
        self.clyde.update(self.walls, False)

        # Get a list of the dots that the player has hit
        dots_hit = pygame.sprite.spritecollide(self.player, self.dot_list, True)

        if len(dots_hit) > 0:
            self.player.score += 1

    def do_draw(self):
        # Clear the screen
        screen.fill(black)

        # Draw all of the sprites and walls
        self.walls.draw(screen)
        self.gate.draw(screen)
        self.all_sprites_list.draw(screen)
        self.ghost_list.draw(screen)

        # Draw the score text
        score_text = font.render("Score: {}/{}".format(self.player.score,
                                                       len(self.dot_list)),
                                 True, red)
        screen.blit(score_text, [10, 10])

        # Draw the elapsed time
        time_text = font.render("Time: {}".format(self.elapsed_time()), True,
                                red)
        # Draw the elapsed time at the width of the screen minus 10px for
        # padding and minus the width of the text. This gives the effect of
        # aligning the text to the right of the screen.
        screen.blit(time_text,
                    [screen.get_size()[1] - 10 - time_text.get_width(), 10])

    def start(self):
        self.start_time = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.setspeed(-30, 0)
                    if event.key == pygame.K_RIGHT:
                        self.player.setspeed(30, 0)
                    if event.key == pygame.K_UP:
                        self.player.setspeed(0, -30)
                    if event.key == pygame.K_DOWN:
                        self.player.setspeed(0, 30)

            self.do_update()
            self.do_draw()

            # logger.debug("======================================")
            # logger.debug("PINKY: turn = {}, steps = {}".format(self.pinky.turn, self.pinky.steps))
            # logger.debug("BLINKY: turn = {}, steps = {}".format(self.blinky.turn, self.blinky.steps))
            # logger.debug("INKY: turn = {}, steps = {}".format(self.inky.turn, self.inky.steps))
            # logger.debug("CLYDE*: turn = {}, steps = {}".format(self.clyde.turn, self.clyde.steps))

            if self.player.score == len(self.dot_list):
                doNext("Congrats, you won!", 145)

            ghost_collide = pygame.sprite.spritecollide(self.player, self.ghost_list, False)

            if ghost_collide:
                doNext("Game Over!", 235)

            # Partially update the display
            pygame.display.flip()

            clock.tick(10)


current_game = Game()


def doNext(message, left):
    logger.info("Showing message box...")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    # Create a new game and start it
                    current_game = Game()
                    current_game.start()

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
current_game.start()
pygame.quit()
