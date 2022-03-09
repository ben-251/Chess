#define full board
board = []
for y in range(8):
    for x in range(8):
        board.append([y+1,x+1])


class player:
    def __init__(self,turn,side):
        self.turn = turn
        self.side = side

class piece:
    def __init__(self,side,alive,position):
        self.side = side
        self.alive = alive
        self.position = position

class bishop(piece):
    def __init__(self,side,alive,position):
       super().__init__(side,alive,position)

    def move(start_position,end_position):
        #check if that position could actually be reached from diagonal movement. 
        #diagonal movement - plus one on both, or minus one on both, or plus one 
        #on one and negative on the other
        delta_x = abs(end_position[0] - start_position[0])
        delta_y = abs(end_position[1] - start_position[1])

        if delta_x != delta_y:
            start()
        return end_position

player1 = player(True,"white")
player2 = player(False, "black")

white_bishop_1 = bishop("white",True,[3,1])
white_bishop_2 = bishop("white",True,[6,1])
white_pieces = [white_bishop_1,white_bishop_2]

black_bishop_1 = bishop("black",True,[3,8])
black_bishop_2 = bishop("black",True,[6,8])
black_pieces = [white_bishop_1,white_bishop_2]

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
    if player1.turn == True and player2.turn == False:
        player2.turn = True
        player1.turn = False
    elif player1.turn == False and player2.turn == True:
        player2.turn = False
        player1.turn = True
    else: 
        raise Exception("Neither player is playing rn????")

def determine_valid_bishop_squares(init_position,all_pieces): #need to find a way to get all the pieces' positions
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

def invalid_move(function):
    print("Invalid Move.")
    function()

def start(): 
    all_positions = []
    for i in white_pieces:
        all_positions.append(i.position)

    start_position = get_array("start",all_positions) #get_array("start",all_piecces for colour)

    if start_position == white_bishop_1.position:
        chosen_piece = white_bishop_1
    else:
        chosen_piece = white_bishop_2
    
    valid_squares = determine_valid_bishop_squares(chosen_piece.position,white_pieces)
    print(f"the squares your bishop can move to are{valid_squares}.")

    end_position = get_array("end",valid_squares)

    cl = chosen_piece.__class__
    if chosen_piece.__class__== bishop:
        chosen_piece.position = bishop.move(start_position,end_position)
        swap()
        print("The bishop on",start_position,"is now on",chosen_piece.position)
start()
