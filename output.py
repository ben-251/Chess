import spaces as sp
import backend as ext

#~~~~COLOUR~~
import colorama
Back = colorama.Back
Fore = colorama.Fore
Clear = f"{Fore.RESET}{Back.RESET}"

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

def show_valid_options(piece_name,squares,can_castle_short,can_castle_long):
	if len(squares) == 1:
		print(f"the square your {piece_name} can move to is {convert_to_letters(squares[0])}.")
	elif len(squares) == 0:
		print(f"The {piece_name} you chose cannot move to any squares")
	else:
		print(f"your {piece_name} can go to", end = " ")
		for i in range(len(squares)):
			square = convert_to_letters(squares[i])

			if i == len(squares)-1:
				print(square,end = ".\n")
			elif i == (len(squares)-2):
				if len(squares) == 2:
					print(square,end = " and ")
				else:
					print(square,end = ", and ")            
			else:
				print(square,end = ", ")
		
	if can_castle_long:
		print("You can castle long with \"0-0-0.\"")
	if can_castle_short:
		print("You can castle short with \"0-0\"")

def display_board(active_player, enemy_player, is_check,board):
	active_pieces = []
	enemy_pieces = []
	for i in active_player.pieces:
		active_pieces.append(i)
	for i in enemy_player.pieces:
		enemy_pieces.append(i)


	for piece in active_pieces:
		if piece.name == "king":
			king_piece = piece
			init_symbol = king_piece.symbol
	if is_check:
		king_piece.symbol = f"{Fore.BLACK}{Back.RED}{king_piece.symbol}{Clear}"

	active_positions = []
	enemy_positions = []

	for i in active_player.pieces:
		active_positions.append(i.position)
	for i in enemy_player.pieces:
		enemy_positions.append(i.position)

	print("\n  |",end = "")
	for i in range(board.x-1):
		print(chr(i+97),end = " ")
	print(chr(board.x+96))
	
	print("  ._",end = "")
	for i in range(board.x-1):
		print("._",end = "")
	print(".")

	for y in range(board.y, 0, -1):
		print(y,end = " ")
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
				color = f"{Fore.WHITE}{Back.BLACK}"
			else:
				color = f"{Fore.BLACK}{Back.WHITE}"
			
			if not is_there:
				symbol = f"{color} {Clear}"
			else:
				symbol = f"{color}{ext.find_piece(player_with_piece,[x,y]).symbol}{Clear}"
			
			print(f"|{symbol}", end="")
		print("|") 
		
	print("\n  |",end = "")
	for i in range(board.x):
		print(chr(i+97),end = " ")
	print("\n")
	king_piece.symbol = init_symbol
	return

def help():
	pieces = ["pawn","rook","bishop","knight","queen","king"]
	symbols = ["o","r","b","n","q","k"]
	help_menu = {
		"intro": "Welcome to the help menu!\n type play to see how pieces move, controls to see how this program works, and exit to leave",
		"play": "Pawns move forwards 1 square each move, but can go two squares forwards on their first move.\n They capture diagonally.\n gonna write the rest later.",
		"controls": sp.display(pieces, symbols )
	}
	print(help_menu["intro"])
	def help_display():
		choice = input()
		while choice not in help_menu:
			if choice == "exit":
				return
			choice = input(".")
		
		print(help_menu[choice])
		help_display()
	help_display()
