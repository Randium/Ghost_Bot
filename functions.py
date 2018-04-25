import csv

# Imports a file and presents it as a table.
# If the table has another table as their only argument, it returns the inner table.
# The function returns [] is unsuccessful.
def import_data(csv_file):

    try:
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            table = [[e for e in r] for r in reader]
        return table
    except FileNotFoundError:
        print("ERROR: The program called a file that did not exist: {} does not appear to exist.".format(csv_file))
        return []

# Writes a table to a given file, effectively overwriting its previous contents.
# Returns true if successful, false if unsuccessful.
def save(table,csv_file):

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
        if int(user[0]) == int(user_id) and spot < len(user):
            user[spot] = int(user[spot]) + amount
            save(score_table,fdata)
            return True

    # Add user to the database
    new_length = 0
    for user in score_table:
        new_length = max(new_length,len(user))
    new_player = [user_id,amount]
    for i in range(new_length - 2):
        new_player.append(0)

    print('New user! {} has been added to the database.'.format(user_id))
    score_table.append(new_player)
    save(score_table,fdata)
    return True

    #print("ERROR: User {} not found.".format(user_id))
    #return False


# Takes an emoji as input, and reflects the position of the emoji within the database.
# Returns 0 if unsuccessful.
def position(emoji,femoji):

    emoji_table = import_data(femoji)

    for i in range(len(emoji_table)):
        if emoji_table[i][0] == emoji:
            return i + 2

    return 0


# When given a player and a spot, this function calls how many the user owns of that emoji.
# Returns 0 if unsuccessful.
def count(user_id,spot,fdata):

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
def make_balance(target,fdata,femoji,name):

    score_table = import_data(fdata)
    emoji_table = import_data(femoji)

    if score_table == [] or emoji_table == []:
        print("ERROR: Could not load all files required to show the profile of {}.".format(target))

    # Find the wanted user
    for user in score_table:
        if int(user[0]) == int(target):
            msg = '__**BALANCE:**__\n'
            msg += '\n'
            for i in range(max(len(emoji_table),len(user)-2)):
                if int(user[i+2]) != 0:
                    msg += '{} - {}x\n'.format(emoji_table[i][0],user[i+2])
            msg += '\n'
            msg += 'Money: {}\n'.format(user[1])
            msg += '\n'
            msg += 'Balance Owner: **{}**'.format(name)

            return msg

    print("ERROR: Could not load the balance of {}.".format(target))
    return "ERROR: Could not load the balance of {}.".format(target)


# Looks for the best offer for a specified emoji
# Returns None if none found
# number_only is a boolean; when True, the function is only to return the price
def best_offer(emoji,fmarket,number_only):

    deals_table = import_data(fmarket)

    best_deal = ['0','0',1000001,0]

    for deal in deals_table:
        if int(deal[2]) < int(best_deal[2]) and deal[1] == 's' and deal[0] == emoji:
            best_deal = deal

    if best_deal == ['0','0',1000001,0]:
        if number_only == True:
            return '-'

        print("ERROR: No deal found!")
        return None

    if number_only == True:
        return int(best_deal[2])

    return best_deal


# Looks for the best request for a specified emoji
# Returns None if none found, or '-' if number_only is True.
# number_only is a boolean; when True, the function is only to return the price
def best_request(emoji,fmarket,number_only):

    deals_table = import_data(fmarket)

    best_deal = ['0','0',0,0]

    for deal in deals_table:
        if int(deal[2]) > int(best_deal[2]) and deal[1] == 'b' and deal[0] == emoji:
            best_deal = deal

    if best_deal == ['0','0',0,0]:
        if number_only == True:
            return '-'

        print("ERROR: No deal found!")
        return None

    if number_only == True:
        return int(best_deal[2])

    return best_deal

# Checks if an emoji is a registered emoji in the database.
# If so, it returns true. If not, it returns false.
def isvalid(emoji,femoji):

    emoji_table = import_data(femoji)

    for i in range(len(emoji_table)):
        if emoji_table[i][0] == emoji:
            return True

    return False

# This function responds to a command to buy something.
# Returns a message that is to be put in the trade-center channel.
def buy_something(target,emoji,amount,femoji,fmarket,fdata):

    # The function checks if the emoji is valid, though this SHOULD HAVE BEEN filtered before the function is called.
    if isvalid(emoji,femoji) == False:
        print("An invalid emoji has been detected!")
        return "**ERROR:** An invalid emoji has been detected.", '0', 0

    if best_offer(emoji,fmarket,False) != None:

        deal = best_offer(emoji,fmarket,False)

        if amount >= int(deal[2]):

            # Fulfil the transaction.
            add_score(target.id,1,-1*int(deal[2]),fdata)
            add_score(target.id,position(emoji,femoji),1,fdata)
            add_score(deal[3],1,amount,fdata)

            market_table = import_data(fmarket)
            market_table.remove(deal)
            save(market_table,fmarket)
            return "You have successfully bought {} for {} coins!".format(emoji,int(deal[2])), deal[3], int(deal[2])

    add_score(target.id,1,-amount,fdata)

    market_table = import_data(fmarket)
    market_table.append([emoji,'b',amount,target.id])
    save(market_table,fmarket)
    print("{} has put up a request to buy {} for the price of {}.".format(target,emoji,amount))
    return "We couldn't find an emoji for that price. But don't worry! We've put up a request for you, so that any willing sellers can consider your needs. :hugging:", '0', 0


# This function responds to a command to sell something.
# Returns a message that is to be put in the trade-center channel.
def sell_something(target,emoji,amount,femoji,fmarket,fdata):

    # The function checks if the emoji is valid, though this SHOULD HAVE BEEN filtered before the function is called.
    if isvalid(emoji,femoji) == False:
        print("An invalid emoji has been detected!")
        return "**ERROR:** An invalid emoji has been detected.", '0', 0

    if best_request(emoji,fmarket,False) != None:

        deal = best_request(emoji,fmarket,False)

        if amount <= int(deal[2]):

            # Fulfil the transaction.
            add_score(target.id,1,int(deal[2]),fdata)
            add_score(target.id,position(emoji,femoji),-1,fdata)
            add_score(deal[3],position(emoji,femoji),1,fdata)

            market_table = import_data(fmarket)
            market_table.remove(deal)
            save(market_table,fmarket)
            return "You have successfully sold {} for {} coins!".format(emoji,int(deal[2])), deal[3], int(deal[2])

    add_score(target.id,position(emoji,femoji),-1,fdata)

    market_table = import_data(fmarket)
    market_table.append([emoji,'s',amount,target.id])
    save(market_table,fmarket)
    print("{} has put up an offer to sell {} for the price of {}.".format(target,emoji,amount))
    return "We couldn't find a request for that price. But don't worry! We've put up an offer for you, so that any willing buyers can consider your awesome deal. :wink:", '0', 0


# This function makes the layout of the specific market page branch.
def make_market_branch(emoji,fmarket):

    market = import_data(fmarket)

    if market == []:
        print("ERROR: Could not open file {} while trying to see the market page of {}".format(fmarket,emoji))
        return "Looks like something went wrong! The market file couldn't get loaded. Make sure to let <@248158876799729664> know about this!"

    offers = []
    requests = []


    for deal in market:
        if deal[0] == emoji:
            if deal[1] == 's':
                # Count the number up in the table.
                offercounted = False
                for offer in offers:
                    if offer[0] == int(deal[2]):
                        offercounted = True
                        offer[1] += 1
                        break
                if offercounted == False:
                    offers.append([int(deal[2]),1])

            elif deal[1] == 'b':
                # count the number up in the table.
                requestcounted = False
                for request in requests:
                    if request[0] == int(deal[2]):
                        requestcounted = True
                        request[1] += 1
                        break
                if requestcounted == False:
                    requests.append([int(deal[2]),1])
            else:
                print("An unknown type of trade was found in {}: the type was {}".format(fmarket,deal[1]))

    if offers == [] and requests == []:
        return "*Though we might have this item on the market, there is currently no offer or request being made. Come back later, or make one yourself!*"

    offers.sort()
    requests.sort(reverse = True)

    # Make sure that AT MOST five possible trades are given.
    offer_limit = 4
    request_limit = 4
    if len(offers) < offer_limit + 1:
        offer_limit = len(offers) - 1
    if len(requests) < request_limit + 1:
        request_limit = len(requests) - 1

    msg = '**MARKET EMOJI** {}\n\n**__Offers:__**\n'.format(emoji)

    if offers == []:
        msg += "*There is currently no offer for this emoji. Come back later!*\n"
    else:
        i = offer_limit
        while i >= 0:
            msg += '{}x {}\t{} coins\n'.format(offers[i][1],emoji,offers[i][0])
            i = i - 1

    msg += '\n**__Requests:__**\n'

    if requests == []:
        msg += "*There is currently no request for this emoji. Come back later!*\n"
    else:
        i = 0
        while i <= request_limit:
            msg += '{}x {}\t{} coins\n'.format(requests[i][1],emoji,requests[i][0])
            i = i + 1

    if offers == []:
        offers = [[best_request(emoji,fmarket,True)-1]]
    if requests == []:
        requests = [[best_offer(emoji,fmarket,True)+1]]
    msg += '\nDo you want to buy an offer? Type `!buy {} {}`!\n'.format(emoji,offers[0][0])
    msg += 'Do you want to sell and fulfill a request? Type `!sell {} {}`!'.format(emoji,requests[0][0])

    return msg

# This function shows an overview of the whole market.
# If it cannot display the market for some reason, let it return an error message.
def make_complete_market(femoji,fmarket):

    emojis = import_data(femoji)

    if emojis == []:
        print("ERROR: The emoji file didn't get loaded for the market display.")
        return "Hm, it seems like a file is missing or empty. Make sure to let <@248158876799729664> know about it!"

    msg = '**PLAYER COINS MARKET**\n\n'
    for emoji in emojis:
        msg += '{}\t\tBuy: {} coins\t\tSell: {} coins\n'.format(emoji[0],best_offer(emoji[0],fmarket,True),best_request(emoji[0],fmarket,True))
    msg += '\nTo view the specific market of a specific player coin, please type `!market <emoji>`.'
    return msg

    return "This is the market! It's kinda empty in here...\n*Hint from Randium: he hasn't finished this part yet...*"

# This function removes all deals of a certain player about a certain emoji
def retract_emoji(target,emoji,fmarket,femoji,fdata):
    market = import_data(fmarket)

    msg_table = []

    for deal in market:
        if int(deal[3]) == int(target.id) and emoji == deal[0]:
            if deal[1] == 's':
                add_score(target.id,position(emoji,femoji),1,fdata)
                msg_table.append("Retracted an offer of {} for {} coins!".format(emoji,deal[2]))
            elif deal[1] == 'b':
                add_score(target.id,1,int(deal[2]),fdata)
                msg_table.append("Retracted a request of {} for {} coins!".format(emoji,deal[2]))
            else:
                print("Weird! For some reason, I had to retract a different type!")

            market.remove(deal)

    save(market,fmarket)
    return msg_table
