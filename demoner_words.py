def choose_word_dificulty(game_mode, starting_words):
    return starting_words[f'{game_mode}_words']

def pick_word_length(word_pool):
    return len(word_pool[randrange(len(word_pool))])

def setup_pool(length, words):
    return (f'{"_ " * length}', [word for word in words if len(word) == length])

def split_pool(word_pool, guess):
    sub_pools = {}
    for word in word_pool:
        pool_key = ''
        for letter in word:
            if letter == guess:
                pool_key += f"{guess} "
            else:
                pool_key += "_ "
        if pool_key in sub_pools:
            sub_pools[pool_key].append(word)
        else:
            sub_pools[pool_key] = [word]
    sorted_pools = sorted(sub_pools, key=lambda k: len(sub_pools[k]), reverse=True)
    return (sub_pools[sorted_pools[0]])

def smallest_bigpool(word_pool):
    letters = 'abcdefghijklmnopqurstuvwxyz'
    letters_pool_length = {}
    for i in letters:
        i_words = split_pool(word_pool, i)
        letters_pool_length[i] = len(i_words)
    best_letter_for_player = sorted(letters_pool_length, key = lambda k: letters_pool_length[k])[0]
    return letters_pool_length[best_letter_for_player]

def biggest_smallest_bigpool(word_pool, guess):
    sub_pools = {}
    for word in word_pool[1]:
        pool_key = ''
        for letter in word:
            if letter == guess:
                pool_key += f"{guess} "
            else:
                pool_key += "_ "
        if pool_key in sub_pools:
            sub_pools[pool_key].append(word)
        else:
            sub_pools[pool_key] = [word]
    pool_choices = {}
    for i in sub_pools:
        min_max = smallest_bigpool(sub_pools[i])
        pool_choices[i] = min_max
    sorted_choices = sorted(pool_choices, key=lambda k: pool_choices[k], reverse=True)
    return (sorted_choices[0], sub_pools[sorted_choices[0]])

def consolidate_keys(old_pool, new_pool):
    new_key = ''
    i = 0
    while i < len(new_pool):
        if new_pool[i] == old_pool[i]:
            new_key += new_pool[i]
        elif new_pool[i] == '_':
            new_key += old_pool[i]
        else:
            new_key += new_pool[i]
        i += 1
    return new_key


if __name__ == '__main__':
    from random import *

    starting_words = {'easy_words' : [], 'normal_words' : [], 'hard_words' : []}
    states = {'live' : 0, 'guesses' : '', 'word_pool' : (), 'running' : True}

    with open('words.txt') as all_words:
        clean_words = [line.strip() for line in all_words]
        starting_words['easy_words'] = [word.lower() for word in clean_words if len(word) > 3 and len(word) < 7]
        starting_words['normal_words'] = [word.lower() for word in clean_words if len(word) > 5 and len(word) < 9]
        starting_words['hard_words'] = [word.lower() for word in clean_words if len(word) > 7]
    
    initial_list = choose_word_dificulty(input('Enter a difficulty (Easy, Normal, Hard): ').lower(), starting_words)
    states['word_pool'] = setup_pool(pick_word_length(initial_list), initial_list)
    states['lives'] = 8
    letters = 'abcdefghijklmnopqrstuvwxyz'

    while states['running']:
        print()
        print(states['word_pool'][0].upper())
        print("Guessed letters:", states['guesses'].upper())
        print(f"You have {states['lives']} more lives")
        guess = input('Guess a letter: ').lower()
        while guess not in letters or guess.upper() in states['guesses']:
            guess = input('Enter a valid letter: ').lower()
        states['guesses'] += f"{guess.upper()} "
        if states['word_pool'][0] == consolidate_keys(states['word_pool'][0], biggest_smallest_bigpool(states['word_pool'], guess)[0]):
            states['lives'] -= 1
            if states['lives'] == 0:
                print(states['word_pool'][1][randrange(len(states['word_pool'][1]))].upper())
                print('You lose!')
                states['running'] = False
        states['word_pool'] = (consolidate_keys(states['word_pool'][0], biggest_smallest_bigpool(states['word_pool'], guess)[0]), biggest_smallest_bigpool(states['word_pool'], guess)[1])
        if '_ ' not in states['word_pool'][0]:
            print(states['word_pool'][0])
            print('You win!')
            states['running'] = False
        if not states['running']:
            if input('Would you like to play again? (Y / N) ').upper() == 'Y':
                states['running'] = True
                initial_list = choose_word_dificulty(input('Enter a difficulty (Easy, Normal, Hard): ').lower(), starting_words)
                states['word_pool'] = setup_pool(pick_word_length(initial_list), initial_list)
                states['lives'] = 8
                states['guesses'] = ''
