import backend as ext
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


def display(active_player, enemy_player, is_check,board):
    active_pieces = []
    enemy_pieces = []
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

    for i in range(board.x):
        print("._",end = "")
    print(".")
    for y in range(board.y, 0, -1):
        for x in range(1, board.x+1):
            if [x, y] in active_positions:
                player_with_piece = active_player
                is_there = True
            elif [x, y] in enemy_positions:
                player_with_piece = enemy_player
                is_there = True
            else:
                is_there = False

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                color = "-----"
            else:
                color = "     "
            
            if not is_there:
                symbol = color[0]
            else:
                symbol = ext.find_piece(player_with_piece,[x,y]).symbol
            
            print(f"|{symbol}", end="")
        print("|")    
    return
