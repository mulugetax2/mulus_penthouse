import json
import os
import time
import random
def main():
    
# TODO: allow them to choose from multiple JSON files?
    for file in os.listdir():
        if file.endswith(".json"):
            print(file)
    json_file = input("which file will you open")
    with open(json_file) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

def play(rooms):
    
    current_time = time.time()
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    

    while True:
        times = int(time.time()- current_time)
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        
        # Print the description.
        print(here["description"])
        print ("It has been " + str(times)+ " seconds")
        if here ["items"] == []:
            print ("There is nothing here to take")
        else:
            print ("you can take" + str(here["items"]))


        Cat = random.randint(0,7)
        if Cat == 2:
            print ("You see some cat hairs")
        else:
            if Cat ==1:
                print ("You've come across a black cat")
        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
       # unlocked_exits = usable_exits[0]
       # locked_exits = usable_exits[1]
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break

        if action == "help":
          print_instructions()
          continue
      # TODO: if they type "stuff", print any items they have (check the stuff list!)
        
        if action == "stuff":
            if stuff == []:
                     print ("You have nothing.")
            else:
                print (stuff)
            continue

        
        # TODO: if they type "take", grab any items in the room.
        if action == "take":
            if here ["items"] == []:
                    print ("there is nothing here for you to take")
            else:
                print("you picked up", + here["items"])
                stuff.extend(here['items'])
                here["items"].clear ()
            continue
        
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action == "drop":
            drop = -1
            while drop != 0:
                print("which item do you want to drop?")
                for i, item in enumerate (stuff):
                    print ("  {}. {}".format(i+1, item))
                
                drop = input(">").lower().strip()
                
                if int(drop)> len(stuff) or int(drop) < 0:
                    print ("thats not an item")
                else:
                    drop = int(drop)
                    here["items"].append(stuff[drop-1])
                    stuff.pop(drop-1)
                    drop = 0
                
                
                
            continue 
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable



if __name__ == '__main__':
    main()
