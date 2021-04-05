'''
create a function that takes user input and creates rooms on a Grid that can then be explored
The rooms will be numbered, each with a unique number associated with them
'''



from random import randint
from random import shuffle
from math import isqrt



def get_rooms():
    print("How many rooms would you like in your game?")
    while True:
        try:
            num_of_rooms = int(input("> "))
            return num_of_rooms
        except:
            print("That is not a valid number...")


def make_grid(num_of_rooms):
    grid = []
    width = isqrt(num_of_rooms * 2)

    for i in range(width):
        grid.append([0])
        for j in range(width):
            grid[i].append(0)
    
    rooms = [i for i in range(1, num_of_rooms + 1)]
    print(rooms)

    #create a list of possible rooms - 0's are empty spaces    
    
    row, col = randint(0, width -1), randint(0, width)

    for i in rooms:
        #row, col = randint(0, width -1), randint(0, width)

        while grid[row][col] != 0:
            if randint(0, 1) == 1:
                row += randint(-1, 1)
                if row < 0: row += 1
                if row > (width -1): row -=1

            else:
                col += randint(-1, 1)
                if col < 0: col += 1
                if col > width: col -=1

        grid[row][col] = i    
    return grid


def print_grid(grid):
    for i in grid:
        print(i)

def main():
    rooms = get_rooms()
    grid = make_grid(rooms)
    print_grid(grid)


    
    
if __name__ == "__main__":
    main()