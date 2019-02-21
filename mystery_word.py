from random import *

running=True
easy_words = []
normal_words = []
hard_words = []
game_mode = ""
mystery_word = ""
current_letters = []
guesses = 8

with open("words.txt") as all_words:
        line = all_words.readline()
        while line:            
            line = line.replace("\n", "")
            if len(line) > 3 and len(line) < 7:
                easy_words.append(line)
            if len(line) > 5 and len(line) < 9:
                normal_words.append(line)
            if len(line) > 7:
                hard_words.append(line)
            line = all_words.readline()

mode_choice = input("Select difficulty (Easy, Normal, or Hard): ")
mode_choice = mode_choice.lower()
game_mode = mode_choice

if game_mode == "easy":
    mystery_word = easy_words[randrange(len(easy_words))].upper()
if game_mode == "normal":
    mystery_word = normal_words[randrange(len(normal_words))].upper()
if game_mode == "hard":
    mystery_word = hard_words[randrange(len(hard_words))].upper()

while running:

    if not current_letters:
        for i in mystery_word:
            current_letters.append('_ ')

    cl_print = ""
    for i in current_letters:
        cl_print = cl_print + i
    print('')
    print(cl_print)
    print('')
    print("You have", guesses, "more lives")

    if cl_print.replace(" ", "") == mystery_word:
        print("You Win!")
        running = False
        break

    guess = input("Guess a letter: ").upper()

    if guess not in mystery_word:
        print("Nope!")
        guesses -= 1
        if guesses == 0:
            print("You Lose!")
            running = False
    
    else:
        i = 0
        while i < len(mystery_word):
            if mystery_word[i] == guess:
                current_letters[i] = f"{guess} "
            i += 1
