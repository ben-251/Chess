# initialised
import copy


class player:
    def __init__(self, turn, side, pieces, name, back_rank):
        self.turn = turn
        self.side = side
        self.pieces = pieces
        self.name = name
        self.back_rank = back_rank


class piece:
    def __init__(self, side, alive, position, first_move, symbol):
        self.side = side
        self.alive = alive
        self.position = position
        self.first_move = first_move
        self.symbol = symbol


class bishop(piece):
    def __init__(self, side, alive, position, first_move, symbol):
        super().__init__(side, alive, position, first_move, symbol)
        self.name = "bishop"

    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        squares = board.copy()
        removed_squares = []
        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if delta_x != delta_y and not i in removed_squares:
                removed_squares.append(i)
            elif i in active_positions and not i in removed_squares:
                removed_squares.append(i)
            elif pieces_between(init_position, i, active_player, enemy_player):
                removed_squares.append(i)

        return removed_squares

    def determine_valid_squares(self, init_position, active_player, enemy_player, board):
        removed_squares = self.almost_determine_valid_squares(
            init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)

        if init_position == [3, 8]:
            print()
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()

        for i in removed_squares:
            if i in squares:
                squares.remove(i)

        for i in squares:
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board):
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class knight(piece):
    def __init__(self, side, alive, position, first_move, symbol):
        super().__init__(side, alive, position, first_move, symbol)
        self.name = "knight"

    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        squares = board.copy()
        removed_squares = []

        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if (not(delta_x == 1 and delta_y == 2)) and (not(delta_x == 2 and delta_y == 1)) and not i in removed_squares:
                removed_squares.append(i)
            elif i in active_positions and not i in removed_squares:
                removed_squares.append(i)
        return removed_squares

    def determine_valid_squares(self, init_position, active_player, enemy_player, board):
        removed_squares = self.almost_determine_valid_squares(
            init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)

        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class rook(piece):
    def __init__(self, side, alive, position, first_move, symbol):
        super().__init__(side, alive, position, first_move, symbol)
        self.name = "rook"

    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        squares = board.copy()
        removed_squares = []

        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if (not(delta_x > 0 and delta_y == 0)) and (not(delta_x == 0 and delta_y > 0)) and (not i in removed_squares):
                removed_squares.append(i)
            elif i in active_positions:
                removed_squares.append(i)

            elif pieces_between(init_position, i, active_player, enemy_player):
                removed_squares.append(i)
        return removed_squares

    def determine_valid_squares(self, init_position, active_player, enemy_player, board):
        removed_squares = self.almost_determine_valid_squares(
            init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class queen(piece):
    def __init__(self, side, alive, position, first_move, symbol):
        super().__init__(side, alive, position, first_move, symbol)
        self.name = "queen"

    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        squares = board.copy()
        removed_squares = []

        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if (not(delta_x > 0 and delta_y == 0)) and (not(delta_x == 0 and delta_y > 0)) and (delta_x != delta_y):
                if not i in removed_squares:
                    removed_squares.append(i)
            elif i in active_positions and not i in removed_squares:
                removed_squares.append(i)

            elif pieces_between(init_position, i, active_player, enemy_player):
                removed_squares.append(i)
        return removed_squares

    def determine_valid_squares(self, init_position, active_player, enemy_player, board):
        removed_squares = self.almost_determine_valid_squares(
            init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class pawn(piece):
    def __init__(self, side, alive, position, first_move, symbol):
        super().__init__(side, alive, position, first_move, symbol)
        self.name = "pawn"

    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        squares = board.copy()
        removed_squares = []

        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        enemy_positions = []
        for i in enemy_player.pieces:
            enemy_positions.append(i.position)

        all_positions = []
        all_positions.extend(enemy_positions)
        all_positions.extend(active_positions)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            if self.side == "white":
                delta_y = i[1] - init_position[1]
            elif self.side == "black":
                delta_y = init_position[1] - i[1]

            if not i in enemy_positions:
                if self.first_move:
                    if not(delta_y == 1 and delta_x == 0) and not(delta_y == 2 and delta_x == 0):
                        removed_squares.append(i)
                elif not(delta_y == 1 and delta_x == 0):
                    removed_squares.append(i)

            if i in all_positions:
                removed_squares.append(i)

            if pieces_between(init_position, i, active_player, enemy_player):
                removed_squares.append(i)

            if i in enemy_positions and (delta_y == 1 and delta_x == 1):
                if i in removed_squares:
                    removed_squares.remove(i)
        return removed_squares

    def determine_valid_squares(self, init_position, active_player, enemy_player, board):
        removed_squares = self.almost_determine_valid_squares(
            init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()

        for i in squares:

            move(ghost_chosen_piece, i, ghost_enemy_player)
            is_check = check(ghost_active_player, ghost_enemy_player, board)
            if is_check:
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)

        return squares


class king(piece):   
    def __init__(self, side, alive, position, first_move, symbol):
        super().__init__(side, alive, position, first_move, symbol)
        self.name = "king" 
    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        x = 0
        y = 0
        squares = board.copy()
        removed_squares = []
        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if delta_x > 1 or delta_y > 1:
                if not i in removed_squares:
                    removed_squares.append(i)
            else:
                if i in active_positions and not i in removed_squares:
                    removed_squares.append(i)
        return removed_squares

    def determine_valid_squares(self, init_position, active_player, enemy_player, board):
        removed_squares = self.almost_determine_valid_squares(
            init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
 
        for i in squares:
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            squares.remove(i)
        return squares


white_bishop_1 = bishop("white", True, [3, 1], True, "b")
white_bishop_2 = bishop("white", True, [6, 1], True, "b")
white_knight_1 = knight("white", True, [2, 1], True, "n")
white_knight_2 = knight("white", True, [7, 1], True, "n")
white_rook_1 = rook("white", True, [1, 1], True, "r")
white_rook_2 = rook("white", True, [8, 1], True, "r")
white_queen = queen("white", True, [4, 1], True, "q")
white_king = king("white", True, [5, 1], True, "k")
white_pawn_1 = pawn("white", True, [1, 2], True, "o")
white_pawn_2 = pawn("white", True, [2, 2], True, "o")
white_pawn_3 = pawn("white", True, [3, 2], True, "o")
white_pawn_4 = pawn("white", True, [4, 2], True, "o")
white_pawn_5 = pawn("white", True, [5, 2], True, "o")
white_pawn_6 = pawn("white", True, [6, 2], True, "o")
white_pawn_7 = pawn("white", True, [7, 2], True, "o")
white_pawn_8 = pawn("white", True, [8, 2], True, "o")

white_pieces = [white_pawn_1,
                white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5,
                white_pawn_6, white_pawn_7, white_pawn_8, white_bishop_1, white_bishop_2,
                white_knight_1, white_knight_2, white_rook_1,
                white_rook_2, white_queen, white_king]

black_bishop_1 = bishop("black", True, [3, 8], True, "B")
black_bishop_2 = bishop("black", True, [6, 8], True, "B")
black_knight_1 = knight("black", True, [2, 8], True, "N")
black_knight_2 = knight("black", True, [7, 8], True, "N")
black_rook_1 = rook("black", True, [1, 8], True, "R")
black_rook_2 = rook("black", True, [8, 8], True, "R")
black_queen = queen("black", True, [4, 8], True, "Q")
black_king = king("black", True, [5, 8], True, "K")
black_pawn_1 = pawn("black", True, [1, 7], True, "O")
black_pawn_2 = pawn("black", True, [2, 7], True, "O")
black_pawn_3 = pawn("black", True, [3, 7], True, "O")
black_pawn_4 = pawn("black", True, [4, 7], True, "O")
black_pawn_5 = pawn("black", True, [5, 7], True, "O")
black_pawn_6 = pawn("black", True, [6, 7], True, "O")
black_pawn_7 = pawn("black", True, [7, 7], True, "O")
black_pawn_8 = pawn("black", True, [8, 7], True, "O")

black_pieces = [black_rook_1, black_rook_2,
                black_bishop_1, black_bishop_2, black_knight_1,
                black_knight_2, black_queen, black_king, black_pawn_1,
                black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5,
                black_pawn_6, black_pawn_7, black_pawn_8]

player1 = player(True, "white", white_pieces, "player1",1)
player2 = player(False, "black", black_pieces, "player2",8)


# PROCESSES
def check(active_player, enemy_player, board):
    for piece in active_player.pieces:
        if piece.name == "king":
            king_piece = piece
            break

    for piece in enemy_player.pieces:
        valid_squares = board.copy()
        invalid_squares = piece.almost_determine_valid_squares(
            piece.position, enemy_player, active_player, board)
        for i in invalid_squares:
            if i in valid_squares:
                valid_squares.remove(i)

        if king_piece.position in valid_squares:
            return True
    return False


def move(piece, position, enemy_player):
    for enemy_piece in enemy_player.pieces:
        if position == enemy_piece.position:
            enemy_piece.alive = False
            enemy_player.pieces.remove(enemy_piece)
            break

    piece.position = position
    if piece.first_move == True:
        piece.first_move = False


def pieces_between(start, end, player, enemy):
    delta_x = end[0] - start[0]
    delta_y = end[1] - start[1]

    # This function only works if the movement is a straight line (vertical, horizontal, or diagonal)
    # Which is fine because a knight is the only piece that doesn't move like that...
    # and also the only piece that can jump over others so this function never needs to be called for it!
    if not (delta_x == 0 or delta_y == 0 or abs(delta_x) == abs(delta_y)):
        return False

    if delta_x > 0:
        sign_x = 1
    elif delta_x < 0:
        sign_x = -1
    elif delta_x == 0:
        sign_x = 0
    else:
        raise Exception(
            "Error. start position or end position dont have numbers for x??")

    if delta_y > 0:
        sign_y = 1
    elif delta_y < 0:
        sign_y = -1
    elif delta_y == 0:
        sign_y = 0
    else:
        raise Exception(
            "Error. start position or end position dont have numbers for y??")

    coord = start.copy()
    coord[0] += sign_x
    coord[1] += sign_y

    all_positions = []
    for i in player.pieces:
        all_positions.append(i.position)
    for i in enemy.pieces:
        all_positions.append(i.position)

    while coord != end:
        if coord in all_positions:
            return True
        coord[0] += sign_x
        coord[1] += sign_y

    return False


def find_piece(active_player, position):
    for i in active_player.pieces:
        if position == i.position:
            return i
    return "PieceNotFoundError"


def can_castle(direction, active_player, enemy_player):
    if direction == "long":
        rook_position = [1,active_player.back_rank]
    elif direction == "short":
        rook_position = [8,active_player.back_rank]
    else:
        raise Exception("No castle direction")
    
    king_position = [5,active_player.back_rank]
    

    piece =  find_piece(active_player, king_position)
    if piece.name != "king":
        return False

    piece = find_piece(active_player,rook_position)
    if piece.name != "rook":
        return False

    if pieces_between(king_position.rook_position,active_player,enemy_player):
        return False
    
    return True
    #  then check if rook and king there, then chek if first move,
    #  then check if pieces betwen, then check that there is no check as you 
    # loop through, putting the king on each square between
    #if return false never happens, then castle by following the ryles based on yeah





##output##


def convert_to_letters(coordinates):
    letters = ""
    letters += chr(coordinates[0]+96)
    letters += str(coordinates[1])
    return letters


def convert_to_coordinates(letters):
    # a = 97, ord("a") = 97, chr(97) = "a"
    # 97 - 96 = 1
    coord = []
    coord.append(ord(letters[0])-96)
    coord.append(int(letters[1]))
    return coord


def display(active_player, enemy_player, is_check):
    active_pieces = []
    enemy_pieces = []

    king_piece = king("blue", False, [1000, 10000], False, "ben")

    for i in active_player.pieces:
        active_pieces.append(i)
    for i in enemy_player.pieces:
        enemy_pieces.append(i)

    if is_check:
        for piece in active_pieces:
            if piece.name == "king":
                king_piece = piece
                init_symbol = king_piece.symbol
                king_piece.symbol = "+"

    active_positions = []
    enemy_positions = []

    for i in active_player.pieces:
        active_positions.append(i.position)
    for i in enemy_player.pieces:
        enemy_positions.append(i.position)

    board = []
    for y in range(8):
        for x in range(8):
            board.append([y+1, x+1])

    for y in range(8, 0, -1):
        for x in range(1, 9):
            if [x, y] in active_positions:
                player_with_piece = active_player
                is_there = True
            elif [x, y] in enemy_positions:
                player_with_piece = enemy_player
                is_there = True
            else:
                is_there = False

            if is_there:
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                    print(
                        f"[---{find_piece(player_with_piece,[x,y]).symbol}---]", end="")
                else:
                    print(
                        f"[   {find_piece(player_with_piece,[x,y]).symbol}   ]", end="")
            else:
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                    print("[-------]", end="")
                else:
                    print("[       ]", end="")
        print("\n")

    return
