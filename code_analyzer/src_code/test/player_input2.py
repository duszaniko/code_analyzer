import random as rd

def main():
    points = 0
    player_input = '' # This has to be initialized for the loop   

    while True:    
        player_input = input('Roll or quit (r or q)')
        player_input_corr = player_input.lower()
        if player_input_corr not in ['r', 'q']:    
            print('invalid choice, try again')
        if player_input_corr == 'q': # This will break the loop if the player decides to quit            
            print(f"Your final score: {points} point(s).")
            return points, 0
        if player_input == 'r':    
            roll= rd.randint (1,6)    
            points += roll #(+= sign helps to keep track of score)    
            print('You rolled is ' + str(roll))    
            if roll == 1:    
                print(f'You lost with {points} point(s)!')    
                return points, -1


if __name__ == "__main__":
    main()