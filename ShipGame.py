class ShipGame:
    """A class to represent a Battleship game played by two players."""

    def __init__(self):
        """Constructor for ShipGame class. Initializes the required data members."""

        # Initialize game state
        self._player1_turn = True
        self._player2_turn = False
        self._current_state = 'UNFINISHED'

        # Initialize player data
        self._num_ships_remaining1 = 0
        self._num_ships_remaining2 = 0
        self._ship_list1 = {}
        self._ship_list2 = {}
        self._player1_target_squares = []
        self._player2_target_squares = []

        # Initialize board data
        self._board_player1 = self._initialize_board()
        self._board_player2 = self._initialize_board()

    def _initialize_board(self):
        """Helper method to initialize the game board with coordinates."""

        board = {}
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for letter in letters:
            for i in range(1, 11):
                square = letter + str(i)
                board[square] = [ord(letter) - ord('A'), i - 1]
        return board

    def place_ship(self, player_num, length_of_ship, start_square, ship_orientation):
        """Places a ship on the game board for the specified player.
        
        Parameters:
        - player_num: Represents the player's turn.
        - length_of_ship: Length of the ship to be placed.
        - start_square: The coordinate at which the player wishes to place the ship.
        - ship_orientation: Orientation of the ship ('C' for column, 'R' for row).
        
        Returns:
        - False: If ship does not fit into the required game board, overlaps with another ship, or invalid parameters.
        - True: If the ship is successfully placed on the board.
        """
        if self._count_start != 0:
            print("Already placed ship")
            return False

        board = self._board_player1 if player_num == 'first' else self._board_player2

        if start_square not in board or board[start_square] == 'X':
            return False

        row, col = board[start_square]
        max_row, max_col = max(board.values())

        if ship_orientation == 'C':
            if row + length_of_ship - 1 > max_row:
                return False
            for i in range(row, row + length_of_ship):
                if board.get(chr(i + ord('A')) + str(col + 1)) == 'X':
                    return False
        elif ship_orientation == 'R':
            if col + length_of_ship - 1 > max_col:
                return False
            for i in range(col,.
                if board.get(chr(row + ord('A')) + str(i + 1)) == 'X':
                    return False
        else:
            return False

        # Place the ship on the board
        if ship_orientation == 'C':
            for i in range(row, row + length_of_ship):
                board[chr(i + ord('A')) + str(col + 1)] = 'X'
        elif ship_orientation == 'R':
            for i in range(col, col + length_of_ship):
                board[chr(row + ord('A')) + str(i + 1)] = 'X'

        # Update ship data for the player
        if player_num == 'first':
            self._num_ships_remaining1 += 1
            self._ship_list1[start_square] = length_of_ship
        else:
            self._num_ships_remaining2 += 1
            self._ship_list2[start_square] = length_of_ship

        return True

    def _switch_turns(self):
        """Helper method to switch turns between players."""
        self._player1_turn = not self._player1_turn
        self._player2_turn = not self._player2_turn

    def fire_torpedo(self, player_num, target_square):
        """Fires a torpedo at the specified target square for the player.
        
        Parameters:
        - player_num: Represents the player's turn.
        - target_square: The coordinate at which the player wishes to fire the torpedo.
        
        Returns:
        - False: If the game is already finished, it's not the player's turn, or the target square has already been hit.
        - True: If the torpedo successfully hits the target square.
        """
        if self._current_state != 'UNFINISHED' or (player_num == 'first' and not self._player1_turn) or (player_num == 'second' and not self._player2_turn):
            return False

        board = self._board_player1 if player_num == 'first' else self._board_player2
        target_board = self._board_player2 if player_num == 'first' else self._board_player1
        target_squares = self._player1_target_squares if player_num == 'first' else self._player2_target_squares

        if target_square not in target_board or target_square in target_squares:
            return False

        target_squares.append(target_square)

        # Check if the torpedo hits a ship
        if target_board[target_square] == 'X':
            target_board[target_square] = 'H'
            if player_num == 'first':
                self._num_ships_remaining2 -= 1
            else:
                self._num_ships_remaining1 -= 1
        else:
            target_board[target_square] = 'M'

        # Check if the game is finished
        if self._num_ships_remaining1 == 0 or self._num_ships_remaining2 == 0:
            self._current_state = 'FINISHED'
        else:
            self._switch_turns()

        return True
