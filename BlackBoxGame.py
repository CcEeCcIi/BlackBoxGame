# Author: Tingting Fang
# Date: 7/27/2020
# Description: A class named BlackBoxGame for playing an abstract board game called Black Box.

class BlackBoxGame:
    """To represent a board game BlackBoxGame with board, score and memory."""

    def __init__(self, atom_list):
        """To create a BlackBoxGame object with board, score and memory."""
        self._current_score = 25
        self._board = Board(atom_list)
        self._score = Score(self._current_score)
        self._memory = Memory()
        self._direction = None
        self._sign = None

    def shoot_ray(self, ray_row, ray_col):
        """Return false if row and column designate a corner square or a non-border square.
        Otherwise return a tuple of the row and column of the exit border square. Return None
        if no exit border square."""
        # shoot from corner square
        ray = (ray_row, ray_col)
        if ray == (0, 0) or ray == (0, 9) or ray == (9, 0) or ray == (9, 9):
            return print(False) #False

        # shoot from non-border square
        elif 1 <= ray_row <= 8 and 1 <= ray_col <= 8:
            return print(False) #False

        # other scenarios
        else:
            self._board.shoot_ray(ray_row, ray_col)


        # a hit
        #for el in range(0, len(self._atoms)):
            #if ray_row == self._atoms[el][0] or ray_col == self._atoms[el][1]:
                #print("hit")
                #return None
        # a miss
        #if ray_row == 0 or ray_row == 9:
            #for el in range(0, len(self._atoms)):
                #if ray_row != self._atoms[el][0] and ray_col != self._atoms[el][1]:
                    #exit = (ray_row, ray_col)
                #print("miss", exit)
                #return exit


        # adjust score accordingly


    def guess_atom(self, row, col):
        """Return True if there is an atom at that location. Otherwise return False."""
        pass
        # adjust score accordingly

    #def set_score(self):
        #"""Return the score after the action."""

    def get_score(self):
        """Return current score."""
        pass

    def atoms_left(self):
        """Returns the number of atoms that haven't been guessed yet."""
        pass

class Board:
    """To represent a game Board with rows and columns."""
    def __init__(self, atom_list):
        """To create a board object with rows and columns."""
        # initialize the board
        self._board = []
        for row in range(0, 10):
            self._board.append([])
            for col in range(0, 10):
                self._board[row].append(" ")

        # put atoms in the board
        self._atoms = atom_list
        for el in range(0, len(self._atoms)):
            row = self._atoms[el][0]
            col = self._atoms[el][1]
            self._board[row][col] = "o"

        self._current = None
        self._sign = None
        self._direciton = None
        self._atom_result = None
        # for debug
        for row in range(0, 10):
            print(self._board[row])

    def shoot_ray(self, ray_row, ray_col):
        """Return a tuple of the row and column of the exit border square. Return None\
        if no exit border square."""
        self._current = (ray_row, ray_col)

        # to decide direction and sign
        if ray_row == 0 or ray_row == 9:
            self._direction = True  # "vertical"
            if ray_row == 0:
                self._sign = True  # means "+"
            else:
                self._sign = False  # means "-"
        elif ray_col == 0 or ray_col == 9:
            self._direction = False  # "horizontal"
            if ray_col == 0:
                self._sign = True  # means "+"
            else:
                self._sign = False  # means "-"

        self._atom_result = self.scan(ray_row, ray_col, self._direction, self._sign)

        # a miss (vertical and horizontal)
        if self._atom_result == None and self._direction is True and self._sign is True:
            exit = (9, self._current[1])
            print("miss", exit)
            return exit
        elif self._atom_result == None and self._direction is True and self._sign is False:
            exit = (0, self._current[1])
            print("miss", exit)
            return exit
        elif self._atom_result == None and self._direction is False and self._sign is True:
            exit = (self._current[0], 9)
            print("miss", exit)
            return exit
        elif self._atom_result == None and self._direction is False and self._sign is False:
            exit = (self._current[0], 0)
            print("miss", exit)
            return exit

        # a "hit"
        if self._atom_result[0] != None:
            print("hit")
            return None

        # double deflection
        #elif self._atom_result[1] != None and self._atom_result[2] != None:
            #print("double deflection", (ray_row, ray_col))
            #return self.shoot_ray(ray_row, ray_col)

        else:
            if self._atom_result[1] != None and self._atom_result[2] == None:
                # a "reflection", vertical and horizontal
                if (ray_row == 0 and self._atom_result[1][0] == 1) or \
                        (ray_row == 9 and self._atom_result[1][0] == 8) or \
                        (ray_col == 0 and self._atom_result[1][1] == 1) or \
                        (ray_col == 9 and self._atom_result[1][1] == 8):
                    print("reflection", (ray_row, ray_col))
                    return (ray_row, ray_col)
                else:
                    # a detour
                    self.action(self._direction, self._sign)
                    return self.shoot_ray(self._current[0], self._current[1])
            elif self._atom_result[1] == None and self._atom_result[2] != None:
                if (ray_row == 0 and self._atom_result[2][0] == 1) or \
                        (ray_row == 9 and self._atom_result[2][0] == 8) or \
                        (ray_col == 0 and self._atom_result[2][1] == 1) or \
                        (ray_col == 9 and self._atom_result[2][1] == 8):
                    print("reflection", (ray_row, ray_col))
                    return (ray_row, ray_col)
                else:
                    # a detour
                    self.action(self._direction, self._sign)
                    return self.shoot_ray(self._current[0], self._current[1])
            else:
                # a detour
                self.action(self._direction, self._sign)
                return self.shoot_ray(self._current[0], self._current[1])

    def action(self, direction, sign):
        # take in where the ray start, change direction and sign
        """Return the square of ray start point."""
        # detour
        if (direction is True and sign is True) or (direction is False and sign is True):
            if self._atom_result[2] != None and self._atom_result[1] == None:
                self._sign = not sign
        if (direction is True and sign is False) or (direction is False and sign is False):
            if self._atom_result[1] != None and self._atom_result[2] == None:
                self._sign = not sign
        self._direction = not direction  # change direction



    def scan(self, row, col, direction, sign):
        """Return an array of tuple of atoms in three squares order (center, left, right)towards the ray direction.\
        if no atoms along the way, return None"""
        self._atom = []
        has_atom = False
        if sign is True:
            next_row = row + 1
            next_col = col + 1
            check_rows = 8 - row
            check_cols = 8 - col
        else:
            next_row = row - 1
            next_col = col - 1
            check_rows = row - 1
            check_cols = col - 1
        # case 1: vertical check atom
        if direction is True: #"vertical":
            for _ in range(0, check_rows):
                # check the center square
                if self._board[next_row][col] == "o":
                    self._atom.append((next_row, col))
                    has_atom = True
                else:
                    self._atom.append(None)

                # check the left square
                if 0 < col - 1 < 9:
                    if self._board[next_row][col - 1] == "o":
                        self._atom.append((next_row, col - 1))
                        has_atom = True
                    else:
                        self._atom.append(None)
                else:
                    self._atom.append(None)

                # check the right square
                if 0 < col + 1 < 9:
                    if self._board[next_row][col + 1] == "o":
                        self._atom.append((next_row, col + 1))
                        has_atom = True
                    else:
                        self._atom.append(None)
                else:
                    self._atom.append(None)

                if has_atom == True:
                    return self._atom
                else:
                    self._atom = []

                # update current ray
                self._current = (next_row, col)
                if sign is True: # means "+"
                    next_row += 1
                else:
                    next_row -= 1
            return None

        # case 2: horizontal check atom
        if direction is False: # "horizontal"
            for _ in range(0, check_cols):

                # check the center square
                if self._board[row][next_col] == "o":
                    self._atom.append((row, next_col))
                    has_atom = True
                else:
                    self._atom.append(None)

                # check the upper square
                if 0 < row - 1 < 9:
                    if self._board[row - 1][next_col] == "o":
                        self._atom.append((row - 1, next_col))
                        has_atom = True
                    else:
                        self._atom.append(None)
                else:
                    self._atom.append(None)

                # check the lower square
                if 0 < row + 1 < 9:
                    if self._board[row + 1][next_col] == "o":
                        self._atom.append((row + 1, next_col))
                        has_atom = True
                    else:
                        self._atom.append(None)
                else:
                    self._atom.append(None)

                if has_atom == True:
                    return self._atom
                else:
                    self._atom = []
                # update current ray
                self._current = (row, next_col)
                if sign is True: #means "+"
                    next_col += 1
                else:
                    next_col -= 1
            return None

    def get_direction(self):
        """Return direction"""



    def set_score(self):
        """Return the score after the action."""
        pass


class Score:
    """To represent the Score."""
    def __init__(self, score):
        """To create a score object."""
        self._score = 25

    def set_score(self):
        """Return the score after the action."""
        pass


    def get_score(self):
        """Return the current score."""
        pass

class Memory:
    """To represent the Memory of game with previous points and previous guess."""

    def __init__(self):
        """To create a Memory object with previous points and previous guess."""
        self._previous_points = []
        self._previous_guess = []

    def add_previous_points(self):
        """Return array of tuples of previous entry/exit point."""
        pass

    def add_previous_guess(self):
        """Return array of atoms of previous guess."""
        pass

# detour 1
atom_list_1 = [(3,2),(3,7),(6,4),(8,7)]
# detour 2: median
atom_list_2 = [(2,6),(7,6),(7,8)]
# detour 3: easy
atom_list_3 = [(4,6)]
# detour 4:
atom_list_4 = [(3,3),(2,6),(7,6)]
# double deflection:
atom_list_5 = [(6,4),(6,6)]
# deflection:
atom_list_6 = [(3,2),(3,7),(6,4),(8,7)]
#board = Board(atom_list)
game = BlackBoxGame(atom_list_6)
# test for detour 1:
#game.shoot_ray(0, 3)
#game.shoot_ray(4, 9)
#game.shoot_ray(5, 0)

# test for detour 3
#game.shoot_ray(5, 0)

# test for detour 2:
#game.shoot_ray(3, 9)

# test for detour 4:
#game.shoot_ray(6, 0)

# test for double deflection 5:
#game.shoot_ray(0, 5)

# test for deflection:
#game.shoot_ray(5, 9)

#board.action(1, 9)
#board.action(0, 6)
#board.action(9, 6)
#board.action(7, 0)
# corner square
#game.shoot_ray(0, 0)
#game.shoot_ray(0, 9)
#game.shoot_ray(9, 0)
#game.shoot_ray(9, 9)
# non-border square
#game.shoot_ray(1, 7)
#game.shoot_ray(3, 8)
#game.shoot_ray(8, 8)
#game.shoot_ray(8, 5)
#game.shoot_ray(1, 1)
# vertical, sign"+", sign"-"
#game.shoot_ray(0, 4)
#game.shoot_ray(0, 6)
#game.shoot_ray(0, 2)
#game.shoot_ray(9, 5)
#game.shoot_ray(9, 7)
# horizontal, sign"+", sign"-"
#game.shoot_ray(3, 0)
#game.shoot_ray(7, 0)
#game.shoot_ray(4, 9)
#game.shoot_ray(2, 9)
# vertical, reflection
#game.shoot_ray(9, 7)
# detour

#game.shoot_ray(0, 5)
#game.shoot_ray(3, 9)
