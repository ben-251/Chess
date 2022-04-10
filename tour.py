import external as ext


def start():
	knight = ext.knight("white", True, [4,4],True,"N")
	visited_squares = knight.position

	board = []
	for y in range(8):
        for x in range(8):
            board.append([y+1, x+1])

start()