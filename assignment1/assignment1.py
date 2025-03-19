from os.path import split

def hello():
    return "Hello!"

def greet(name):
    return f"Hello, {name}!"

def calc(first, second, operation = "multiply"):
    try:
        match operation:
            case "add":
                return first + second
            case "subtract":
                return first - second
            case "multiply":
                return first * second
            case "divide":
                return first / second
            case "modulo":
                return first % second
            case "int_divide":
                return first // second
            case _:
                return "error"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"

def data_type_conversion(value, data_type):
    try:
        match data_type:
            case "float":
                return float(value)
            case "str":
                return str(value)
            case "int":
                return int(value)
            case _:
                return "error"
    except ValueError:
        return f"You can't convert {value} into a {data_type}."

def grade(*args):
    try:
        average = sum(args) / len(args)
        if average < 60:
            return "F"
        elif average < 69:
            return "D"
        elif average < 79:
            return "C"
        elif average < 89:
            return "B"
        else:
            return "D"
    except TypeError:
        return "Invalid data was provided."

def repeat(string, count):
    result = ""
    for x in range(count):
        result += string

    return result

def student_scores(positional, **kwargs):
    if positional == "best":
        best_score = 0
        best_name = ""
        for key, value in kwargs.items():
            if value > best_score:
                best_name = key
                best_score = value

        return best_name

    if positional == "mean":
        return sum(kwargs.values()) / len(kwargs)

def titleize(string):
    LITTLE_WORDS =  ("a", "on", "an", "the", "of", "and", "is", "in")
    words = string.split(" ")
    words_len = len(words)
    result = []
    for i, word in enumerate(words):
        if i == 0 or i == words_len - 1:
            result.append(word.capitalize())

            continue

        if word in LITTLE_WORDS:
            result.append(word)

            continue

        result.append(word.capitalize())

    return " ".join(result)

def hangman(secret, guess):
    result = ""

    for letter in secret:
        if letter in guess:
            result = result + letter
        else:
            result = result + "_"

    return result

def pig_latin(string):
    result = []
    VOWELS = "aeiou"

    for word in string.split(" "):
        if word[:1] in VOWELS:
            result.append(word + "ay")
        else:
            counter = 0
            string_to_add = ""
            for i, letter in enumerate(word):
                if letter in VOWELS:
                    break

                if word[i:i+2] == "qu":
                    counter += 2
                    string_to_add = string_to_add + word[i:i+2]

                    break
                else:
                    counter += 1
                    string_to_add = string_to_add + letter

            result.append(("" if counter == 0 else word[counter:]) + string_to_add + "ay")

    return " ".join(result)
