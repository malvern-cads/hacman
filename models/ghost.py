from models.player import Player
import pygame
import random


# Inheritime Player klassist
class Ghost(Player):
    turn = 0
    steps = 0
    directions = []
    # n e s w
    possible_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    unit_direction = 15
    hypo_unit_direction = 30
    direction = None

    def __init__(self, x, y, image, name, player):
        Player.__init__(self, x, y, image)
        self.name = name
        self.player = player

    # Change the speed of the ghost
    def changespeed(self, walls):
        if self.direction is None:
            self.direction = random.choice(self.possible_directions)

        cx = self.rect.left
        cy = self.rect.top

        nx = cx + self.direction[0] * self.unit_direction
        ny = cy + self.direction[1] * self.unit_direction

        possible = self.get_junction(walls, cx, cy)

        if self.direction in possible and len(possible) >= 3:
            # if self.name == "blinky":
            #     print("change blink", self.direction)
            #     best = None
            #     shortest = 1000000
            #     px = self.player.rect.left
            #     py = self.player.rect.top
            #     for direction in possible:
            #         manhat = abs(cx + self.unit_direction * direction[0] - px) + abs(cy + self.unit_direction * direction[1] - py)
            #         print(manhat)
            #         if manhat < shortest:
            #             shortest = manhat
            #             best = direction
            #     self.direction = best


            # else:
            #     self.direction = random.choice(possible)
            self.direction = random.choice(possible)
        # corner time
        elif self.direction not in possible and len(possible) == 2:
            print("corner")
            print(self.direction)
            self.direction = [i for i in possible if abs(i[0]) != abs(self.direction[0])][0]
            print(self.direction)


        # if there is a wall then choose another direction
        if self.is_wall(walls, nx, ny):
            possible = self.get_junction(walls, cx, cy)
            self.direction = random.choice(possible)


        self.change_x = self.direction[0] * self.unit_direction
        self.change_y = self.direction[1] * self.unit_direction

        
    def get_junction(self, walls, cx, cy):
        possible = []
        for direction in self.possible_directions:
            nx = cx + direction[0] * self.hypo_unit_direction
            ny = cy + direction[1] * self.hypo_unit_direction

            if not self.is_wall(walls, nx, ny):
                possible.append(direction)

        return possible



    def is_wall(self, walls, nx, ny):
        old_x = self.rect.left
        old_y = self.rect.top
        is_wall = False

        self.rect.left = nx
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
            is_wall = True
        else:
            self.rect.top = ny
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y
                is_wall = True

        self.rect.left = old_x
        self.rect.top = old_y

        return is_wall
