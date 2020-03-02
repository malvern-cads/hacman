from models.player import Player


# Inheritime Player klassist
class Ghost(Player):
    turn = 0
    steps = 0
    directions = []

    # Change the speed of the ghost
    def changespeed(self, ghost):
        try:
            z = self.directions[self.turn][2]
            if self.steps < z:
                self.change_x = self.directions[self.turn][0]
                self.change_y = self.directions[self.turn][1]
                self.steps += 1
            else:
                if self.turn < (len(self.directions) - 1):
                    self.turn += 1
                elif ghost == "clyde":
                    self.turn = 2
                else:
                    self.turn = 0
                self.change_x = self.directions[self.turn][0]
                self.change_y = self.directions[self.turn][1]
                self.steps = 0
        except IndexError:
            self.turn = 0
            self.steps = 0
