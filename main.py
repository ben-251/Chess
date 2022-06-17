import backend as ext
import output as out
import copy
from functools import cache
#######doesnt register chack when pawn promotes, maybe it doesnt add it to pieces properly

def get_array(stage, valid_squares):
	valid_coord = False
	while valid_coord == False:
		valid_coord = True
		letters = input(f"enter {stage} position: ")
		if letters == "help":
			out.help()
			valid_coord = False
			continue

		accepted_words = ["back", "0-0", "0-0-0"]
		if letters in accepted_words:
			return letters

		try:
			coord = out.convert_to_coordinates(letters)
		except:
			print("Invalid coordinate.")
			valid_coord = False
			continue
		if coord not in valid_squares:
			if stage == "start":
				print("you don't have a piece on that square")
			valid_coord = False
	return coord

def get_selected_piece(active_player, active_positions):
	piece_valid = False
	while piece_valid == False:  # see extras.txt "attribution"
		start_position = get_array("start", active_positions)
		if start_position == "back":
			return get_selected_piece(active_player, active_positions)
		selected_piece = ext.find_piece(active_player, start_position)

		piece_valid = True
		if selected_piece == "PieceNotFoundError":
			piece_valid = False
			print("Try Again. NO piece here.")
			continue
	return selected_piece,start_position

def verify_piece(active_player, enemy_player, board, selected_piece, can_castle_short, can_castle_long):
	piece_valid = True
	active_positions = []
	for i in active_player.pieces:
		active_positions.append(i.position)

	valid_squares = selected_piece.determine_valid_squares(selected_piece.position,
															active_player, enemy_player, board)
	valid_coords = []
	for i in valid_squares:
		valid_coords.append(out.convert_to_letters(i))
	out.display_squares(selected_piece.name, valid_squares,
						can_castle_short, can_castle_long)
	if len(valid_squares) == 0 and not can_castle_short and not can_castle_long:
		piece_valid = False
	
	if not piece_valid:
		return False

	return valid_squares

def process_end_position(active_player, enemy_player, selected_piece, valid_squares, board, start_position, is_check):
	square_valid = False
	while square_valid == False:
		square_valid = True
		end_position = get_array("end", valid_squares)
		if end_position == "back":
			return play(active_player, enemy_player, is_check)

		elif end_position == "0-0-0":
			if ext.can_castle("long", active_player, enemy_player):
				return ext.castle("long", active_player, enemy_player)
			else:
				print("you cant castle long right now")
				square_valid = False
				continue

		elif end_position == "0-0":
			if ext.can_castle("short", active_player, enemy_player):
				return ext.castle("short", active_player, enemy_player)
			else:
				print("you can't castle that way right now")
				square_valid = False
				continue

		if end_position not in valid_squares:
			square_valid = False
			print("sorry, you cant move here..")

	return ext.move(selected_piece, end_position, enemy_player)

def play(active_player, enemy_player, is_check):
	can_castle_short = ext.can_castle("short", active_player, enemy_player)
	can_castle_long = ext.can_castle("long", active_player, enemy_player)

	# if not can_castle_long and not can_castle_short:
	# 	print("You can't castle on this move.")
	all_moves = []

	for i in active_player.pieces:
		all_moves.append(i.determine_valid_squares(
			i.position, active_player, enemy_player, ext.board.squares))

	total_moves = 0
	for i in all_moves:
		total_moves += len(i)

	if total_moves == 0:
		if is_check:
			return f"{enemy_player.name} won", "checkmate."
		else:
			return "draw", "stalemate."


	if not ext.draws(active_player,enemy_player,ext.board.squares) == False:
		return ext.draws(active_player,enemy_player,ext.board.squares)
	print(f"{active_player.name} is going now.")
	if is_check:
		print("you are in check.")
	
	active_positions = []
	for i in active_player.pieces:
		active_positions.append(i.position)

	enemy_positions = []
	for i in enemy_player.pieces:
		enemy_positions.append(i.position)

	all_positions = enemy_positions.copy()
	all_positions.extend(active_positions)

	selected_piece, start_position = get_selected_piece(active_player, active_positions)
	valid_squares = verify_piece(active_player, enemy_player, ext.board.squares, selected_piece, can_castle_short, can_castle_long)
	while valid_squares == False:
		selected_piece, start_position = get_selected_piece(active_player, active_positions)
		valid_squares = verify_piece(active_player, enemy_player, ext.board.squares, selected_piece, can_castle_short, can_castle_long)

	action = process_end_position(active_player, enemy_player, selected_piece,
					 valid_squares, ext.board.squares, start_position, is_check)

	active_player.just_promoted,pawn_destination = ext.pawn_promote_check(active_player, enemy_player, selected_piece)

	if not active_player.just_promoted:
		if action == "moved":
			print(f"The {selected_piece.name} which was on {out.convert_to_letters(start_position)} is now on {out.convert_to_letters(selected_piece.position)}.\n")
		elif action == "castled":
			print("Successfully Castled.")
	else:
		print(f"The pawn which was on {out.convert_to_letters(start_position)} is now a {ext.find_piece(active_player, pawn_destination).name} on {out.convert_to_letters(pawn_destination)}")

	is_check = ext.check(active_player, enemy_player, ext.board.squares)
	out.display(active_player, enemy_player, is_check, ext.board)
	active_player.just_promoted = False

	#swap
	if active_player == ext.player1 and enemy_player == ext.player2:
		active_player = ext.player2
		enemy_player = ext.player1
	elif active_player == ext.player2 and enemy_player == ext.player1:
		active_player = ext.player1
		enemy_player = ext.player2
	else:
		raise Exception("Neither player is playing rn????")

	return play(active_player, enemy_player, is_check)


def start_game():
	ext.player1.name = "Player1"
	ext.player2.name = "Player2"
	active_player = ext.player1
	enemy_player = ext.player2

	all_pieces = []
	for i in ext.white_pieces:
		all_pieces.append(i)
	for i in ext.black_pieces:
		all_pieces.append(i)

	is_check = ext.check(active_player, enemy_player, ext.board.squares)
	out.display(active_player, enemy_player, is_check, ext.board)
	winner, reason = play(active_player, enemy_player,
						is_check)
	return winner, reason

def main():
	print("enter \"help\" to see the help menu.")
	winner, reason = start_game()
	print(f"Game over. {winner} by {reason}")


if __name__ == "__main__":
	main()
