import csv

def add_point(player,csv_file,amount):

    # read the file
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        table = [[e for e in r] for r in reader]

    player_found = False
    for stored_player in table:
        if stored_player[0] == player:
            player_found = True
            stored_player[1] = int(stored_player[1]) + amount
            break

    if player_found == False:
        table.append([player,amount])
        print('New player! {} has just been added to the party!'.format(player))

    # re-write the file
    with open(str(csv_file), 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in table]

def check_money(player_id,csv_file):

    # read the file
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        table = [[e for e in r] for r in reader]

    for stored_player in table:
        if stored_player[0] == player_id:
            return int(stored_player[1])

    # as the command is being counted when checking the balance, one can assume a player will never have 0 messages.
    return 0

def check_for_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
