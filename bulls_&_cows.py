"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Petr Boček
email: bocek2@seznam.cz
discord: Seth_Cz#8510
"""
# Hra Bulls & Cows

# Ve hře hráč hádá náhodné čtyřmístné číslo
# (číslo nezačíná "0" a číslice jsou unikátní). 
# Pokud hráč uhodne číslice, ale ne jejich správné
# umístění hra mu vrátí odpovídající počet "Cows".
# Pokud hráč uhodne číslice i jejich správné umístění
# hra mu vrátí odpovídající počet "Bulls". Jakmile
# hráč číslo uhodne dostane možnost výsledek uložit a
# následně se hra ukončí.

# Při psaní jsem zkoušel různé postupy, na které jsem
# narazil, takže nejsem úplně konzistentí, jen mě to zajímalo :)


import os
import sys
import random
import time
import datetime
import csv
from operator import itemgetter


def greet_user() -> str:

    """Greets the user and print the introductory text."""

    print(
        f"Hi there!\n"
        f"{"-" * 47}\n"
        f"I've generated a random 4 digit number for you.\n"
        f"Let's play a bulls and cows game.\n"
        f"{"-" * 47}\n"
        f"Enter a number:\n"
        f"{"-" * 47}"
    )

    return


def generate_random_number() -> str:    # while cyklus a podmínky by měly zajistit unikátnost číslic

    """
    Generates a random four-digit number, where each digit is unique
    and the number doesn't start with zero.
    """

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
    Tests whether the number entered by the user meets
    the conditions of a suitable number for the game.
    If not, func returns aprropriate warn.
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
        
    elif bulls_cows[0] == 1 or bulls_cows[1] == 1:      # úprava množného/jednotného čísla odpovědi na tip uživatele
        if bulls_cows[0] == 1 == bulls_cows[1]:
            result = f"{bulls_cows[0]} bull, {bulls_cows[1]} cow\n{"-" * 47}"
        elif bulls_cows[0] == 1:
            result = f"{bulls_cows[0]} bull, {bulls_cows[1]} cows\n{"-" * 47}"
        else:
            result = f"{bulls_cows[0]} bulls, {bulls_cows[1]} cow\n{"-" * 47}"
    
    else:
        result = f"{bulls_cows[0]} bulls, {bulls_cows[1]} cows\n{"-" * 47}"

    return result


def request_nickname(blank_nick: str ="") -> str:   # zkoušel jsem rekurzy pro vyžádání jména kvůli uložení výsledku

    """
    Gives the user the option to save the game score and asks for the user's nickname.
    """

    save = input("Do you want save your score? [Y/N] \n")
    print(f"{"-" * 47}")

    if save.upper() == "Y":
        nick_name = input("Enter your nickname\n(max 5 alphanumeric characters): \n")
        print(f"{"-" * 47}")
        if len(nick_name) <= 5 and nick_name.isalnum():
            return nick_name
        else:
            print(
                f"Nickname has to be max 5 characters long!\n"
                f"And all characters has to be alphanumeric only!"
            )
            print()

    
    elif save.upper() == "N":
        print("Thanks for playing Bulls & Cows game. BB")
        sys.exit()

    else:
        print("Options are only Y or N!")
        print()
        nick_name = ""

    return request_nickname(blank_nick + nick_name)


def save_score_csv(                 # vytvoří v adresáři s hrou soubor "savesbc.csv" s uloženými výsledky
        nick_name: str,
        number_of_guess: int,
        final_time: str
        ):
    
    """
    Saves players score to '.csv' file 'savesbc.csv'
    """                                                                          
    
    path_bc = os.path.realpath("savesbc.csv")
    header = ("NICK", "GUESSES", "FINAL TIME")
    player_stats = [nick_name, number_of_guess, final_time]
    
    if not os.path.exists(path_bc):
        with open(path_bc, mode="w", encoding="utf-8", newline='') as saves_csv:
            writer = csv.writer(saves_csv)
            writer.writerows((header, player_stats))

    else:
        with open(path_bc, mode="a", encoding="utf-8", newline='') as saves_csv:
            writer = csv.writer(saves_csv)
            writer.writerow(player_stats)

    return


def retrieve_save(saved_score: str = "savesbc.csv") -> tuple[list[str | int], ...] | str:

    """
    Returns all saved scores from the file savesbc.csv as a tuple.
    If the file doesn't exist, prints an info line.
    """

    try:
        with open(saved_score, mode="r", encoding="utf-8", newline='') as csv_save:
            score_reader = csv.reader(csv_save)
            return tuple(score_reader)

    except FileNotFoundError:       # podle toho jak program pracuje by k výjimce nemělo dojít, ale kdo ví...
        print("File with saved score not found.")
    

def pick_five(raw_data: tuple[list[str | int], ...]) -> tuple[list[str | int], ...]:

    """
    Sorts scores data by number of guesses and final time and return five top scores.
    """
    ordered_scores_data = sorted(raw_data[1:], key= itemgetter(1, 2))       # pochopil jsem, že argumentem pro "key" musí být callable objekt a ten právě vrací "itemgetter"
    #ordered_scores_data_lambda = sorted(test_tuple[1:], key= lambda tup: (tup[1], tup[2]))

    if len(ordered_scores_data) > 5:
        top_five = ordered_scores_data[:5]
    else:
        top_five = ordered_scores_data

    top_five.insert(0, raw_data[0])

    return tuple(top_five)


def print_top_five(top_five: tuple[list[str | int], ...]) -> str:   # zkusil jsem pomocí "for" cyklu a "time.sleep()" napodobit psací stroj 

    """
    Prints the top five scores from the save file if available.
    The printing of individual characters is delayed
    to achieve the "typewriter" effect.
    """

    for row in top_five:
        for record in row:
            for char in record:
                print(char, end="", flush=True); time.sleep(0.085)
            print(f"\t{" ":^8}", end=""); time.sleep(0.35)      # zarovnání textu jsem udělal metodou pokus a omyl, jinak jsem na to nepřišel :(
        print(); time.sleep(0.35)
            
    print(f"{"-" * 47}")
    print("Thanks for playing Bulls & Cows game. BB")
    sys.exit()


def main():
    
    greet_user()

    random_number = generate_random_number()
    number_of_guess = 1     # začíná 1, aby byl započítaný i poslední pokus, kdy je správně uhodnuto číslo
    start = time.time()     # začátek měření doby hádání

    while True:
        
        users_number = request_users_number()
        warn = tests_users_number(users_number)        

        if warn != None:
            print(warn)
            continue
        
        else:
            bulls_cows = evaluate_users_tip(random_number, users_number)
            print(print_tip_result(bulls_cows, number_of_guess))
            
            if bulls_cows[0] != 4:
                number_of_guess += 1
                continue
            
            else:
                end = time.time()       # konec měření doby hádání
                formated_time = str(datetime.timedelta(seconds=round(end-start)))       # zformátování doby hádání knihovnou "datetime"
                print(f"It took you {formated_time}\n{"-" * 47}")   
                break
    
    nick_name = request_nickname()

    save_score_csv(nick_name, number_of_guess, formated_time)

    raw_data = retrieve_save()

    top_five = pick_five(raw_data)

    print_top_five(top_five)

if __name__ == "__main__":
    main()