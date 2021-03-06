# Author: Tingting Fang
# Date: 8/7/2020
# Description: A class named BlackBoxGame for playing an abstract board game called Black Box.

class BlackBoxGame:
    """To represent a board game BlackBoxGame with board, score and memory."""

    def __init__(self, atom_list):
        """To create a BlackBoxGame object with board, score and memory."""
        self._board_size = 10
        self._high = self._board_size - 2
        self._score = 25
        self._point_penalty = 1
        self._guess_penalty = 5
        self._board = Board(atom_list)
        self._atom_list = atom_list
        self._previous_points = set()
        self._previous_guess = set()

    def shoot_ray(self, ray_row, ray_col):
        """Return false if row and column designate a corner square or a non-border square.
        Otherwise return a tuple of the row and column of the exit border square. Return None
        if no exit border square."""

        ray = (ray_row, ray_col)

        # shoot from corner square
        if ray == (0, 0) or ray == (0, self._board_size - 1) or \
                ray == (self._board_size - 1, 0) or ray == (self._board_size - 1, self._board_size - 1):
            return False

        # shoot from non-border square
        elif 1 <= ray_row <= self._high and 1 <= ray_col <= self._high:
            return False

        # other scenarios
        else:
            # if ray not in previous points
            if ray not in self._previous_points:
                self.set_score(self._point_penalty)
            # update previous entry/exit points
            self.add_previous_points(ray)

            exit = self._board.shoot_ray(ray_row, ray_col)

            # if exit exists
            if exit != None:
                # if exit not in previous points
                if exit not in self._previous_points:
                    self.set_score(self._point_penalty)
                # add to previous entry/exit points
                self.add_previous_points(exit)
            return exit

    def guess_atom(self, row, col):
        """Return True if there is an atom at that location. Otherwise return False."""
        # add to guess set
        guess = (row, col)
        # check if guess right
        for el in self._atom_list:
            if (row, col) == el:
                self.add_previous_guess(guess)
                self._board.change_atom_state(row, col)
                return True
        # update score if guess wrong
        if guess not in self._previous_guess:
            self.set_score(self._guess_penalty)
        self.add_previous_guess(guess)
        return False

    def set_score(self, penalty):
        """Return the score after the action."""
        self._score -= penalty

    def get_score(self):
        """Return the current score."""
        return self._score

    def atoms_left(self):
        """Returns the number of atoms that haven't been guessed yet."""
        left = 0
        for el in range(0, len(self._atom_list)):
            row = self._atom_list[el][0]
            col = self._atom_list[el][1]
            if self._board._board[row][col] == "o":
                left += 1
        return left

    def add_previous_points(self, point):
        """Return array of tuples of previous entry/exit point."""
        self._previous_points.add(point)

    def add_previous_guess(self, guess):
        """Return array of atoms of previous guess."""
        self._previous_guess.add(guess)

    # debug
    def get_previous_points(self):
        return self._previous_points

    def get_previous_guess(self):
        return self._previous_guess

class Board:
    """To represent a game Board with rows and columns."""
    def __init__(self, atom_list):
        """To create a board object with rows and columns."""
        self._board_size = 10
        self._high = self._board_size - 2

        # initialize the board
        self._board = []
        for row in range(0, self._board_size):
            self._board.append([])
            for col in range(0, self._board_size):
                self._board[row].append(" ")

        # put atoms in the board
        self._atoms = atom_list
        for el in range(0, len(self._atoms)):
            row = self._atoms[el][0]
            col = self._atoms[el][1]
            self._board[row][col] = "o"

        self._current = None
        self._sign = None
        self._direction = None
        self._atom_result = None
        self._atom = []
        self._has_atom = False

    def shoot_ray(self, ray_row, ray_col):
        """Return a tuple of the row and column of the exit border square. Return None\
        if no exit border square."""
        self._current = (ray_row, ray_col)

        # to decide direction and sign
        if ray_row == 0 or ray_row == self._board_size - 1:
            self._direction = True  # "vertical"
            if ray_row == 0:
                self._sign = True  # means "+"
            else:
                self._sign = False  # means "-"
        elif ray_col == 0 or ray_col == self._board_size - 1:
            self._direction = False  # "horizontal"
            if ray_col == 0:
                self._sign = True  # means "+"
            else:
                self._sign = False  # means "-"

        self._atom_result = self.scan(ray_row, ray_col, self._direction, self._sign)

        # check if is "miss"
        exit = self.miss()
        if exit != None:
            return exit

        # a "hit"
        if self._atom_result[0] != None:
            return None

        # check if is "reflection"
        if self.reflection(ray_row, ray_col) != None:
            return self.reflection(ray_row, ray_col)
        else:
            # a detour
            self.action(self._direction, self._sign)
            return self.shoot_ray(self._current[0], self._current[1])

    def miss(self):
        """To take care of the scenario "miss" and return the exit square, otherwise return None."""
        # a miss (vertical and horizontal)
        if self._atom_result == None and self._direction is True and self._sign is True:
            exit = (self._board_size - 1, self._current[1])
            return exit
        elif self._atom_result == None and self._direction is True and self._sign is False:
            exit = (0, self._current[1])
            return exit
        elif self._atom_result == None and self._direction is False and self._sign is True:
            exit = (self._current[0], self._board_size - 1)
            return exit
        elif self._atom_result == None and self._direction is False and self._sign is False:
            exit = (self._current[0], 0)
            return exit
        else:
            return None

    def reflection(self, ray_row, ray_col):
        """To take care of scenario "reflection" and return the exit square, otherwise return None."""
        if self._atom_result[1] != None and self._atom_result[2] == None:
            # a "reflection", vertical and horizontal
            if (ray_row == 0 and self._atom_result[1][0] == 1) or \
                    (ray_row == self._board_size - 1 and self._atom_result[1][0] == self._high) or \
                    (ray_col == 0 and self._atom_result[1][1] == 1) or \
                    (ray_col == self._board_size - 1 and self._atom_result[1][1] == self._high):
                return (ray_row, ray_col)
            else:
                return None
        elif self._atom_result[1] == None and self._atom_result[2] != None:
            # a "reflection", vertical and horizontal
            if (ray_row == 0 and self._atom_result[2][0] == 1) or \
                    (ray_row == self._board_size - 1 and self._atom_result[2][0] == self._high) or \
                    (ray_col == 0 and self._atom_result[2][1] == 1) or \
                    (ray_col == self._board_size - 1 and self._atom_result[2][1] == self._high):
                return (ray_row, ray_col)
            else:
                return None
        else:
            return None

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

    def vertical_scan(self, next_row, col, sign, check_rows):
        """Return an array of tuple of atoms in three squares order (center, left, right)towards \
        the ray direction. If no atoms along the way, return None."""
        self._has_atom = False
        self._atom = []

        for _ in range(0, check_rows):
            # check the center square
            self.check_center(next_row, col)
            # check the left square
            if 0 < col - 1 < self._board_size - 1:
                if self._board[next_row][col - 1] != " ":
                    self._atom.append((next_row, col - 1))
                    self._has_atom = True
                else:
                    self._atom.append(None)
            else:
                self._atom.append(None)
            # check the right square
            if 0 < col + 1 < self._board_size - 1:
                if self._board[next_row][col + 1] != " ":
                    self._atom.append((next_row, col + 1))
                    self._has_atom = True
                else:
                    self._atom.append(None)
            else:
                self._atom.append(None)

            if self._has_atom == True:
                return self._atom
            else:
                self._atom = []
            # update current ray and next row
            next_row = self.update_row(next_row, col, sign)
        return None

    def check_center(self, row, col):
        """Check if there is an atom in the center."""
        if self._board[row][col] != " ":
            self._atom.append((row, col))
            self._has_atom = True
        else:
            self._atom.append(None)

    def update_row(self, row, col, sign):
        """Update current square and next row"""
        # update current ray
        self._current = (row, col)
        if sign is True:  # means "+"
            row += 1
        else:
            row -= 1
        return row

    def horizontal_scan(self, row, next_col, sign, check_cols):
        """Return an array of tuple of atoms in three squares order (center, left, right)towards \
        the ray direction. If no atoms along the way, return None."""
        self._has_atom = False
        self._atom = []

        for _ in range(0, check_cols):
            # check the center square
            self.check_center(row, next_col)
            # check the upper square
            if 0 < row - 1 < self._board_size - 1:
                if self._board[row - 1][next_col] != " ":
                    self._atom.append((row - 1, next_col))
                    self._has_atom = True
                else:
                    self._atom.append(None)
            else:
                self._atom.append(None)
            # check the lower square
            if 0 < row + 1 < self._board_size - 1:
                if self._board[row + 1][next_col] != " ":
                    self._atom.append((row + 1, next_col))
                    self._has_atom = True
                else:
                    self._atom.append(None)
            else:
                self._atom.append(None)

            if self._has_atom == True:
                return self._atom
            else:
                self._atom = []
            # update current ray and next column
            next_col = self.update_col(row, next_col, sign)
        return None

    def update_col(self, row, col, sign):
        """Update current square and next col"""
        # update current ray
        self._current = (row, col)
        if sign is True:  # means "+"
            col += 1
        else:
            col -= 1
        return col

    def scan(self, row, col, direction, sign):
        """Return an array of tuple of atoms in three squares order (center, left, right)towards \
        the ray direction. If no atoms along the way, return None"""

        # initialize next_row and next_col.
        if sign is True:
            next_row = row + 1
            next_col = col + 1
            check_rows = self._high - row
            check_cols = self._high - col
        else:
            next_row = row - 1
            next_col = col - 1
            check_rows = row - 1
            check_cols = col - 1

        # case 1: vertical check atom
        if direction is True:  # "vertical"
            return self.vertical_scan(next_row, col, sign, check_rows)

        # case 2: horizontal check atom
        if direction is False:  # "horizontal"
            return self.horizontal_scan(row, next_col, sign, check_cols)

    def change_atom_state(self, row, col):
        """If user guess the atom correct, atom will be changed as "x" to indicate correct guess."""
        self._board[row][col] = "x"

