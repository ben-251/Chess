import backend as ext
import output as out
import copy

def get_array(stage, valid_squares,can_castle):
    valid_coord = False
    while valid_coord == False:
        valid_coord = True
        letters = input(f"enter {stage} position: ")
        if letters == "back":
            return letters
        if can_castle:
            if letters == "0-0" or letters == "0-0-0":
                return letters
        try:
            coord = out.convert_to_coordinates(letters)
        except:
            print("Invalid coordinate.")
            valid_coord = False
            continue
        if coord not in valid_squares:
            valid_coord = False

    return coord

def get_start(active_player,enemy_player,active_positions,enemy_positions,board):
    piece_valid = False
    while piece_valid == False:  # see extras.txt "attribution"
        start_position = get_array("start", active_positions)
        if start_position == "back":
            return get_start(active_player,enemy_player,active_positions,enemy_positions,board)
        elif start_position ==  "0-0":
            return 
        chosen_piece = ext.find_piece(active_player, start_position)

        piece_valid = True
        if chosen_piece == "PieceNotFoundError":
            piece_valid = False
            print("Try Again. NO piece here.")
            continue

        valid_squares = chosen_piece.determine_valid_squares(chosen_piece.position,
                                                                active_player, enemy_player, board)

        valid_coords = []
        for i in valid_squares:
            valid_coords.append(out.convert_to_letters(i))

        if len(valid_squares) > 0:
            print(f"Your {chosen_piece.name} can move to are {valid_coords}.")
        else:
            print(
                f"The {chosen_piece.name} you chose cannot move to any squares ")
            piece_valid = False
    return chosen_piece,valid_squares,start_position

def get_end(active_player,enemy_player,chosen_piece,valid_squares,board,start_position):
    square_valid = False
    while square_valid == False:
        end_position = get_array("end", valid_squares)
        if end_position == "back":
            return play(active_player,enemy_player, board)
        square_valid = True
        if end_position not in valid_squares:
            square_valid = False
            print("sorry, no squares found here.")

    ext.move(chosen_piece, end_position, enemy_player)

    print(f"The {chosen_piece.name} which was on {out.convert_to_letters(start_position)} is now on {out.convert_to_letters(chosen_piece.position)}.\n")

def play(active_player,enemy_player,board):
    is_check = ext.check(active_player, enemy_player, board)

    out.display(active_player, enemy_player, is_check)
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
        enemy_positions.append(i.position)
    
    all_positions = enemy_positions.copy()
    all_positions.extend(active_positions)

    chosen_piece,valid_squares,start_position = get_start(active_player,enemy_player,active_positions,enemy_positions,board)   
    get_end(active_player,enemy_player,chosen_piece,valid_squares,board,start_position)
    
    if active_player == ext.player1 and enemy_player == ext.player2:
        active_player = ext.player2
        enemy_player = ext.player1
    elif active_player == ext.player2 and enemy_player == ext.player1:
        active_player = ext.player1
        enemy_player = ext.player2
    else:
        raise Exception("Neither player is playing rn????")
    return play(active_player,enemy_player,board)

def start_game():
    board = []
    for y in range(8):
        for x in range(8):
            board.append([y+1, x+1])

    ext.player1.name = "Player1"
    ext.player2.name = "Player2"
    active_player = ext.player1
    enemy_player = ext.player2

    all_pieces = []
    for i in ext.white_pieces:
        all_pieces.append(i)
    for i in ext.black_pieces:
        all_pieces.append(i)

    winner,reason = play(active_player,enemy_player,board)
    return winner,reason

def start():
    winner, reason = start_game()
    print(f"Game over. {winner}{reason}")
start()