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