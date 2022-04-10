def convert_to_letters(coordinates):
    letters = ""
    letters += chr(coordinates[0]+96)
    letters += str(coordinates[1])
    return letters

def convert_to_coordinates(letters):
    #a = 97, ord("a") = 97, chr(97) = "a"
    #97 - 96 = 1 
    coord = []
    coord.append(ord(letters[0])-96)
    coord.append(int(letters[1]))
    return coord

def display(active_player,enemy_player,is_check):
    active_pieces = []
    enemy_pieces = []

    king_piece = king("blue", False, [1000,10000], False, "ben")
    
    for i in active_player.pieces:
        active_pieces.append(i)
    for i in enemy_player.pieces:
        enemy_pieces.append(i)  

    if is_check:
        for piece in active_pieces:
            if piece.__class__.__name__ == "king":
                king_piece = piee
                init_symbol = king_piece.symbol
                king_piece.symbol = "+"

    all_pieces = []
    all_pieces.extend(active_pieces,enemy_pieces)

    board = []
    for y in range(8):
        for x in range(8):
            board.append([y+1, x+1])

    
    for y in range(8):
        for x in range(8):
            if (x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1):
                print("\n[---{find_piece(all_pieces,[x,y]).symbol}---]")
            else:
                print("\n[   {find_piece(all_pieces,[x,y]).symbol}   ]")
        print("\n")
    

    return
