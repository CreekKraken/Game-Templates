#!/usr/bin/python3

from map import rooms
from player import *
from items import *
from gameparser import *

def list_of_items(items):
    output=''
    if items!=[]:
        for player_item in items:
            output+= ", " + str(player_item["name"])

    return output[2:]

def print_room_items(room):
    items_in_room=room["items"]
    if room["items"]!=[]:
        print("There is "+list_of_items(items_in_room),"here.\n")


def print_inventory_items(items):
    output="You have "+list_of_items(items)+".\n"
    print(output)

def print_room(room):
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()
    if room["items"]==[]:
        pass
    else:
        print_room_items(room)

def exit_leads_to(exits, direction):
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    for item in room_items:
        print("TAKE",item["id"].upper(),"to take",item["name"])

    for item in inv_items:
        print("DROP",item["id"].upper(),"to drop",item["name"])
    
    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    return chosen_exit in exits

def execute_go(direction):
    global current_room # moving from room to room without knowing the current room and the list of other rooms is difficult, it turns out
    global rooms
    
    if is_valid_exit(current_room["exits"],direction):
        current_room = rooms[current_room["exits"][direction]]
    else:
        print("You cannot go there.")


def execute_take(item_id):
    global current_room
    present=False
    for i in current_room["items"]:
        if i["id"]==item_id:
            print("item recognised")
            present=True
            
    if present:
        for item in current_room["items"]:
            if item["id"]==item_id:
                inventory.append(item)
                current_room["items"].remove(item)
    else:
        print("You cannot take that, it is not here.")

def execute_drop(item_id):
    global current_room
    present=False
    for i in inventory:
        if i["id"]==item_id:
            print("item recognised")
            present=True
    if present:
        for item in inventory:
            if item["id"]==item_id:
                current_room["items"].append(item)
                inventory.remove(item)
    else:
        print("You cannot drop that, you do not have it.")
    

def execute_command(command):
    global current_room
    if 0 == len(command):
        return

    if command == ["drop","laptop"] and current_room["name"]=="the parking lot":
        win()

    elif command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    print_menu(exits, room_items, inv_items)
    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    # Next room to go to
    return rooms[exits[direction]]

def win():
    print("""congratulations you have dropped your laptop.\n\nyou win the insurance money and a crippling\nself-hatred and fear of dropping things in\nthe future.\n\nhttps://www.youtube.com/watch?v=1Bix44C1EzY""")
    exit()
    

# This is the entry point of our program
def main():

    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)



# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

