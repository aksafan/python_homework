def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)

        new_letters = ["_" if l not in guesses else l for l in secret_word]
        result_word = "".join(new_letters)

        print(result_word)

        return result_word

    return hangman_closure

secret_word = input("Set the secret word: \n")
hangman_closure = make_hangman(secret_word)

letter_to_guess = ""
while hangman_closure(letter_to_guess) != secret_word:
    letter_to_guess = input("Guess the letter: \n")

print("You guessed it! Congratz! \n")
