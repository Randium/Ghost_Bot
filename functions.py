import csv

def add_point(player,csv_file):

    # read the file
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        table = [[e for e in r] for r in reader]

    player_found = False
    for stored_player in table:
        if stored_player[0] == player:
            player_found = True
            stored_player[1] = int(stored_player[1]) + 1
            break

    if player_found == False:
        table.append([player,1])
        print('New player! {} has just been added to the party!'.format(player))

    print(table)

    # re-write the file
    with open(str(csv_file), 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in table]
