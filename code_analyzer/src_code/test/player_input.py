import random as rd
import sys

import random as rd
import sys

def main():
    points = 0
    player_input = '' # This has to be initialized for the loop    
    while True:    
        player_input = str(input('Roll or quit (r or q)'))
        if player_input.lower() not in ['r', 'q']:    
            print('invalid choice, try again')
        elif player_input.lower() == 'q': # This will break the loop if the player decides to quit            
            print(f"Your final score: {points} point(s).")
            break
        if player_input.lower() == 'r':    
            roll= rd.randint (1,6)    
            points += roll #(+= sign helps to keep track of score)    
            print('You rolled is ' + str(roll))    
            if roll == 1:    
                print(f'You lost with {points} point(s)!')    
                sys.exit(-1)
                break


if __name__ == "__main__":
    main()