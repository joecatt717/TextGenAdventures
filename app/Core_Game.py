'''
This file is meant to show the basic classes needed to create game objects.
This is the engine of the system. Each module tacked on is an adventure or character class.
Trim the fat here! This should be broad strokes and highly reusable code!
'''

class Game:
    ''' The Game class represents the world. Internally, we use a graph
    of Location objects and Item objects, which can be at a Location or in
    the player's inventory. We will also add an NPC class. These will be
    both friend and foe, with stats and items. These should be moldable like
    clay, so if the Player class tries to mess with them, they can fight back.
    Avoid static characters! Each Location has a set of exits which are directions
    that a Player can move to get to an adjacent location. The Player can
    move from one location to another by typing a command like "Go North". or
    the Player could describe the path like "open the door" or "follow the brick
    road".
    '''

    def __init__(self, start_at):
        #start_at is the location in the game where the player starts
        #alter this in save files for players that are continueing the game later
        self.curr_location = start_at
        self.curr_location.has_been_visited = True
        #inventory is a set of objects that the player has collected
        #this means no duplicate itmes i.e. a set {}
        self.inventory = {}
        #Print the special commands associated with items in the game
        #this will help with debugging and for novice players
        self.print_commands = True

    def describe(self):
        '''Describe the current game state by first describing the current location,
        then listing any Items/Objects in the current location, and then listing any
        exits that the Player can percieve.'''
        self.describe_curr_location()
        self.describe_items()
        self.describe_exits()

    def describe_curr_location(self):
        '''Describe the current location by printing its description field.'''
        print(self.curr_location.description)

    def describe_items(self):
        '''Describe what objects are in the current location.'''
        if len(self.curr_location.items) > 0:
            print("You see: ")
            for item_name in self.curr_location.items:
                item = self.curr_location.items[item_name]
                print(item.description)
                if self.print_commands:
                    special_commands = item.get_commands()
                    for cmd in special_commands:
                        print('\t', cmd)

    def describe_exits(self):
        '''List the directions that the player can take to exit from the current
        location.'''
        exits = []
        for exit in self.curr_location.connections.keys()
            exits.append(exit.capitalize())
        if len(exits) > 0:
            print("Exits: ", end = ' ')
            print(*exits, sep = ", ",)

    def add_to_inventory(self,item):
        '''add an item to the player's inventory.'''
        self.inventory[item.name] = item

    def is_in_inventory(self, item):
        return item.name in self.inventory

    def get_items_in_scope(self):
        '''returns a list of items in the current lovation and in the inventory'''
        items_in_scope = []
        for item_name in self.curr_location.items:
            items_in_scope.append(self.curr_location.items[item_name])
        for item_name in self.inventory:
            items_in_scope.append(self.inventory[item_name])
        return items_in_scope

class Location:
    '''Locations are the places in the game that a player can visit.
    Internally they are represented nodes in a graph. Each location stores
    a description of the location, any items in the location, its connections
    to adjacent locations, and any locks that prevent movement to an adjacent
    location. The connections is a dictionary whose keys are directions and
    whose values are the location that is the result of traveling in that
    direction. The travel_descriptions also has directions as keys, and its
    values are an optional short description of traveling to that location.
    '''
    def __init__(self, name, description, end_game=False):
        # a short name for the location
        self.name = name
        # a description of the location
        self.description = description
        # True if entering this location should end the game
        self.end_game = end_game
        # Dictionary mapping from directions other Location objects
        self.connections = {}
        # Dictionary mapping from directions to text description of the path there
        self.travel_descriptions = {}
        # Dictionary mapping from item name to Item objects present in this location
        self.items = {}
        # Dictionary mapping from direction to Block object in that direction
        self.blocks = {}
        # Flag that gets set to True once this location has been visited by player
        self.has_been_visited = False

    def add_connection(self, direction, connected_location, travel_description=""):
        '''Add a connection from the current location to a connected location.
        Direction is a string that the player can use to get to the connected location.
        If the direction is a cardinal direction, then we also automatically make
        a connection in the reverse direction'''
        self.connections[direction] = connected_location
        self.travel_descriptions[direction] = travel_description
        if direction == 'north':
            connected_location.connections["south"] = self
            connected_location.travel_descriptions['south'] = ""
        if direction == 'south':
            connected_location.connections["north"] = self
            connected_location.travel_descriptions['north'] = ""
        if direction == 'east':
            connected_location.connections['west'] = self
            connected_location.travel_descriptions['west'] = ""
        if direction == 'west':
            connected_location.connections['east'] = self
            connected_location.travel_descriptions['east'] = ""
        if direction == 'up':
            connected_location.connections["down"] = self
            connected_location.travel_descriptions['down'] = ""
        if direction == 'down':
            connected_location.connections["up"] = self
            connected_location.travel_descriptions['up'] = ""
        if direction == 'in':
            connected_location.connections['out'] = self
            connected_location.travel_descriptions['out'] = ""
        if direction == 'out':
            connected_location.connections['in'] = self
            connected_location.travel_descriptions['in'] = ""

    def add_item(self, name, item):
        '''put an item in this location'''
        self.items[name] = item

    def remove_item(self, item):
        '''remove an item from this location (for instance, if the player picks
        it up and puts it in their inventory... or they destroy something, remove it,
        and perhaps add Item (debris) to the scene.)'''
        self.items.pop(item.name)

    def is_blocked(self,direction, game):
        '''check to if there is an obstacle in this direction.'''
        if not direction in self.blocks:
            return False
        (block_desription, preconditions) = self.blocks[direction]
        if check_preconditions(preconditions, game):
            #All the preconditions have been met. you may enter...
            return False
        else:
            #there are still obstacles to overcome or puzzles to solve.
            #Think snorlax blocking the road... you need to play the flute first
            return True

    def get_block_description(self, direction):
        '''check if there is an obstacle in this direction.'''
        if not direction in self.blocks:
            return ""
        else:
            (block_desription, preconditions) = self.blocks[direction]
            return block_desription

    def add_block(self, blocked_direction, block_description, preconditions):
        '''create an obtacle that prevents a player from moving in the blocked
        location until the preconditions are all met.'''
        self.blocks[blocked_direction] = (block_description, preconditions)

def check_preconditions(preconditions, game, print_failure_reasons = True):
    '''checks whether the player has met all of the specified preconditions'''
    all_conditions_met = True
    for check in preconditions:
        # the block bay be overcome by a key or some other object the player collects
        if check == "inventory_contains":
            item = preconditions[check]
            if not game.is_in_inventory(item):
                all_conditions_met = False
                if print_failure_reasons:
                    print("You don't have the %s" % item.name)
        #can't use ELIF here because there may be multiple preconditions, all must be met
        if check == "in_location":
            location = preconditions[check]
            if not game.curr_location == location:
                all_conditions_met = False
                if print_failure_reasons:
                    print("You aren't in the currect location")
        if check == "location_has_item":
            item = preconditions[check]
            if not item.name in game.curr_location.items:
                all_conditions_met = False
                if print_failure_reasons:
                    print("The %s isn't in this location" % item.name)
        ### TODO - add oher types of preconditions
        ## defeated an enemy, completed a story arc, reached a certain level, achieved a certain status
    return all_conditions_met

class Item:
    '''Items are objects that a player can get, or scenery that a player can examine
    or interact with in some way. There is no use describing something that cannot be
    interacted with or that has no purpose. TRIM THE FAT!'''
    def __init__(self,
                name,
                desription,
                examine_text = "",
                take_text = "",
                start_at = None,
                gettable = True,
                end_game = False):
        # The name of the object
        self.name = name
        # The default description of the object
        self.description = desription
        # The detailed description given if the player examines the object
        ## may expand this to include detains of smell, sight, taste, feel, sound
        self.examine_text = examine_text
        # Text that displays when player takes an object.
        self.take_text = take_text if take_text else ("You take the %s." % self.name)
        # Indicates whether a player can get the object and put it in their inventory.
        self.gettable = gettable
        # True if entering this location should end the game
        self.end_game = end_game
        # The location in the Game where the object starts
        if start_at:
            start_at.add_item(name, self)
        self.commands = {}

    def get_commands(self):
        '''Returns a list of special commands associated with this object'''
        return self.commands.keys()

    def add_action(self, command_text, function, arguments, preconditions = {}):
        '''Add a special action associated with this item'''
        self.commands[command_text] = (function, arguments, preconditions)

    def do_action(self, command_text, game):
        ''' perform a special action associated with this item'''
        end_game = False #switches to True if this action ends the game.
        if command_text in self.commands:
            function, arguments, preconditions = self.commands[command_text]
            if check_preconditions(preconditions, game):
                end_game = function(game, arguments)
        else:
            print("Cannot perform the action %s" % command_text)
        return end_game

class Parser:
    '''The parser is the class that handles the player's input. The player
    writes commands, and the parser performs natural language understanding
    in order to interpret what the player intended, and how that intend
    is reflected in the simulated world.
    '''
    def __init__(self, game):
        # A list of all of the commands that the player has issued.
        self.command_history = []
        # A pointer to the game.
        self.game = game

    def get_player_intent(self, command):
        command = command.lower()
        if "," in command:
            # Let the player type in a coma separated sequence of commands
            return "sequence"
        elif self.get_direction(command):
            # Check fo the direction intent
            return "direction"
        elif command.lower() == "look" if command.lower() == "l":
            # when the user issues a "look" command, re=describe what they see
            return "redescribe"
        elif "examine" in command or command.lower().startswith("x "):
            return "examine"
        elif "take " in command or "get " in command:
            return "take"
        elif "drop " in command:
            return "drop"
        elif "inventory" in command or command.lower() == "i":
            return "inventory"
        else:
            for item in self.game.get_items_in_scope():
                special_commands = item.get_commands()
                for special_command in special_commands:
                    if command == special_command.lower():
                        return "special"

    def parse_command(self, command):
        # add this command to the history
        self.command_history.append(command)

        # By default, none of the intents end the game. the following are ways this
        # flag can be changed to True.
        # * Going to a certain place.
        # * Entering a certain special command
        # * Picking up a certain object.

        end_game = False

        # Intents are functions that can be executed
        intent = self.get_player_intent(command)
        if intent == "direction":
            end_game = self.go_in_direction(command)
        elif intent == "redescribe":
            self.game.describe()
        elif intent == "examine":
            self.examine(command)
        elif intent == "take":
            end_game = self.take(command)
        elif intent == "drop":
            self.drop(command)
        elif intent == "special":
            end)game = self.run_special_command(command)
        elif intent == "sequence":
            end_game = self.execute_sequence(command)
        else:
            print("I'm not sure what you want to do.")
        return end_game

    ### Intent Functions ###

    def go_in_direction(self, command):
        ''' The user wants to in some direction '''
        direction = self.get_direction(command)

        if direction:
            if direction in self.game.curr_location.connections:
                if self.game.curr_location.is_blocked(direction, self.game):
                    # check to see whether that direction is blocked.
                    print(self.game.curr_location.get_block_description(direction))
                else:
                    # if it's not blocked, then move there
                    self.game.curr_location = self.game.curr_location.connections[direction]

                    # if moving to this location ends the game, only describe the location
                    # and not the available items or actions.
                    if self.game.curr_location.end_game:
                        self.game.describe_current_location()
                    else:
                        self.game.describe()
                else:
                    print("You can't go %s from here." % direction.capitalize())
                return self.game.curr_location.end_game

    def check_inventory(self, command):
        ''' The player wants to check their inventory'''
        if len(self.game.inventory) == 0:
            print("You don't have anything.")
        else:
            descriptions = []
            for item_name in self.game.inventory:
                item = self.game.inventory[item_name]
                descriptions.append(item.description)
            print("You have: ", end = '')
            print(*descriptions, sep = ", ",)

    def examine(self, command):
        ''' The player wants to examine something '''
        command = command.lower()
        matched_item = False
        # check whether any of the items at this location match the command
        for item_name in self.game.curr_location.items:
            if item_name in command:
                item = self.game.curr_location.items[item_name]
                if item.examine_text
                    print(item.examine_text)
                    matched_item = True
                break
        # check whether any of the items in the inventory match the command
        for item_name in self.game.inventory:
            if item_name in command:
                item = self.game.inventory[item_name]
                if item.examine_text:
                    print(item.examine_text)
                    matched_item = True
        #fail
        if not matched_item:
            print("You don't see anything special.")

        def take(self, command):
            ''' The player wants to put something in their inventory '''
            command = command.lower()
            matched_item = False

            # This gets set to True if posession of this object ends the game.
            end_game = False

            # check whether any of the items at this location match the command
            for item_name in self.game.curr_location.items:
                if item_name in command:
                    item = self.game.curr_location.items[item_name]
                    if item.gettable:
                        self.game.add_to_inventory(item)
                        self.game.curr_location.remove_item(item)
                        print(item.take_text)
                        end_game = item.end_game
                    else:
                        print("You cannot take %s." % item_name)
                    matched_item = True
                    break
            # check whether any of the items in the inventory match the command
            if not matched_item:
                for item_name in self.game.inventory:
                    if item_name in command:
                        print("You already have the %s." % item_name)
                        matched_item = True
            # fail
            if not matched_item
                print("You can't find it.")

            return end_game

        def drop(self, command):
            ''' The player wants to remove something from their inventory '''
            command = command.lower()
            matched_item = False
            # check whether any of the itmes in the inventory match the command
            if not matched_item:
                for item_name in self.game.inventory:
                    if item_name in command:
                        matched_item = True
                        item = self.game.inventory[item_name]
                        self.game.curr_location.add_item(item_name, item)
                        self.game.inventory.pop(item_name)
                        print("You drop the %s." % item_name)
                        break
            # fail
            if not matched_item:
                print("You don't have that.")

        def run_special_command(self, command):
            ''' Run a special command associated with one of the items in this location
            or in the player's inventory '''
            for item in self.game.get_items_in_scope():
                special_command = item.get_commands()
                for special_command in special_commands:
                    if command == special_command.lower():
                        return item.do_action(special_command, self.game)

        def execute_sequence(self, command):
            for cmd in command.split(","):
                cmd = cmd.strip()
                self.parse_command(cmd)

        def get_direction(self, command):
            command = command.lower()
            if command == "n" or "north" in command:
                return "north"
            if command == "s" or "south" in command:
                return "south"
            if command == "e" or "east" in command:
                return "east"
            if command == "w" or "west" in command:
                return "west"
            if command == "up":
                return "up"
            if command == "down":
                return "down"
            if command.startswith("go out"):
                return "out"
            if command.startswith("go in"):
                return "in"
            for exit in self.game.curr_location.connections.keys():
                if command == exit.lower() or command == "go" + exit.lower():
                    return exit
            return None

def add_item_to_inventory(game, *args):
    ''' Add a newly creaed item and add it to your inventory.'''
    (item, action_description, already_done_description) = args[0]
    if(not game.is_in_inventory(item)):
        print(action_description)
        game.add_to_inventory(item)
    else:
        print(already_done_description)
    return False

def describe_something(game, *args):
    '''Describe some aspect of the Item'''
    (description) = args[0]
    print(description)
    return False

def destroy_item(game, *args):
    '''Removes an Item from the game setting its location is set to None.'''
    (item, action_description) = args[0]
    if game.is_in_inventory(item):
        game.inventory.pop(item.name)
        print(action_description)
    elif item.name in game.curr_location.items:
        game.curr_location.remove_item(item)
        print(action_description)
    else:
        print(already_done_description)
    return False

def end_game(game, *args):
    '''Ends the game.'''
    end_message = args[0]
    print(end_message)
    return True



""" GAME DATA """
## This is where we input the actual game ##

def build_game()
    # Locations = Location(Name, Desctiption, end_game = False)
    cottage = Location("Cottage", "You are standing in a small cottage.")
    garden_path = Location("Garden Path", "You are standing on a lush garden path. There is a cottage here.")
    cliff = Location("Cliff", "There is a steep cliff here. You fall off the cliff lose the game. THE END.", end_game=True)
    fishing_pond = Location("Fishing Pond", "You are at the edge of a small fishing pond.")

    # Connections
    cottage.add_connection("out", garden_path)
    garden_path.add_connection("west", cliff)
    garden_path.add_connection("south", fishing_pond)

    # Items that you can pick up
    # Item(name, description, examine_text, take_text, start_at = None, gettable = True, end_game = False
    fishing_pole = Item("pole", "a fishing pole", "A SIMPLE FISHING POLE.", start_at=cottage)
    potion = Item("potion", "a poisonous potion", "IT'S BRIGHT GREEN AND STREAMING.", start_at=cottage, take_text='As you near the potion, the fumes cause you to faint and lose the game. THE END.', end_game=True)
    rosebush = Item("rosebush", "a rosebush", "THE ROSEBUSH CONTAINS A SINGLE RED ROSE. IT IS BEAUTIFUL.", start_at=garden_path)
    rose = Item("rose", "a red rose", "IT SMELLS GOOD.", start_at==None)
    fish = Item("fish", "a dead fish", "IT SMELLS TERRIBLE.", start_at=None)

    # Scenery (not things that you can pick up)
    pond = Item("pond", "a small fishing pond", "THERE ARE FISH IN THE POND.", start_at=fishing_pond, gettable=False)

    # Add special functions to your items
    rosebush.add_action("pick rose", add_item_to_inventory, (rose, "You pick the lone rose from the rosebush.", "You already picked the rose."))
    rose.add_action("smell rose", describe_something, ("It smells sweet."))
    pond.add_action("catch fish", describe_something, ("You reach into the pond and try to catch a fish with your hands, but they are too fast."))
    pond.add_action("catch fish with pole", add_item_to_inventory, (fish, "You dip your hook into the pond and catch a fish.", "You weren't able to catch another fish."), preconditions={"inventory_contains":fishing_pole})
    fish.add_action("eat fish", end_game, ("That's disgusting! It's raw! And definitely not sashimi-grade! But you've won this version of the game. THE END."))

    return Game(cottage)

#!pip install graphviz
from graphviz import Digraph
from Ipython.display import Image
import queue

def DFS(game, graph):
    '''Do a depth-first-search traversal of the locations in the game
    starting at the start lovation, and create a GraphViz graph
    to visualize the connections between the locations, and the items
    that are located at each location'''
    start_location = game.curr_location
    frontier = queue.Queue()
    frontier.put(start_location)
    visited = {}
    visited[start_location.name] = True

    while not frontier.empty():
        current_location = frontier.get()
        game.curr_location = current_location
        name = current_location.name
        description = current_location.description
        items = current_location.items
        items_html = describe_items(current_location)
        html = "<<b>%s</b><br />%s<br />%s>" % (name, description, items_html)
        # Create a new node in the graph for this location
        graph.node(name, label=html)

        connections = current_location.connections
        for direction in connections.keys():
            next_location = connections[direction]
            if not current_location.is_blocked(direction, game):
                # Create an edge between the current location and its successor
                graph.edge(name, next_location.name, label = direction.capitalize())
            else:
                # Create a dotted edge for connected locations that are blocked
                block_description = "%s\n%s" % (direction.capitalize(), current_location.get_block_description(direction))
                graph.edge(name, next_location.name, label=block_description, style = "dotted")
            if not next_location.name in visited:
                visited[next_location.name] = True
                frontier.put(next_location)

def describe_items(location, print_commands = True):
    '''Describe what objects are in teh current location.'''
    items_html = ""
    if len(location.items.keys()) > 0:
        items_html = "You see: "
    for item_name in location.items:
        item = location.items[item_name]
        items_html += item.description
        if print_commands:
            special_commands = item.get_commands()
            for cmd in special_commands:
                items_html += "<br/><i%s</i>" % cmd
    return items_html

def save_to_drive(graph):
    from google.colab import save_to_drive
    drive.mount('/content/drive/')
    graph.render('/content/drive/My Drive/game-visualization', view = True)

graph = Digraph(node_attr={'color': 'lightblue2', 'style': 'filled'})
game = build_game()
DFS(game, graph)
#save_to_drive(graph)
graph