import csv

# Imports a file and presents it as a table.
# If the table has another table as their only argument, it returns the inner table.
# The function returns [] is unsuccessful.
def import_data(csv_file):

    try:
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            table = [[int(e) for e in r] for r in reader]
        return table
    except FileNotFoundError:
        print("The program called a file that did not exist.")
        return []

# Writes a table to a given file, effectively overwriting its previous contents.
# Returns true if successful, false if unsuccessful.
def save(table,csv_file)

    # write it
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in table]
    return True


# Changes the score of a certain player on a certain spot. Accepts negative amounts.
# If the user doesn't have a record yet, then they are added to the database.
# Returns true if successful, false if unsuccessful.
def add_score(user_id,spot,amount,fdata):

    score_table = import_data(fdata)

    for user in score_table:
        if user[0] == user_id and spot < len(user):
            user[spot] = int(user[spot]) amount
            save(score_table,fdata)
            return True

    print("ERROR: User {} not found.".format(user_id))
    return False


# Takes an emoji as input, and reflects the position of the emoji within the database.
# Returns 0 if unsuccessful.
def position(emoji,femoji)

    emoji_table = import_data(femoji)

    for i in range(len(emoji_table)):
        if emoji_table[i] == emoji:
            return i + 2

    return 0


# When given a player and a spot, this function calls how many the user owns of that emoji.
# Returns 0 if unsuccessful.
def count(user_id,spot,fdata)

    score_table = import_data(fdata)

    for user in score_table:
        if user[0] == user_id and spot < len(user):
            return int(user[spot])
    return 0


# Checks if a file can be converted into an integer.
# If it cannot, the function returns false.
def check_for_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# Makes the message for the balance command
# Gives error message if unsuccessful.
def make_balance(target,fdata):

    # TODO
    return "ERROR: Could not load the balance of {}.".format(target)


# Looks for the best offer for a specified emoji
# Returns None if none found
# number_only is a boolean; when True, the function is only to return the price
def best_offer(fmarket,number_only):

    # TODO
    return None


# Looks for the best request for a specified emoji
# Returns None if none found
# number_only is a boolean; when True, the function is only to return the price
def best_request(fmarket,number_only):

    # TODO
    return None


# Checks if an emoji is a registered emoji in the database.
# If so, it returns true. If not, it returns false.
def isvalid(emoji,femoji):

    # TODO
    return False


# This function makes the layout of the specific market page branch.
def make_market_branch(emoji,fmarket):

    return "ERROR: Could not print out the market page."
