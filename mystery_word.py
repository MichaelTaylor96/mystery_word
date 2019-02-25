from random import *

states = {'game_mode' : "", 'mystery_word' : "", 'current_letters' : [], 'guesses_left' : 8, 'guesses' : [], 'running' : False, 'cl_print' : '', 'easy_words' : [], 'normal_words' : [], 'hard_words' : []}

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

with open('words.txt') as all_words:
    clean_words = [line.strip() for line in all_words]
    states['easy_words'] = [word for word in clean_words if len(word) > 3 and len(word) < 7]
    states['normal_words'] = [word  for word in clean_words if len(word) > 5 and len(word) < 9]
    states['hard_words'] = [word for word in clean_words if len(word) > 7]

def pick_word(mode):
    if mode == "easy":
        return states['easy_words'][randrange(len(states['easy_words']))].upper()
    if mode == "normal":
        return states['normal_words'][randrange(len(states['normal_words']))].upper()
    if mode == "hard":
        return states['hard_words'][randrange(len(states['hard_words']))].upper()

def setup_game(states):
    states['game_mode'] = input("Select difficulty (Easy, Normal, or Hard): ").lower()
    while states['game_mode'] != 'easy' and states['game_mode'] != 'normal' and states['game_mode'] != 'hard':
        states['game_mode'] = input('Mode invalid. Select difficulty (Easy, Normal, or Hard): ').lower()
    states['mystery_word'] = pick_word(states['game_mode'])    
    states['current_letters'] = ['_ ' for _ in states['mystery_word']]
    states['guesses_left'] = 8
    states['guesses'] = []
    states['running'] = True
    return states

def print_cl(states):
    states['cl_print'] = ""
    for i in states['current_letters']:
        states['cl_print'] = states['cl_print'] + i
    print('')
    print(states['cl_print'])
    print('')
    print("You have", states['guesses_left'], "more lives")
    return states
    
def win_check(states):
    states['cl_print'] = ""
    for i in states['current_letters']:
        states['cl_print'] = states['cl_print'] + i    
    if states['cl_print'].replace(" ", "") == states['mystery_word']:
        print('')
        print(states['cl_print'])
        print('')
        print("You Win!") 
        states['running'] = False

def guess_check(guess, states):
    if guess not in states['guesses']:
        states['guesses'].append(guess)
        if guess not in states['mystery_word']:
            print('')
            print("Nope!")
            states['guesses_left'] -= 1
            if states['guesses_left'] == 0:
                print('')
                print(states['mystery_word'])
                print('')
                print("You Lose!")
                states['running'] = False
                return states        
        else:
            i = 0
            while i < len(states['mystery_word']):
                if states['mystery_word'][i] == guess:
                    states['current_letters'][i] = f"{guess} "
                i += 1
            return states
    else:
        print('')
        print("You already guessed that letter.")
        pass

setup_game(states)

while states['running']:
    print_cl(states)
    guess = input("Guess a letter: ").upper()
    while not guess or len(guess) > 1 or guess not in letters:
        guess = input("Guess invalid. Guess again: ").upper()
    guess_check(guess, states)
    win_check(states)
    if not states['running']:
        if input("Would you like to play again? (Y or N): ").upper() == "Y":
            setup_game(states)
            pick_word(states["game_mode"])