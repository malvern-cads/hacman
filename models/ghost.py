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
    direction = None

    # Change the speed of the ghost
    def changespeed(self, walls):
        if self.direction is None:
            self.direction = random.choice(self.possible_directions)

        cx = self.rect.left
        cy = self.rect.top

        nx = cx + self.direction[0] * self.unit_direction
        ny = cy + self.direction[1] * self.unit_direction

        if self.is_wall(walls, nx, ny):
            self.direction = random.choice(self.possible_directions)

        self.change_x = self.direction[0] * self.unit_direction
        self.change_y = self.direction[1] * self.unit_direction

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
