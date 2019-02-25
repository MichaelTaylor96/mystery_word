from random import *

states = {'game_mode' : "", 'word_pool' : [], 'current_letters' : [], 'guesses_left' : 8, 'guesses' : [], 'running' : False, 'cl_print' : '', 'easy_words' : [], 'normal_words' : [], 'hard_words' : [], 'word_length' : 0, 'pool_letters' : [], 'word_type' : ''}

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
clean_words = []

with open('words.txt') as all_words:
    clean_words = [line.strip() for line in all_words]
    states['easy_words'] = [word for word in clean_words if len(word) > 3 and len(word) < 7]
    states['normal_words'] = [word  for word in clean_words if len(word) > 5 and len(word) < 9]
    states['hard_words'] = [word for word in clean_words if len(word) > 7]

def pick_word_length(mode):
    if mode == "easy":
        states['word_length'] = len(states['easy_words'][randrange(len(states['easy_words']))])
        return states
    if mode == "normal":
        states['word_length'] = len(states['normal_words'][randrange(len(states['normal_words']))])
        return 
    if mode == "hard":
        states['word_length'] = states['hard_words'][randrange(len(states['hard_words']))].upper()
        return states

def setup_game(states):
    states['game_mode'] = input("Select difficulty (Easy, Normal, or Hard): ").lower()
    while states['game_mode'] != 'easy' and states['game_mode'] != 'normal' and states['game_mode'] != 'hard':
        states['game_mode'] = input('Mode invalid. Select difficulty (Easy, Normal, or Hard): ').lower()
    states['word_length'] = pick_word_length(states['game_mode'])['word_length']
    states['word_pool'] = [word.upper() for word in clean_words if len(word) == states['word_length']]    
    states['word_type'] = f"{'_ ' * states['word_length']}"
    states['guesses_left'] = 8
    states['guesses'] = []
    states['running'] = True
    pool_letters(states)
    return states

def print_cl(states):
    print('')
    print(states['word_type'])
    print('')
    print("You have", states['guesses_left'], "more lives")
    return states
    
def win_check(states):   
    if states['word_type'].replace(" ", "") == states['word_pool'][0] and len(states['word_pool']) == 1:
        print('')
        print(states['word_type'])
        print('')
        print("You Win!") 
        states['running'] = False

def new_pool(guess, word_pool, states):
    sub_pools = {}
    for word in word_pool:
        word_type = ''
        for letter in word:
            if letter == guess:
                word_type = word_type + guess + ' '
            else:
                word_type = word_type + "_ "
        if word_type not in sub_pools:
            sub_pools[word_type] = [word]
        else:
            sub_pools[word_type].append(word)
    key_list = sorted(sub_pools, key=lambda k: len(k[1]), reverse=True)
    states['word_pool'] = sub_pools[key_list[0]]
    states['word_type'] = key_list[0]
    return states

def pool_letters(states):
    for word in states['word_pool']:
        for letter in word:
            if letter not in states['pool_letters']:
                states['pool_letters'].append(letter)

def guess_check(guess, states):
    if guess not in states['guesses']:
        states['guesses'].append(guess)
        states = new_pool(guess, states['word_pool'], states)
        if guess not in states['word_type']:
            print('')
            print("Nope!")
            states['guesses_left'] -= 1
            if states['guesses_left'] == 0:
                print('')
                print(states['word_type'])
                print('')
                print("You Lose!")
                states['running'] = False
                return states 
            return states       
        else:
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
            pick_word_length(states["game_mode"])