class ShipGame:
    def __init__(self):
        self._player1_target_squares = []
        self._player2_target_squares = []
        self._num_ships_remaining1 = 0
        self._num_ships_remaining2 = 0
        self._ship_list1 = {}
        self._ship_list2 = {}
        self._current_state = 'UNFINISHED'
        self._board_size = 10
        self._board_player1 = self._create_board()
        self._board_player2 = self._create_board()

    def _create_board(self):
        board = {}
        for row in range(self._board_size):
            for col in range(self._board_size):
                square = f'{chr(row + 65)}{col + 1}'
                board[square] = [row, col]
        return board

    def get_count(self, player_num):
        if player_num == 'first':
            return self._num_ships_remaining1
        elif player_num == 'second':
            return self._num_ships_remaining2
        else:
            return None

    def set_count_start(self, count):
        self._num_ships_remaining1 = count
        self._num_ships_remaining2 = count

    def get_count_start(self):
        return self._num_ships_remaining1

    def set_count(self, player_num, count):
        if player_num == 'first':
            self._num_ships_remaining1 = count
        elif player_num == 'second':
            self._num_ships_remaining2 = count

    def place_ship(self, player_num, length_of_ship, start_square, ship_orientation):
        if player_num == 'first':
            board = self._board_player1
            target_squares = self._player1_target_squares
            ship_list = self._ship_list1
            num_ships_remaining = self._num_ships_remaining1
        elif player_num == 'second':
            board = self._board_player2
            target_squares = self._player2_target_squares
            ship_list = self._ship_list2
            num_ships_remaining = self._num_ships_remaining2
        else:
            return False

        if start_square not in board or board[start_square] == 'X':
            return False

        row, col = board[start_square]
        if ship_orientation == 'C':
            if col + length_of_ship > self._board_size:
                return False
            for i in range(col, col + length_of_ship):
                square = f'{chr(row + 65)}{i + 1}'
                if board[square] == 'X':
                    return False
                target_squares.append(square)
                ship_list[square] = num_ships_remaining
        elif ship_orientation == 'R':
            if row + length_of_ship > self._board_size:
                return False
            for i in range(row, row + length_of_ship):
                square = f'{chr(i + 65)}{col + 1}'
                if board[square] == 'X':
                    return False
                target_squares.append(square)
                ship_list[square] = num_ships_remaining
        else:
            return False

        for square in target_squares:
            board[square] = 'X'
        
        num_ships_remaining += 1
        return True

    def get_current_state(self):
        return self._current_state

    def set_current_state(self, state):
        self._current_state = state

    def fire_torpedo(self, player_num, target_square):
        if player_num == 'first':
            board = self._board_player2
            target_squares = self._player2_target_squares
            ship_list = self._ship_list2
            num_ships_remaining = self._num_ships_remaining2
        elif player_num == 'second':
            board = self._board_player1
            target_squares = self._player1_target_squares
            ship_list = self._ship_list1
            num_ships_remaining = self._num_ships_remaining1
        else:
            return False

        if target_square not in board:
            return False

        if target_square in target_squares:
            target_squares.remove(target_square)
            if self.validate_ship_sunk(ship_list, num_ships_remaining):
                num_ships_remaining -= 1
                if num_ships_remaining == 0:
                    self.set_current_state('WON')
            return True
        else:
            return False

    def get_num_ships_remaining(self, player_num):
        if player_num == 'first':
            return self._num_ships_remaining1
        elif player_num == 'second':
            return self._num_ships_remaining2
        else:
            return None

    def validate_ship_sunk(self, ship_list, num_ships_remaining):
        return all(ship == 0 for ship in ship_list.values())

    def validate_winner(self):
        if self._current_state == 'WON':
            return 'first' if self._num_ships_remaining2 == 0 else 'second'
        else:
            return None
