class player:
    def __init__(self,turn,side,pieces):
        self.turn = turn
        self.side = side
        self.pieces = pieces

class piece:
    def __init__(self,side,alive,position):
        self.side = side
        self.alive = alive
        self.position = position

class bishop(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,all_pieces,board):
        x = 0
        y = 0
        squares = board
        removed_squares = []

        all_positions = []
        for i in all_pieces:
            all_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if delta_x != delta_y:
                #squares.remove(i) #removing squares in the middle of the loop messes up the index, instead store in an array of sqaures to be removed.
                removed_squares.append(i)
            else:
                # for piece in all_pieces:
                #     piece.position = i

                if i in all_positions:
                    removed_squares.append(i)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares

class knight(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,all_pieces,board):
        x = 0
        y = 0
        squares = board
        removed_squares = []

        all_positions = []
        for i in all_pieces:
            all_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if (not(delta_x == 1 and delta_y ==2)) and (not(delta_x == 2 and delta_y == 1)):
                removed_squares.append(i) 
            else:
                if i in all_positions:
                    removed_squares.append(i)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares        

class rook(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,all_pieces,board):
        x = 0
        y = 0
        squares = board
        removed_squares = []

        all_positions = []
        for i in all_pieces:
            all_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if (not(delta_x > 0 and delta_y == 0)) and (not(delta_x == 0 and delta_y > 0)):
                removed_squares.append(i) 
            else:
                if i in all_positions:
                    removed_squares.append(i)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares        

class queen(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,all_pieces,board):
        x = 0
        y = 0
        squares = board
        removed_squares = []

        all_positions = []
        for i in all_pieces:
            all_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if (not(delta_x > 0 and delta_y == 0)) and (not(delta_x == 0 and delta_y > 0)) and (delta_x != delta_y):
                removed_squares.append(i) 
            else:
                if i in all_positions:
                    removed_squares.append(i)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares     

def get_array(stage,valid_squares): #I can refine this later but for now need to focus   
    x_values = []
    y_values = []

    for i in valid_squares:
        x_values.append(i[0])
    for i in valid_squares:
        y_values.append(i[1])

    x_position = int(input(f"enter first value for {stage} position: "))
    while x_position not in x_values:
        x_position = int(input(f"Try again.\nEnter first value for {stage} position: "))

    y_position = int(input(f"enter second value for {stage} position: "))
    while y_position not in y_values:
        y_position = int(input(f"Try again.\nEnter first value for {stage} position: "))

    return [x_position,y_position]

def swap():
    global player1
    global player2
    global active_player
    if player1.turn == True and player2.turn == False:
        player2.turn = True
        player1.turn = False
        active_player = player2
    elif player1.turn == False and player2.turn == True:
        player2.turn = False
        player1.turn = True
        active_player = player1
    else: 
        raise Exception("Neither player is playing rn????")


def invalid_move(function):
    print("Invalid Move.")
    function()

def find_piece(active_player,position):
    for i in active_player.pieces:
        if position == i.position:
            return i    
    return "PieceNotFoundError"

def moves(): 
    #define full board
    board = []
    for y in range(8):
        for x in range(8):
            board.append([y+1,x+1])

    white_bishop_1 = bishop("white",True,[3,1])
    white_bishop_2 = bishop("white",True,[6,1])
    white_knight_1 = knight("white",True,[2,1])
    white_knight_2 = knight("white",True,[7,1])
    white_rook_1 = rook("white",True,[1,1])
    white_rook_2 = rook("white",True,[8,1])
    white_queen = queen("white",True,[4,1])
    white_pieces = [white_bishop_1,white_bishop_2,white_knight_1,white_knight_2,white_rook_1,white_rook_2,white_queen]

    black_bishop_1 = bishop("black",True,[3,8])
    black_bishop_2 = bishop("black",True,[6,8])
    black_knight_1 = knight("black",True,[2,8])
    black_knight_2 = knight("black",True,[7,8])
    black_rook_1 = rook("black",True,[1,8])
    black_rook_2 = rook("black",True,[8,8])
    black_pieces = [black_bishop_1,black_bishop_2,black_knight_1,black_knight_2]

    player1 = player(True,"white",white_pieces)
    player2 = player(False, "black",black_pieces)

    active_player = player1
    #while game not over
    all_positions = []

    for i in active_player.pieces:
        all_positions.append(i.position)

    all_pieces = []
    for i in white_pieces:
        all_pieces.append(i)
    for i in black_pieces:
        all_pieces.append(i)

    start_position = get_array("start",all_positions) #get_array("start",all_pieces for colour)

    piece_valid = False
    while piece_valid == False: #see extras.txt "attribution"
        chosen_piece = find_piece(active_player,start_position)
        piece_valid = True

        if chosen_piece == "PieceNotFoundError":
            piece_valid = False
            print("Try Again.")

    valid_squares = chosen_piece.determine_valid_squares(chosen_piece.position,white_pieces,board)
    print(f"the squares your piece can move to are{valid_squares}.")

    #end_position = get_array("end",valid_squares)

    #chosen_piece.position = chosen_piece.move(start_position,end_position) #need to make this function, currently doesnt exist
   #print("The piece on",start_position,"is now on",chosen_piece.position)
    #swap()
    #end of while. returns winner when game ends

def start():
    winner = moves()
    print(f"Game over. {winner} won.")

start()