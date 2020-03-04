# Pacman in Python with PyGame
# https://github.com/hbokmann/Pacman

import pygame
import json
from logzero import logger
from models.wall import Wall
from models.player import Player
from models.ghost import Ghost
from models.dot import Dot
import scoring

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
font = pygame.font.Font("OverpassMono-Regular.ttf", 24)
small_font = pygame.font.Font("OverpassMono-Regular.ttf", 16)

# default locations for Pacman and monstas
width = 303-16  # Width
player_height = (7*60)+19  # Pacman height

ghost_starting_x = 303 - 16
ghost_starting_y = 303 - 96


class Game:
    start_time = 0
    max_score = None

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
        self.player = Player(width, player_height, "images/Trollman.png")
        self.all_sprites_list.add(self.player)
        self.player_collide.add(self.player)

        self.blinky = Ghost(ghost_starting_x, ghost_starting_y,
                            "images/Blinky.png", "blinky", self.player)
        self.blinky.directions = directions["blinky"]
        self.all_sprites_list.add(self.blinky)
        self.ghost_list.add(self.blinky)

        self.pinky = Ghost(ghost_starting_x, ghost_starting_y,
                           "images/Pinky.png", "pinky", self.player)
        self.pinky.directions = directions["pinky"]
        self.all_sprites_list.add(self.pinky)
        self.ghost_list.add(self.pinky)

        self.inky = Ghost(ghost_starting_x, ghost_starting_y,
                          "images/Inky.png", "inky", self.player)
        self.inky.directions = directions["inky"]
        self.all_sprites_list.add(self.inky)
        self.ghost_list.add(self.inky)

        self.clyde = Ghost(ghost_starting_x, ghost_starting_y,
                           "images/Clyde.png", "clyde", self.player)
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
                    dot = Dot(green, 4, 4)

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

        self.max_score = len(self.dot_list)

    def elapsed_time(self):
        return round((pygame.time.get_ticks() - self.start_time) / 1000, 1)

    def do_update(self):
        # Update player location
        self.player.update(self.walls, self.gate)

        # Update ghost locations
        self.pinky.changespeed(self.walls)
        self.pinky.update(self.walls, False)

        self.blinky.changespeed(self.walls)
        self.blinky.update(self.walls, False)

        self.inky.changespeed(self.walls)
        self.inky.update(self.walls, False)

        self.clyde.changespeed(self.walls)
        self.clyde.update(self.walls, False)

        # Get a list of the dots that the player has hit
        dots_hit = pygame.sprite.spritecollide(self.player, self.dot_list,
                                               True)

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
        score_text = font.render("Score: {}".format(self.player.score), True,
                                 red)
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
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.setspeed(-30, 0)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.setspeed(30, 0)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.setspeed(0, -30)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.setspeed(0, 30)

            self.do_update()
            self.do_draw()

            if self.player.score == self.max_score:
                show_message("Congrats, you won!", score=self.player.score,
                             time=self.elapsed_time())
                return

            ghost_collide = pygame.sprite.spritecollide(self.player,
                                                        self.ghost_list, False)

            if ghost_collide:
                show_message("Game Over!", score=self.player.score,
                             time=self.elapsed_time())
                return

            # Partially update the display
            pygame.display.flip()

            clock.tick(15)


current_game = Game()


def user_input(prompt):
    logger.info("Getting user input...")
    output = ""

    while True:
        event = pygame.event.poll()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)

            if len(key) == 1:
                output += key
            elif key == "backspace":
                output = output[:len(output) - 1]
            elif key == "space":
                output += " "
            elif event.key == pygame.K_RETURN:
                break

        w = pygame.Surface((screen.get_size()[0], 200))
        w.fill((128, 128, 128))
        screen.blit(w, (0, 200))

        prompt_text = font.render(prompt, True, white)
        screen.blit(prompt_text, [20, 233])

        input_text = font.render(output.upper(), True, white)
        screen.blit(input_text, [20, 263])

        pygame.display.flip()

        clock.tick()

    return output


def ask_question(question, message):
    logger.info("Asking question...")

    while True:
        event = pygame.event.poll()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)

            if key == "y":
                return True
            elif key == "n":
                return False

        w = pygame.Surface((screen.get_size()[0], 200))
        w.fill((128, 128, 128))
        screen.blit(w, (0, 200))

        text = font.render(message, True, white)
        screen.blit(text, [20, 233])

        question_text = small_font.render(question, True, white)
        screen.blit(question_text, [20, 263])

        text2 = small_font.render("Y/N", True, white)
        screen.blit(text2, [20, 283])

        pygame.display.flip()

        clock.tick()


def show_message(message, score=None, time=None):
    if score is not None and time is not None:
        name = user_input("Name:").strip()
        school = user_input("School:").strip()
        logger.debug("Scoreboard info: {} from {}".format(name.upper(),
                                                          school.upper()))

        if len(name) > 0 and len(school) > 0:
            scoring.add_score(name, score, time, school)

    logger.info("Showing message box...")

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_RETURN:
                    waiting = False

        # Grey background
        w = pygame.Surface((screen.get_size()[0], 200))
        w.fill((128, 128, 128))
        screen.blit(w, (0, 200))

        # Won or lost
        message_text = font.render(message, True, white)
        screen.blit(message_text, [20, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [20, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [20, 333])

        pygame.display.flip()

        clock.tick(10)

    # Create a new game and start it
    current_game = Game()
    current_game.start()


logger.info("Starting hacman!")
show_message("Welcome to Hacman!")
current_game.start()
pygame.quit()
