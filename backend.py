# initialised
import copy
from functools import cache

class player:
	def __init__(self, turn, side, pieces, name, backrank, just_promoted):
		self.turn : bool = turn
		self.side : str = side
		self.pieces : list = pieces
		self.name : str = name
		self.backrank : int = backrank
		self.just_promoted : bool = just_promoted

class board_class:
	def __init__(self, x, y):
		self.squares = []
		self.x: int = x
		self.y: int = y
		for x_val in range(x):
			for y_val in range(y):
				self.squares.append([x_val+1, y_val+1])

	def find_square(desired_square, squares):
		for i in squares:
			if i.position == desired_square.position:
				return i
		return "SquareNotFound"

	def resize(self,new_x, new_y):
		self.squares = []
		for x in range(new_x):
			for y in range(new_y):
				self.squares.append([x+1, y+1])
		self.x = new_x
		self.y = new_y


board = board_class(1, 8)
board.resize(8,8)

class piece:
	def __init__(self, side, position, first_move = None):
		self.side: str = side
		self.position: list = position
		if first_move is None:
			self.first_move = True
		else:
			self.first_move = first_move


class bishop(piece):
	def __init__(self, side, position, first_move = None): 
		super().__init__(side, position, first_move)
		self.name = "bishop"
		if side == "white":
			self.symbol = "b"
		elif side == "black":
			self.symbol = "B"

	@cache
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
			ghost_active_player = copy.deepcopy(active_player)
			ghost_enemy_player = copy.deepcopy(enemy_player)
			ghost_chosen_piece = find_piece(ghost_active_player, init_position)
			move(ghost_chosen_piece, i, ghost_enemy_player)
			if check(ghost_active_player, ghost_enemy_player, board):
				removed_squares.append(i)

		for i in removed_squares:
			if i in squares:
				squares.remove(i)
		return squares


class knight(piece):
	def __init__(self, side, position, first_move = None):
		super().__init__(side, position, first_move)
		self.name = "knight"
		if side == "white":
			self.symbol = "n"
		elif side == "black":
			self.symbol = "N"
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
			ghost_active_player = copy.deepcopy(active_player)
			ghost_enemy_player = copy.deepcopy(enemy_player)
			ghost_chosen_piece = find_piece(ghost_active_player, init_position)
			move(ghost_chosen_piece, i, ghost_enemy_player)
			if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
				removed_squares.append(i)

		for i in removed_squares:
			if i in squares:
				squares.remove(i)
		return squares


class rook(piece):
	def __init__(self, side, position, first_move = None):
		super().__init__(side, position, first_move)
		self.name = "rook"
		if side == "white":
			self.symbol = "r"
		elif side == "black":
			self.symbol = "R"

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
			ghost_active_player = copy.deepcopy(active_player)
			ghost_enemy_player = copy.deepcopy(enemy_player)
			ghost_chosen_piece = find_piece(ghost_active_player, init_position)
			move(ghost_chosen_piece, i, ghost_enemy_player)
			if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
				removed_squares.append(i)

		for i in removed_squares:
			if i in squares:
				squares.remove(i)
		return squares


class queen(piece):
	def __init__(self, side, position, first_move = None):
		super().__init__(side, position, first_move)
		self.name = "queen"
		if side == "white":
			self.symbol = "q"
		elif side == "black":
			self.symbol = "Q"

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
			ghost_active_player = copy.deepcopy(active_player)
			ghost_enemy_player = copy.deepcopy(enemy_player)
			ghost_chosen_piece = find_piece(ghost_active_player, init_position)
			move(ghost_chosen_piece, i, ghost_enemy_player)
			if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
				removed_squares.append(i)

		for i in removed_squares:
			if i in squares:
				squares.remove(i)
		return squares


class pawn(piece):
	def __init__(self, side, position, first_move = None):
		super().__init__(side, position, first_move)
		self.name = "pawn"
		if side == "white":
			self.symbol = "o"
		elif side == "black":
			self.symbol = "O"

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
			ghost_active_player = copy.deepcopy(active_player)
			ghost_enemy_player = copy.deepcopy(enemy_player)
			ghost_chosen_piece = find_piece(ghost_active_player, init_position)
			move(ghost_chosen_piece, i, ghost_enemy_player)
			if i == [3, 5]:
				print(end="")
			is_check = check(ghost_active_player, ghost_enemy_player, board)
			if is_check:
				removed_squares.append(i)

		for i in removed_squares:
			if i in squares:
				squares.remove(i)

		return squares

class king(piece):
	def __init__(self, side, position, first_move = None):
		super().__init__(side, position, first_move)
		self.name = "king"
		if side == "white":
			self.symbol = "k"
		elif side == "black":
			self.symbol = "K"

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
			ghost_active_player = copy.deepcopy(active_player)
			ghost_enemy_player = copy.deepcopy(enemy_player)
			ghost_chosen_piece = find_piece(ghost_active_player, init_position)
			move(ghost_chosen_piece, i, ghost_enemy_player)
			if check(ghost_active_player, ghost_enemy_player, board) and not i in removed_squares:
				removed_squares.append(i)

		for i in removed_squares:
			squares.remove(i)
		return squares

piece_classes = [bishop,knight,pawn,rook,queen,king]
piece_names = ["bishop", "knight", "king", "queen", "rook"]
white_bishop_1 = bishop("white", [3, 1], True)
white_bishop_2 = bishop("white", [6, 1], True)
white_knight_1 = knight("white", [2, 1], True)
white_knight_2 = knight("white", [7, 1], True)
white_rook_1 = rook("white", [1, 1], True)
white_rook_2 = rook("white", [8, 1], True)
white_queen = queen("white", [4, 1], True)
white_king = king("white", [5, 1], True)
white_pawn_1 = pawn("white", [1, 2], True)
white_pawn_2 = pawn("white", [2, 7], True)
white_pawn_3 = pawn("white", [3, 2], True)
white_pawn_4 = pawn("white", [4, 2], True)
white_pawn_5 = pawn("white", [5, 2], True)
white_pawn_6 = pawn("white", [6, 2], True)
white_pawn_7 = pawn("white", [7, 2], True)
white_pawn_8 = pawn("white", [8, 2], True)

white_pieces = [white_pawn_1,
				white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5,
				white_pawn_6, white_pawn_7, white_pawn_8, white_bishop_1, white_bishop_2,
				white_knight_1, white_knight_2,  white_rook_1,
				white_rook_2, white_king, white_queen]

black_bishop_1 = bishop("black", [3, 8], True)
black_bishop_2 = bishop("black", [6, 8], True)
black_knight_1 = knight("black", [2, 8], True)
black_knight_2 = knight("black", [7, 8], True)
black_rook_1 = rook("black", [1, 8], True)
black_rook_2 = rook("black", [8, 8], True)
black_queen = queen("black", [4, 8], True,)
black_king = king("black", [5, 8], True)
black_pawn_1 = pawn("black", [1, 7], True)
black_pawn_2 = pawn("black", [2, 6], True)##
black_pawn_3 = pawn("black", [3, 7], True)
black_pawn_4 = pawn("black", [4, 7], True)
black_pawn_5 = pawn("black", [5, 7], True)
black_pawn_6 = pawn("black", [6, 7], True)
black_pawn_7 = pawn("black", [7, 7], True)
black_pawn_8 = pawn("black", [8, 7], True)

black_pieces = [black_rook_1, black_rook_2,
				black_bishop_1, black_bishop_2, black_knight_1,
				black_knight_2, black_queen, black_king, black_pawn_1,
				black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5,
				black_pawn_6, black_pawn_7, black_pawn_8]

player1 = player(True, "white", white_pieces, "player1", 1, False)
player2 = player(False, "black", black_pieces, "player2", 8, False)

@cache
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


def castle(direction, active_player, enemy_player):
	if direction == "short":
		rook_file = 8
		king_direction = 2
		rook_direction = -2
	elif direction == "long":
		rook_file = 1
		king_direction = -2
		rook_direction = 3
	king_piece = find_piece(active_player, [5, active_player.backrank])
	rook_piece = find_piece(
		active_player, [rook_file, active_player.backrank])

	king_piece.position[0] += king_direction
	rook_piece.position[0] += rook_direction
	return "castled"


def move(piece, position, enemy_player):
	for enemy_piece in enemy_player.pieces:
		if position == enemy_piece.position:
			enemy_player.pieces.remove(enemy_piece)
			break

	piece.position = position
	if piece.first_move == True:
		piece.first_move = False
	return "moved"


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


def squares_between(start, end):
	coords = []
	delta_x = end[0] - start[0]
	delta_y = end[1] - start[1]

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
	while coord != end:
		coords.append(coord)
		coord[0] += sign_x
		coord[1] += sign_y

	return coords


def find_piece(active_player, position):
	for i in active_player.pieces:
		if position == i.position:
			return i
	return "PieceNotFoundError"

def draws(active_player,enemy_player,board):
	is_king = [False, False]
	for square in board:
		piece = find_piece(active_player,square)

		if isinstance(piece,str):
			continue
		if piece.name == "king":
			is_king[0] = True
		
		if piece.name == "king":
			is_king[1] = True
	
	if not all(is_king):
		return "no winner", "missing one or more king(s)"
	
	return False

def get_piece_type(piece_names):
	print("CONGRATULATIONS!! YOU HAVE PROMOTED A PAWN!!")
	piece_valid = False
	while not piece_valid:
		piece_valid = True
		piece_name = input("enter the type of piece to turn it to: ").lower()
		if piece_name not in piece_names:
			piece_valid = False
			print("piece not a valid piece")
	
	for piece in piece_classes:
		sample_piece = piece("",[],True) #refine later
		if sample_piece.name == piece_name:
			return piece
	return "notFOund"

def pawn_promote_check(active_player, enemy_player, chosen_piece):
	if chosen_piece.position[1] == enemy_player.backrank and chosen_piece.name == "pawn":
		active_player.pieces.remove(chosen_piece)
		piece = get_piece_type(piece_names)(active_player.side,chosen_piece.position,False)
		active_player.pieces.append(piece)
		return True,chosen_piece.position
	return False, chosen_piece.position

def can_castle(direction, active_player, enemy_player):
	ghost_active_player = copy.deepcopy(active_player)
	ghost_enemy_player = copy.deepcopy(enemy_player)

	if check(ghost_active_player, ghost_enemy_player, board.squares):
		return False

	if direction == "long":
		rook_position = [1, ghost_active_player.backrank]
	elif direction == "short":
		rook_position = [8, ghost_active_player.backrank]
	else:
		raise Exception("No castle direction")

	king_position = [5, ghost_active_player.backrank]

	king_piece = copy.deepcopy(find_piece(ghost_active_player, king_position))
	if king_piece == "PieceNotFoundError":
		find_piece(ghost_active_player, king_position)
		return False
	if king_piece.name != "king":
		return False
	if not king_piece.first_move:
		return False

	rook_piece = find_piece(ghost_active_player, rook_position)
	if rook_piece == "PieceNotFoundError":
		return False
	if rook_piece.name != "rook":
		return False
	if not rook_piece.first_move:
		return False

	if pieces_between(king_position, rook_position, ghost_active_player, ghost_enemy_player):
		return False

	for square in squares_between(king_position, rook_position):
		move(king_piece, square, ghost_enemy_player)
		if check(ghost_active_player, ghost_enemy_player, board.squares):
			return False

	castle(direction, ghost_active_player, ghost_enemy_player)
	if check(ghost_active_player, ghost_enemy_player, board.squares):
		king_piece.position = [5, ghost_active_player.backrank]
		king_piece.first_move = True
		return False

	return True
