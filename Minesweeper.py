#Minesweeper, Erik Nygren Ugarte 26/4-17
#Last edited: x/11-17

from random import randint
from tkinter import *                     # * = all


class Field:                              # <---- Gameboard/Field

    def __init__(self, dimension, mines): # <---- dimension and mines as parameters for the class Field 
        self.d = dimension                # <---- Assign private variables to class Field
        self.m = mines                    #       --^^--
        self.grid = self.create_grid()    # <---- Calls function createGrid() and saves the returned value in private variable grid
        self.print_grid()                 # <---- Prints out the grid/matrix
        self.add_mines()                  # <---- Randomizes mines on grid/matrix
        self.print_grid()
        self.calculate_surrounding()      # <---- Calculates each node/tile that isn't a bomb's surrounding
        self.print_grid()


    def create_grid(self):
        return [[Tile() for x in range(self.d)] for y in range(self.d)]    # <---- Create array d tiles and create array of array d times

    #taken from the internet (stackoverflow.com)
    def print_grid(self):
        print('\n'.join([''.join(['{!s:4}'.format(item) for item in row]) for row in self.grid]))

    def add_mines(self):
        mines_left = self.m                      # <---- Counter variable to check how many mines are left to assign to the grid/matrix
        while(mines_left != 0):                  # <---- while loop goes on til all mines are placed in the grid/matrix
            x = randint(0, self.d-1)             # <---- Randomized positions, randint(startvalue --> end value), randint(1, 5) randomizes an int between 1 and 5
            y = randint(0, self.d-1)             # <---- --^^--

            if(self.grid[x][y].type != "M"):     # <---- Runs if the if-statement is True
                self.grid[x][y].type = "M"       # <---- Assign a mine to that tile
                mines_left -= 1                  # <---- Important to not get an endless loop

    def find_neighbours(self, x, y):
        mines = 0
        if(x-1 >= 0):                       
            if self.grid[x-1]  [y].type == "M":
                mines += 1                      
        if(x+1 <= self.d-1):
            if self.grid[x+1]  [y].type == "M":
                mines += 1
        if(y-1 >= 0):
            if self.grid[x]  [y-1].type == "M":     
                mines += 1                          #     /
        if(y+1 <= self.d-1):                        #    / 
            if self.grid[x]  [y+1].type == "M":     #   /----------------- Checks if the 8 positions around each tile contains
                mines += 1                          #   \----------------- a mine, and adds a mine if it does not
        if(x-1 >= 0 and y-1 >= 0):                  #    \                                                 
            if self.grid[x-1][y-1].type == "M":     #     \
                mines += 1                          
        if(x-1 >= 0 and y+1 <= self.d-1):                                                                   
            if self.grid[x-1][y+1].type == "M":
                mines += 1
        if(x+1 <= self.d-1 and y-1 >= 0):                                                                       
            if self.grid[x+1][y-1].type == "M":
                mines += 1
        if(x+1 <= self.d-1 and y+1 <= self.d-1):                                                                   
            if self.grid[x+1][y+1].type == "M":
                mines += 1
        return mines

    def calculate_surrounding(self):                              # <---- Calculates the number of mines around a tile
        for y in range(self.d):
            for x in range(self.d):
                if self.grid[x][y].type == "E":
                    number_of_mines = self.find_neighbours(x, y)
                    if number_of_mines != 0:
                        self.grid[x][y].type = "N"
                        self.grid[x][y].number = number_of_mines

#Tile
class Tile:
    def __init__(self):
        self.type = "E"              # <---- Tile type, E = Empty, M = Mine, N= Number
        self.number = 0              # <---- Number stands for n bombs around the tile
        self.status = 0              # <---- Right click
        self.visible = False         # <---- Left click, if it's visible or not for the user
    def __str__(self):
        return self.type

class GU:                                                # <---- GUI=Graphical User Interface, but I chose to just call it GU
    def left(self, event):
        grid_info = event.widget.grid_info()
        x = grid_info["row"]                             # <---- Left click info
        y = grid_info["column"]
        tile = self.grid[x][y]
        button = event.widget
        
        if tile.type == "N":
            tile.visible = True
            self.handling_buttons(button,tile.number)
            self.tiles_left -= 1

        if tile.type == "M":
            tile.visible = True
            self.handling_buttons(button,tile.type)
            self.show_all_mines()
            print()
            print("BOOM")
            self.show_all_tiles()                        # <---- Shows all tiles if you lose
                
        if tile.type == "E":
            self.check_adjacent_tiles(x,y)               # <---- "E" stands for empty, this triggers the empty slots around this button

        if self.tiles_left == 0:
            print()
            print("YOU WIN")
            self.show_all_tiles()                        # <---- Shows all tiles if you win

    def right(self, event):
        grid_info = event.widget.grid_info()
        x = grid_info["row"]
        y = grid_info["column"]                          # <---- Right click info
        tile = self.grid[x][y]
        button = event.widget
        
        tile.status += 1
        mod = tile.status % 3                                           # <---- Mod3 so the value does not go over 0,1,2
        button["text"] = self.flags[mod]                                # <---- Text type is given in the _init_ function below

        if self.flags[1] == self.flags[mod]:
            self.flagcounter += 1
            
            if tile.type == "M":
                self.flagonmine += 1

        elif self.flags[1] == self.flags[(mod-1)% 3]:
            self.flagcounter -= 1

            if tile.type == "M":
                self.flagonmine -=1

        if self.m == self.flagonmine and self.flagcounter == self.m:
            print()
            print("YOU WIN")
            self.show_all_tiles()

    def handling_buttons(self,button,text):
        button["text"] = text                                           # <---- Gives the button the texttype for number, empty, mine
        button["state"] = "disabled"                                    # <---- "disabled"state needed 
        button["relief"] = "sunken"                                     # <---- "sunken meaning the button has been pressed
        button.unbind('<Button-1>')                                     # <---- Unbind the button to end function for left click
        button.unbind('<Button-3>')                                     # <---- Unbind the button to end function for right click

    def check_adjacent_tiles(self, x, y):
        if(0 <= x and x < self.d and 0 <= y and y < self.d):            # <---- RECURSIVE FUNCTION
            tile = self.grid[x][y]

            if(tile.type == "E" and not tile.visible):                  
                self.handling_buttons(self.buttons[x][y], "")           
                tile.visible = True                                     #    /
                self.tiles_left -= 1                                    #   /
                                                                        #  /
                self.check_adjacent_tiles(x+1,y)                        # /
                self.check_adjacent_tiles(x-1,y)                        #/------------------- Checks if it's "E" and not visited
                self.check_adjacent_tiles(x,y+1)                        #\------------------- which will make it visible
                self.check_adjacent_tiles(x,y-1)                        # \
                                                                        #  \
                self.check_adjacent_tiles(x+1,y+1)                      #   \
                self.check_adjacent_tiles(x+1,y-1)                      #    \
                self.check_adjacent_tiles(x-1,y+1)
                self.check_adjacent_tiles(x-1,y-1)

            if(tile.type == "N" and not tile.visible):
                self.handling_buttons(self.buttons[x][y], tile.number)
                tile.visible = True
                self.tiles_left -= 1

    def show_all_mines(self):                                                          # <---- Function to show all mines when the game is lost
        for y in range(self.d):
            for x in range(self.d):
                if(self.grid[x][y].type == "M"):
                    self.handling_buttons(self.buttons[x][y], self.grid[x][y].type)

    def show_all_tiles(self):                                                          # <---- Function to show all tiles when the game is over
        for y in range(self.d):
            for x in range(self.d):

                if self.grid[x][y].type == "N":
                    self.handling_buttons(self.buttons[x][y], self.grid[x][y].number)

                elif self.grid[x][y].type == "M":
                    self.handling_buttons(self.buttons[x][y], self.grid[x][y].type)

                else:
                    self.handling_buttons(self.buttons[x][y], "")
                    
    def __init__(self,dimension,mines):                                                
        self.field = Field(dimension,mines)
        self.d = dimension
        self.m = mines
        self.grid = self.field.grid
        
        self.flags = ["","⚐","?"]                                                      # <---- Texttype for buttons
        self.flagcounter = 0
        self.flagonmine = 0
        self.tiles_left = dimension*dimension - mines
        
        self.root = Tk()
        self.root.title("MineSweeper")

        self.frame = Frame(self.root, width = 1000, height = 1000)                     # <---- Size for matrix frame
        self.frame.grid()

        self.buttons = [[0 for x in range(self.d)] for y in range(self.d)]             # <---- Buttons' matrix
        
        for y in range(self.d):
            for x in range(self.d):
                button = Button(self.frame, text="", width = 3, height = 1)
                button.grid(row=x, column=y)
                button.bind('<Button-1>', self.left)                                   # <---- Bind left mouse click
                button.bind('<Button-3>', self.right)                                  # <---- Bind right mouse click
                self.buttons[x][y] = button

        self.root.mainloop()

def main():                                                                                                                      
    print("Welcome to Minesweeper!")
    print()
    dimension = input("Please select the size for the row and column in your quadratic gameboard you want to play with: ")
    while not dimension.isdigit():
        print()
        print("Please insert integer!")
        print()
        dimension = input("Please select the size for the row and column in your quadratic gameboard you want to play with: ")
    dimension = int(dimension)
    print()
    mines = input("Select the number of mines you want to play with: ")
    while not mines.isdigit():
        print()
        print("Please insert integer!")
        print()
        mines = input("Select the number of mines you want to play with: ")
    mines = int(mines)

    while (dimension*dimension) < mines:
        print()
        print("Invalid option, the number of mines can't be more than the square of dimension!")
        print()
        main()

    GUI = GU(dimension,mines)

if __name__ == "__main__":                                                             # <---- Main function for better organized code
    main()
