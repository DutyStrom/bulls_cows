"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Petr Boček
email: bocek2@seznam.cz
discord: Seth_Cz#8510
"""

import random
import time

# doplnit funkci na ukádání skóre do souboru
# doplnit funkci na měření času
#number_of_guess = 0

def greet_user() -> str:

    """Greet the user and print the introductory text."""

#     print(
#         f"""\
# Hi there!
# {"-" * 47}
# I've genereted a random 4 digit number for you.
# Let's play a bulls and cows game.
# {"-" * 47}
# Enter a number:
# {"-" * 47}"""
# )
    print(
        f"Hi there!\n"
        f"{"-" * 47}\n"
        f"I've generated a random 4 digit number for you.\n"
        f"Let's play a bulls and cows game.\n"
        f"{"-" * 47}\n"
        f"Enter a number:\n"
        f"{"-" * 47}"
    )


def generate_random_number() -> str:

    """Generate a random four-digit number, every digit is unique."""

    random_number = str()

    while len(random_number) < 4:

        random_digit = str(random.randint(0, 9))

        if len(random_number) == 0 and random_digit == "0":
            continue

        elif random_digit not in random_number:
            random_number += random_digit
    
    return random_number


def request_users_number() -> str:

    users_number = input()

    return users_number


def tests_users_number(users_number: str) -> str:

    """
    Test whether the number entered by the user meets
    the conditions of a suitable number for the game.
    """
    warn = None

    if not users_number.isdigit():
        warn = f"The number must contain only digits. Mooo\n{"-" * 47}"

    elif len(users_number) != 4:
        warn = f"The number must have exactly four digits.\nMooo\n{"-" * 47}"
        
    elif users_number[0] == "0":
        warn = f"The first digit cannot be zero. Mooo\n{"-" * 47}"

    else:
        for digit in users_number:
            if users_number.count(digit) > 1:
                warn = f"The number must contain unique digits only.\nMooo\n{"-" * 47}"
                break

                    
    return warn


def evaluate_users_tip(random_number: str, users_number: str) -> tuple[int]:
    """
    Compares the user's number with a randomly generated number
    and returns the number and type of matches.
    """

    bulls = 0
    cows = 0
   
    for r_index, r_digit in enumerate(random_number):
        
        for u_index, u_digit in enumerate(users_number):
            
            if u_digit == r_digit and u_index == r_index:
                bulls += 1

            elif u_digit == r_digit and u_index != r_index:
                cows += 1
    
    return bulls, cows


def print_tip_result(bulls_cows: tuple[int], number_of_guess: int) -> str:
    """
    Return result of user's tip according to type and number of correct matches.
    """
    
    if bulls_cows[0] == 4:
        result = (
            f"Correct, you've guessed the right number\n"
            f"in {number_of_guess} guesses!\n"
            f"{"-" * 47}"
            )
        
    elif bulls_cows[0] == 1 or bulls_cows[1] == 1:
        if bulls_cows[0] == 1 == bulls_cows[1]:
            result = f"{bulls_cows[0]} bull, {bulls_cows[1]} cow\n{"-" * 47}"
        elif bulls_cows[0] == 1:
            result = f"{bulls_cows[0]} bull, {bulls_cows[1]} cows\n{"-" * 47}"
        else:
            result = f"{bulls_cows[0]} bulls, {bulls_cows[1]} cow\n{"-" * 47}"
    
    else:
        result = f"{bulls_cows[0]} bulls, {bulls_cows[1]} cows\n{"-" * 47}"

    return result


# def count_number_of_guess(bulls: int) -> int:
#     """
#     Returns the number of attempts it took the user 
#     to guess the number.
#     """

#     global number_of_guess

#     if bulls <= 4:
#         number_of_guess += 1

#     return number_of_guess

def main():
    
    greet_user()

    random_number = generate_random_number()
    number_of_guess = 1

    while True:
        
        users_number = request_users_number()
        warn = tests_users_number(users_number)

        if warn != None:
            print(warn)
            continue
        
        else:
            bulls_cows = evaluate_users_tip(random_number, users_number)
            #number_of_guess = count_number_of_guess(bulls_cows[0])
            print(print_tip_result(bulls_cows, number_of_guess))
            
            if bulls_cows[0] != 4:
                number_of_guess += 1
                continue
            
            else:
                break
  

if __name__ == "__main__":
    main()