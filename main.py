class player:
    def __init__(self,turn,side,pieces,name):
        self.turn = turn
        self.side = side
        self.pieces = pieces
        self.name = name
class piece:
    def __init__(self,side,alive,position):
        self.side = side
        self.alive = alive
        self.position = position

class bishop(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,side,all_pieces,enemy_pieces,board):
        x = 0
        y = 0
        squares = board
        removed_squares = []

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            delta_y = abs(i[1] - init_position[1])

            if delta_x != delta_y:
                #squares.remove(i) #removing squares in the middle of the loop messes up the index, instead store in an array of sqaures to be removed.
                removed_squares.append(i)
            else:
                # for piece in all_pieces:
                #     piece.position = i

                if i in all_pieces:
                    removed_squares.append(i.position)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares

class knight(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,side,all_pieces,enemy_pieces,board):
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

            if (not(delta_x == 1 and delta_y ==2)) and (not(delta_x == 2 and delta_y == 1)) and not i in removed_squares:
                removed_squares.append(i) 
            else:
                if i in all_positions and not i in removed_squares:
                    removed_squares.append(i)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares        

class rook(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def determine_valid_squares(self,init_position,side,all_pieces,enemy_pieces,board):
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

            if (not(delta_x > 0 and delta_y == 0)) and (not(delta_x == 0 and delta_y > 0)) and (not i in removed_squares):
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

    def determine_valid_squares(self,init_position,side,all_pieces,enemy_pieces,board):
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
                if not i in removed_squares:
                    removed_squares.append(i) 
            else:
                if i in all_positions and not i in removed_squares:
                        removed_squares.append(i)
            
                    
        for i in removed_squares:
            squares.remove(i)
        return squares     

class pawn(piece):
    def __init__(self,side,alive,position,first_move):
        super().__init__(side,alive,position)
        self.first_move = first_move

    def determine_valid_squares(self,init_position,side,all_pieces,enemy_pieces,board):
        '''
        "all" here indicates the player making the move
        '''
        x = 0
        y = 0
        squares = board.copy()
        removed_squares = []

        all_positions = []
        for i in all_pieces:
            all_positions.append(i.position)

        enemy_positions = []
        for i in enemy_pieces:
            enemy_positions.append(i.position)

        for i in squares:
            delta_x = abs(i[0] - init_position[0])
            if side == "white":
                delta_y = i[1] - init_position[1]
            elif side == "black":
                delta_y = init_position[1] - i[1]

            if i in enemy_positions:
                if not(delta_y == 1 and delta_x == 1) and not i in removed_squares:
                    removed_squares.append(i)
            else:
                if self.first_move:
                    if not(delta_y == 1 and delta_x == 0) and not(delta_y == 2 and delta_x == 0) and not i in removed_squares:
                        removed_squares.append(i)
                else:
                    if not(delta_y == 1 and delta_x == 0) and not i in removed_squares:
                        removed_squares.append(i)
            
                if i in all_positions and not i in removed_squares:
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

    x_position = int(input(f"Enter first value for {stage} position: "))
    while x_position not in x_values:
        x_position = int(input(f"Try again.\nEnter first value for {stage} position: "))

    y_position = int(input(f"Enter second value for {stage} position: "))
    while y_position not in y_values:
        y_position = int(input(f"Try again.\nEnter second value for {stage} position: "))

    return [x_position,y_position]

# def swap(active_player,enemy_player,player1,player2):

#     return active_player,enemy_player

def find_piece(active_player,position):
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

def play():  
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
    white_pawn_1 = pawn("white",True,[3,2],True)
    white_pieces = [white_bishop_1,white_bishop_2,white_knight_1,white_knight_2,white_rook_1,white_rook_2,white_queen,white_pawn_1]

    black_bishop_1 = bishop("black",True,[3,8])
    black_bishop_2 = bishop("black",True,[6,8])
    black_knight_1 = knight("black",True,[2,8])
    black_knight_2 = knight("black",True,[7,8])
    black_rook_1 = rook("black",True,[1,8])
    black_rook_2 = rook("black",True,[8,8])
    black_queen = queen("black",True,[4,8])
    black_pawn_1 = pawn("black",True,[1,7],True)
    black_pawn_2 = pawn("black",True,[2,7],True)
    black_pawn_3 = pawn("black",True,[3,7],True)
    black_pawn_4 = pawn("black",True,[4,3],True)
    black_pawn_5 = pawn("black",True,[5,7],True)
    black_pieces = [black_rook_1,black_rook_2,black_bishop_1,black_bishop_2,black_knight_1,black_knight_2,black_queen,black_pawn_1,black_pawn_2,black_pawn_3,black_pawn_4,black_pawn_5]

    player1 = player(True,"white",white_pieces,"player1")
    player2 = player(False, "black",black_pieces,"player2")

    player1.name = input("Enter player1's name: ")
    player2.name = input("Enter player2's name: ")

    active_player = player1
    enemy_player = player2
    #while game not over

    all_pieces = []
    for i in white_pieces:
        all_pieces.append(i)
    for i in black_pieces:
        all_pieces.append(i)

    while True:
        print(f"{active_player.name} is going now.")

        active_positions = []
        for i in active_player.pieces:
            active_positions.append(i.position)

        piece_valid = False
        while piece_valid == False: #see extras.txt "attribution"
            start_position = get_array("start",active_positions) #get_array("start",all_pieces for colour)
            chosen_piece = find_piece(active_player,start_position)
            piece_valid = True

            if chosen_piece == "PieceNotFoundError":
                piece_valid = False
                print("Try Again. NO piece here.")

        valid_squares = chosen_piece.determine_valid_squares(chosen_piece.position,active_player.side, active_player.pieces,enemy_player.pieces,board)
        print(f"the squares your {chosen_piece.__class__.__name__} can move to are{valid_squares}.")

        square_valid = False
        while square_valid == False:
            end_position = get_array("end",valid_squares)
            square_valid = True
            if end_position not in valid_squares:
                square_valid = False
                print("sorry, no squares found here.")
        
        move(chosen_piece, end_position, enemy_player)
        print(f"The {chosen_piece.__class__.__name__} which was on {start_position} is now on {chosen_piece.position}. It should be on {end_position}.")

       # active_player,enemy_player = swap(active_player,enemy_player,player1,player2)
        if active_player == player1 and enemy_player == player2:
            active_player = player2
            enemy_player = player1
        elif active_player == player2 and enemy_player == player1:
            active_player = player1
            enemy_player = player2
        else: 
            raise Exception("Neither player is playing rn????")


    return "placeholder won","by winning."

def start():
    winner,reason = play()
    print(f"Game over. {winner}{reason}")
start()