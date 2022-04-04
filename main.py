import external as ext
import copy
###currently pawns can captre by walking into pieces

class player:
    def __init__(self, turn, side, pieces, name):
        self.turn = turn
        self.side = side
        self.pieces = pieces
        self.name = name


class piece:
    def __init__(self, side, alive, position, first_move):
        self.side = side
        self.alive = alive
        self.position = position
        self.first_move = first_move


class bishop(piece):
    def __init__(self, side, alive, position, first_move):
        super().__init__(side, alive, position, first_move)

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
        removed_squares = self.almost_determine_valid_squares(init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)

        if init_position == [3,8]:
            print()
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()

        for i in removed_squares:
            if i in squares:
                squares.remove(i)

        for i in squares:
            #ghost_king_piece.position = i
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board):
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class knight(piece):
    def __init__(self, side, alive, position, first_move):
        super().__init__(side, alive, position, first_move)

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
        removed_squares = self.almost_determine_valid_squares(init_position, active_player, enemy_player, board)

        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        # for piece in ghost_active_player.pieces:
        #     if piece.__class__.__name__ == "king":
        #         ghost_king_piece = copy.deepcopy(piece)
        #         break

        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            #ghost_king_piece.position = i
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class rook(piece):
    def __init__(self, side, alive, position, first_move):
        super().__init__(side, alive, position, first_move)

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
        removed_squares = self.almost_determine_valid_squares(init_position, active_player, enemy_player, board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
#        for piece in ghost_active_player.pieces:
            # if piece.__class__.__name__ == "king":
            #     ghost_king_piece = copy.deepcopy(piece)
            #     original_position = piece.position
            #     break

        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            #ghost_king_piece.position = i
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)
            #ghost_king_piece.position = original_position

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class queen(piece):
    def __init__(self, side, alive, position, first_move):
        super().__init__(side, alive, position, first_move)

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
        removed_squares = self.almost_determine_valid_squares(init_position,active_player,enemy_player,board)
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        # for piece in ghost_active_player.pieces:
        #     if piece.__class__.__name__ == "king":
        #         ghost_king_piece = copy.deepcopy(piece)
        #         break
        
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            #ghost_king_piece.position = i
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            if i in squares:
                squares.remove(i)
        return squares


class pawn(piece):
    def __init__(self, side, alive, position, first_move):
        super().__init__(side, alive, position, first_move)

    def almost_determine_valid_squares(self, init_position, active_player, enemy_player, board):
        squares = board.copy()
        removed_squares = []

        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        enemy_positions = []
        for i in enemy_player.pieces:
            enemy_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            if self.side == "white":
                delta_y = i[1] - init_position[1]
            elif self.side == "black":
                delta_y = init_position[1] - i[1]
            
            if i == [8, 4]:
                print(end = "")

            if not i in enemy_positions:
                if self.first_move:
                    if not(delta_y == 1 and delta_x == 0) and not(delta_y == 2 and delta_x == 0):
                        removed_squares.append(i)
                elif not(delta_y == 1 and delta_x == 0):
                    removed_squares.append(i)

            elif i in active_positions:
                removed_squares.append(i)
        
            elif pieces_between(init_position, i, active_player, enemy_player):
                removed_squares.append(i)
            
            if i in enemy_positions and (delta_y == 1 and delta_x == 1):
                if i in removed_squares:
                    removed_squares.remove(i) 
        return removed_squares


    def determine_valid_squares(self, init_position, active_player, enemy_player, board):  
        removed_squares = self.almost_determine_valid_squares(init_position, active_player, enemy_player, board)    
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        # for piece in ghost_active_player.pieces:
        #     if piece.__class__.__name__ == "king":
        #         ghost_king_piece = copy.deepcopy(piece)
        #         break
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            #ghost_king_piece.position = i
            move(ghost_chosen_piece, i, ghost_enemy_player)
            is_check = check(ghost_active_player, ghost_enemy_player, board) 
            if is_check:
                removed_squares.append(i)
                
        for i in removed_squares:
            if i in squares:
                squares.remove(i)

        return squares


class king(piece):
    def __init__(self, side, alive, position, first_move):
        super().__init__(side, alive, position, first_move)

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
        removed_squares = self.almost_determine_valid_squares(init_position, active_player, enemy_player, board)
        # make a substitution piece that doesnt get affectecf by anything
        ghost_active_player = copy.deepcopy(active_player)
        ghost_enemy_player = copy.deepcopy(enemy_player)
        # for piece in ghost_active_player.pieces:
        #     if piece.__class__.__name__ == "king":
        #         ghost_king_piece = copy.deepcopy(piece)
        #         break
        ghost_chosen_piece = find_piece(ghost_active_player, init_position)
        squares = board.copy()
        for i in squares:
            #ghost_king_piece.position = i
            move(ghost_chosen_piece, i, ghost_enemy_player)
            if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
                removed_squares.append(i)

        for i in removed_squares:
            squares.remove(i)
        return squares


def get_array(stage, valid_squares):
    valid_coord = False
    while valid_coord == False:
        valid_coord = True
        letters = input(f"enter {stage} position: ")
        if letters == "back":
            return letters
        try:
            coord = ext.convert_to_coordinates(letters)
        except:
            print("Invalid coordinate.")
            valid_coord = False
            continue
        if coord not in valid_squares:
            valid_coord = False

    return coord


def pieces_between(start, end, player, enemy):
    delta_x = end[0] - start[0]
    delta_y = end[1] - start[1]

    if delta_x > 0:
        sign_x = 1
    elif delta_x < 0:
        sign_x = -1
    elif delta_x == 0:  # doing this instead of else incase it messes up soomething
        sign_x = 0
    else:
        raise Exception(
            "Error. start position or end position dont have numbers for x??")

    if delta_y > 0:
        sign_y = 1
    elif delta_y < 0:
        sign_y = -1
    elif delta_y == 0:  #doing this instead of else incase it messes up soomething
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


def check(active_player, enemy_player, board):
    for piece in active_player.pieces:
        if piece.__class__.__name__ == "king":
            king_piece = piece
            break

    for piece in enemy_player.pieces:
        valid_squares = board.copy()
        invalid_squares = piece.almost_determine_valid_squares(piece.position, enemy_player, active_player, board) #returns WAY too many values
        for i in invalid_squares:
            if i in valid_squares:
                valid_squares.remove(i)

        if king_piece.position in valid_squares:
            return True
    return False


def find_piece(active_player, position):
    for i in active_player.pieces:
        if position == i.position:
            return i
    return "PieceNotFoundError"


def move(piece, position, enemy_player):
    for enemy_piece in enemy_player.pieces:
        if position == enemy_piece.position:
            enemy_piece.alive = False
            enemy_player.pieces.remove(enemy_piece)
            break

    piece.position = position
    if piece.first_move == True:
        piece.first_move = False

def get_start(active_player,enemy_player,active_positions,enemy_positions,board):
    piece_valid = False
    while piece_valid == False:  # see extras.txt "attribution"
        start_position = get_array("start", active_positions)
        if start_position == "back":
            return get_start(active_player,enemy_player,active_positions,enemy_positions,board)
        chosen_piece = find_piece(active_player, start_position)

        piece_valid = True
        if chosen_piece == "PieceNotFoundError":
            piece_valid = False
            print("Try Again. NO piece here.")
            continue

        valid_squares = chosen_piece.determine_valid_squares(chosen_piece.position,
                                                                active_player, enemy_player, board)

        valid_coords = []
        for i in valid_squares:
            valid_coords.append(ext.convert_to_letters(i))

        if len(valid_squares) > 0:
            print(f"Your {chosen_piece.__class__.__name__} can move to are {valid_coords}.")
        else:
            print(
                f"The {chosen_piece.__class__.__name__} you chose cannot move to any squares ")
            piece_valid = False
    return chosen_piece,valid_squares,start_position

def get_end(active_player,enemy_player,chosen_piece,valid_squares,board,start_position):
    square_valid = False
    while square_valid == False:
        end_position = get_array("end", valid_squares)
        if end_position == "back":
            return play(active_player,enemy_player,board)
        square_valid = True
        if end_position not in valid_squares:
            square_valid = False
            print("sorry, no squares found here.")

    move(chosen_piece, end_position, enemy_player)
    print(f"The {chosen_piece.__class__.__name__} which was on {ext.convert_to_letters(start_position)} is now on {ext.convert_to_letters(chosen_piece.position)}.\n")

def play(active_player,enemy_player,player1,player2,board):
    is_check = check(active_player, enemy_player, board)
    all_moves = []

    for i in active_player.pieces:
        all_moves.append(i.determine_valid_squares(i.position, active_player, enemy_player, board))

    total_moves = 0
    for i in all_moves:
        total_moves += len(i)

    if total_moves == 0:
        if is_check:
            return f"{enemy_player.name} won ", "by checkmate."
        else:
            return "draw","by stalemate."


    if is_check:
        print("//YOU ARE ON CHECK!!")
    print(f"{active_player.name} is going now.")

    active_positions = []
    for i in active_player.pieces:
        active_positions.append(i.position)

    enemy_positions = []
    for i in enemy_player.pieces:
        active_positions.append(i.position)

    ######
    chosen_piece,valid_squares,start_position = get_start(active_player,enemy_player,active_positions,enemy_positions,board)
    get_end(active_player,enemy_player,chosen_piece,valid_squares,board,start_position)

    if active_player == player1 and enemy_player == player2:
        active_player = player2
        enemy_player = player1
    elif active_player == player2 and enemy_player == player1:
        active_player = player1
        enemy_player = player2
    else:
        raise Exception("Neither player is playing rn????")

    return play(active_player,enemy_player,player1,player2,board)

def start_game():
    # define full board
    board = []
    for y in range(8):
        for x in range(8):
            board.append([y+1, x+1])

    white_bishop_1 = bishop("white", True, [3, 1], True)
    white_bishop_2 = bishop("white", True, [6, 1], True)
    white_knight_1 = knight("white", True, [2, 1], True)
    white_knight_2 = knight("white", True, [7, 1], True)
    white_rook_1 = rook("white", True, [1, 1], True)
    white_rook_2 = rook("white", True, [8, 1], True)
    white_queen = queen("white", True, [4, 1], True)
    white_king = king("white", True, [5, 1], True)
    white_pawn_1 = pawn("white", True, [1, 2], True)
    white_pawn_2 = pawn("white", True, [2, 2], True)
    white_pawn_3 = pawn("white", True, [3, 2], True)
    white_pawn_4 = pawn("white", True, [4, 2], True)
    white_pawn_5 = pawn("white", True, [5, 2], True)
    white_pawn_6 = pawn("white", True, [6, 2], True)
    white_pawn_7 = pawn("white", True, [7, 2], True)
    white_pawn_8 = pawn("white", True, [8, 2], True)

    white_pieces = [white_pawn_1,
                    white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5,
                    white_pawn_6, white_pawn_7, white_pawn_8, white_bishop_1, white_bishop_2,
                    white_knight_1, white_knight_2, white_rook_1,
                    white_rook_2, white_queen, white_king]

    black_bishop_1 = bishop("black", True, [3, 8], True)
    black_bishop_2 = bishop("black", True, [6, 8], True)
    black_knight_1 = knight("black", True, [2, 8], True)
    black_knight_2 = knight("black", True, [7, 8], True)
    black_rook_1 = rook("black", True, [1, 8], True)
    black_rook_2 = rook("black", True, [8, 8], True)
    black_queen = queen("black", True, [4, 8], True)
    black_king = king("black", True, [5, 8], True) 
    black_pawn_1 = pawn("black", True, [1, 7], True)
    black_pawn_2 = pawn("black", True, [2, 7], True)
    black_pawn_3 = pawn("black", True, [3, 7], True)
    black_pawn_4 = pawn("black", True, [4, 7], True)
    black_pawn_5 = pawn("black", True, [5, 7], True) 
    black_pawn_6 = pawn("black", True, [6, 7], True)
    black_pawn_7 = pawn("black", True, [7, 7], True)
    black_pawn_8 = pawn("black", True, [8, 7], True)

    black_pieces = [black_rook_1, black_rook_2,
                    black_bishop_1, black_bishop_2, black_knight_1,
                    black_knight_2, black_queen, black_king, black_pawn_1,
                    black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5,
                    black_pawn_6, black_pawn_7, black_pawn_8]

    player1 = player(True, "white", white_pieces, "player1")
    player2 = player(False, "black", black_pieces, "player2")

    player1.name = "Player1"
    player2.name = "Player2"

    active_player = player1
    enemy_player = player2

    all_pieces = []
    for i in white_pieces:
        all_pieces.append(i)
    for i in black_pieces:
        all_pieces.append(i)

    winner,reason = play(active_player,enemy_player,player1,player2,board)
    return winner,reason



def start():
    winner, reason = start_game()
    print(f"Game over. {winner}{reason}")
start()
