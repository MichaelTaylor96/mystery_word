from random import *

running=True
easy_words = []
normal_words = []
hard_words = []
game_mode = ""
mystery_word = ""
current_letters = []
guesses_left = 8
guesses = []

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
    print("You have", guesses_left, "more lives")

    if cl_print.replace(" ", "") == mystery_word:
        print('')
        print("You Win!") 
        running = False
        # break

    guess = input("Guess a letter: ").upper()

    if guess not in guesses:
        guesses.append(guess)

        if guess not in mystery_word:
            print('')
            print("Nope!")
            guesses_left -= 1
            if guesses_left == 0:
                print("You Lose!")
                running = False
        
        else:
            i = 0
            while i < len(mystery_word):
                if mystery_word[i] == guess:
                    current_letters[i] = f"{guess} "
                i += 1

    else:
        print('')
        print("You already guessed that letter.")

    if not running:
        if input("Would you like to play again? (Y or N): ").upper() == "Y":
                mode_choice = input("Select difficulty (Easy, Normal, or Hard): ")
                mode_choice = mode_choice.lower()
                game_mode = mode_choice

                if game_mode == "easy":
                    mystery_word = easy_words[randrange(len(easy_words))].upper()
                if game_mode == "normal":
                    mystery_word = normal_words[randrange(len(normal_words))].upper()
                if game_mode == "hard":
                    mystery_word = hard_words[randrange(len(hard_words))].upper()

                current_letters = []
                guesses_left = 8
                guesses = []
                running = True
