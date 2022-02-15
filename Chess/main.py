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
        
def invalid_move(function):
    print("Invalid Move.")
    function()

player1 = player(True,"white")
player2 = player(False, "black")

white_bishop_1 = bishop("white",True,[3,1])
white_bishop_2 = bishop("white",True,[6,1])
white_bishops = [white_bishop_1,white_bishop_2]

black_bishop_1 = bishop("black",True,[3,8])
black_bishop_2 = bishop("black",True,[6,8])
black_bishops = [white_bishop_1,white_bishop_2]

def get_array(piece_positions): #I can refine this later but for now need to focus
    
    x_values = []
    y_values = []

    for i in piece_positions:
        x_values.append(i[0])
    for i in piece_positions:
        y_values.append(i[1])

    x_position = int(input("enter first value for start position: "))
    while x_position not in x_values:
        x_position = int(input("Try again.\nEnter first value for start position: "))

    y_position = int(input("enter second value for start position: "))
    while y_position not in y_values:
        y_position = int(input("Try again.\nEnter first value for start position: "))

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
    else: print

def determine_valid_bishop_squares():
    all_squares = [[0,0]]*64
    x = 0
    y = 0

    #generate array with all sqaures
    for i in range(8):
        for i in range(8):
            valid_squares[i] = [x,y]
            x+=1
        

def start():   
    start_position = get_array([white_bishops[0].position,white_bishops[1].position])

    if start_position == white_bishop_1.position:
        chosen_piece = white_bishop_1
    else:
        chosen_piece = white_bishop_2
    
    valid_squares = determine_valid_squares()
    end_position = get_array(valid_squares)
    if chosen_piece.__class__== bishop:
        chosen_piece.position = bishop.move(start_position,end_position)
        swap()
        print("The bishop on",start_position,"is now on",chosen_piece.position)
start()