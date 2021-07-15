import os
#import logging
import argparse
from time import sleep
from random import randint

# Colors
RED = f"\033[;31m"
GRN = f"\033[;32m"
BLU = f"\033[;34m"
GRY = f"\033[;37m"
BLD = f"\033[1m"
END = f"\033[m"

letters_to_numbers = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9
}

def argparser():
    global args
    parser = argparse.ArgumentParser(
        description="Simple battleship game where you have to protect Mars from an Earth attack.",
        epilog="Have fun!")

    parser.add_argument("--no-nerd", action="store_true", help="disable nerd stuff on intro")
    parser.add_argument("--no-ascii", action="store_true", help="disable ascii art")
    parser.add_argument("--mini", action="store_true", help="run game in minimal mode, without fancy stuff")
    parser.add_argument("--hack", dest="hack", action="store_true", help="display ships locations")
    
    args = parser.parse_args()
    if args.mini:
        args.no_nerd = True
        args.no_ascii = True
    return args

class Invader:
    
    def __init__(self, size=5):
        self.size = size
        self.ships = []
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.random_ships(size*2-5)

        """
                       Board reference:

                  A      B      C      D      E
            1 | (0,0), (0,1), (0,2), (0,3), (0,4)
            2 | (1,0), (1,1), (1,2), (1,3), (1,4)
            3 | (2,0), (2,1), (2,2), (2,3), (2,4)
            4 | (3,0), (3,1), (3,2), (3,3), (3,4)
            5 | (4,0), (4,1), (4,2), (4,3), (4,4)
        """
    
    def print_board(self, reveal=False):
        if reveal:
            self.reveal_ships()
        letters = "ABCDEFGHIJ"
        headers = [letters[i] for i in range(self.size)]
        print(BLD, "     " + "     ".join(headers), END)
        for index, row in enumerate(self.board):
            if index == 0:
                print("   ." + "-----."*self.size)
            print(f"{BLD}{index+1:<2}{END} |  {'  |  '.join(row)}  |")
            print("   |" + "-----|"*self.size)
    
    def reveal_ships(self):
        for ship in self.ships:
            y, x = ship
            self.board[y][x] = f"{RED}*{END}"
    
    def cell_check(self, y, x):
        return self.board[y][x]
    
    def create_ship(self, y, x):
        self.ships.append((y, x))
        if args.hack:
            self.board[y][x] = "*"
        #logging.info(f"Ship created at {y}, {x}")

    def destroy_ship(self, y, x):
        self.ships.remove((y, x))
        self.board[y][x] = f"{BLU}X{END}"
        #logging.info(f"Ship destroyed at {y}, {x}")
    
    def random_ships(self, number_of_ships=5):
        """
        Populates the board with n random ships.
        """
        for _ in range(number_of_ships):
            while True:
                x = randint(0, len(self.board)-1)
                y = randint(0, len(self.board[0])-1)
                if not (y, x) in self.ships:
                    self.create_ship(y, x)
                    break
                else:
                    #logging.warning(f"Ship already created at {y}, {x} - trying again")
                    continue

class Game:
    """
    Creates the main engine.
    """
    def run(self):
        os.system("clear")
        self.intro()
        self.lvl = self.difficulty()
        if not args.no_nerd:
            self.nerd_stuff()
        self.play()
    
    def intro(self):
        if args.no_ascii:
            print("Alien Warfare\nProtect Mars from Earth attack!\n")
        else:
            print(r"""
  ___  _ _              _    _             __               
 / _ \| (_)            | |  | |           / _|              
/ /_\ \ |_  ___ _ __   | |  | | __ _ _ __| |_ __ _ _ __ ___ 
|  _  | | |/ _ \ '_ \  | |/\| |/ _` | '__|  _/ _` | '__/ _ \
| | | | | |  __/ | | | \  /\  / (_| | |  | || (_| | | |  __/
\_| |_/_|_|\___|_| |_|  \/  \/ \__,_|_|  |_| \__,_|_|  \___|
                                  
               Protect Mars from Earth attack!
        """)

    def difficulty(self):
        while True:
            try:
                size = int(input("Choose board size (5-10): "))
                if 5 <= size <= 10:
                    return size
                else:
                    print("Invalid value.", end=" ")
                    continue
            except ValueError:
                print("Please enter a number.", end=" ")
                continue
        
    def nerd_stuff(self):
        messages = (
            f"[{GRN}+\033[m] Syncing with Area 51 backdoor...OK",
            f"[{GRN}+\033[m] Intercepting satellite signal...OK",
            f"[{RED}-\033[m] Enumerating targets positions...FAILED",
            f"[{GRN}+\033[m] Gathering targets maximum range...OK",
            f"[{GRN}+\033[m] Building virtual grid...OK"
        )

        sleep(0.5)
        for item in messages:
            print(item)
            sleep(1.2)

    def translate(self, coord):
        """Translates board input, as 'A2', to cartesian points."""
        if len(coord) == 2 and coord[0].isalpha() and coord[1].isdigit():
            y = int(coord[1])-1
            x = letters_to_numbers[coord[0].upper()]
            return y, x
    
    def slow_type(self, message, speed=0.05):
        for char in message:
            print(char, end="", flush=True)
            sleep(speed)
    
    def win(self):
        self.slow_type("\nCongratulations, you destroyed all earthling ships!")
        sleep(0.5)
        self.slow_type("\nAnyone who challenge us will die!")
        sleep(0.5)
        self.slow_type("\nMars is safe... For now.\n")
    
    def gameover(self):
        self.slow_type("\nYou lost your chance to protect Mars, Captain.", 0.07)
        sleep(0.5)
        self.slow_type("\nThe earthlings will reign over us.", 0.07)
        sleep(0.5)
        self.slow_type("\nMars will be gone... And so should you.\n", 0.07)

    def play(self):

        # Initial variables
        max_turns = self.lvl * 2 - 2
        turns = max_turns
        y, x = None, None
        enemy = Invader(self.lvl)
        
        # Game begins
        while turns > 0:
            
            # Update screen
            os.system("clear")
            enemy.print_board()
            
            # If enemy has no ships, he's done
            if not enemy.ships:
                self.win()
                break
            
            print(f"\n{BLU}{len(enemy.ships)}{END} enemy ships remaining")
            print(f"Turn: {turns} / {max_turns}")

            target = input("Target: ")
            try:
                y, x = self.translate(target)
                if enemy.cell_check(y, x):
                    if (y, x) in enemy.ships:
                        enemy.destroy_ship(y, x)
                        print("Ship destroyed!")
                    else:
                        if enemy.board[y][x] == " ":
                            enemy.board[y][x] = "~"
                            print("You missed!")
                            turns -= 1
                        else:
                            print("You already guessed that spot.")
            except:
                print("What are you aiming at? Try again.")
            
            sleep(0.8)
        
        else:
            os.system("clear")
            sleep(0.2)
            enemy.print_board(reveal=True)
            sleep(0.8)
            self.gameover()

if __name__ == "__main__":
    argparser()
    #logging.basicConfig(level=logging.INFO)
    game = Game()
    game.run()
