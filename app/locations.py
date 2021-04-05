from game import Game

class Location:
    """Locations are the places in the game that a player can visit.
    Internally they are represented nodes in a graph.  Each location stores
    a description of the location, any items in the location, its connections
    to adjacent locations, and any blocks that prevent movement to an adjacent
    location.  The connections is a dictionary whose keys are directions and
    whose values are the location that is the result of traveling in that 
    direction.  The travel_descriptions also has directions as keys, and its 
    values are an optional short desciption of traveling to that location.
    """
    def __init__(self, name, description, end_game=False):
        # A short name for the location
        self.name = name
        # A description of the location
        self.description = description
        # True if entering this location should end the game
        self.end_game = end_game
        # Dictionary mapping from directions to other Location objects
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
        """Add a connection from the current location to a connected location.
        Direction is a string that the player can use to get to the connected
        location.  If the direction is a cardinal direction, then we also 
        automatically make a connection in the reverse direction."""
        self.connections[direction] = connected_location
        self.travel_descriptions[direction] = travel_description
        if direction == 'north':
            connected_location.connections["south"] = self
            connected_location.travel_descriptions["south"] = ""
        if direction == 'south':
            connected_location.connections["north"] = self
            connected_location.travel_descriptions["north"] = ""
        if direction == 'east':
            connected_location.connections["west"] = self
            connected_location.travel_descriptions["west"] = ""
        if direction == 'west':
            connected_location.connections["east"] = self
            connected_location.travel_descriptions["east"] = ""
        if direction == 'up':
            connected_location.connections["down"] = self
            connected_location.travel_descriptions["down"] = ""
        if direction == 'down':
            connected_location.connections["up"] = self
            connected_location.travel_descriptions["up"] = ""
        if direction == 'in':
            connected_location.connections["out"] = self
            connected_location.travel_descriptions["out"] = ""
        if direction == 'out':
            connected_location.connections["in"] = self
            connected_location.travel_descriptions["in"] = ""


    def add_item(self, name, item):
        """Put an item in this location."""
        self.items[name] = item

    def remove_item(self, item):
        """Remove an item from this location (for instance, if the player picks it
        up and puts it in their inventory)."""
        self.items.pop(item.name)


    def is_blocked(self, direction, game):
        """Check to if there is an obstacle in this direction."""
        if not direction in self.blocks:
            return False
        (block_description, preconditions) = self.blocks[direction]
        if Location.check_preconditions(preconditions, game):
            # All the preconditions have been met.  You may pass.
            return False
        else: 
            # There are still obstalces to overcome or puzzles to solve.
            return True

    def get_block_description(self, direction):
        """Check to if there is an obstacle in this direction."""
        if not direction in self.blocks:
            return ""
        else:
            (block_description, preconditions) = self.blocks[direction]
        return block_description

    def add_block(self, blocked_direction, block_description, preconditions):
        """Create an obstacle that prevents a player from moving in the blocked 
        location until the preconditions are all met."""
        self.blocks[blocked_direction] = (block_description, preconditions)



    def check_preconditions(preconditions, game, print_failure_reasons=True):
        """Checks whether the player has met all of the specified preconditions"""
        all_conditions_met = True
        for check in preconditions:
            print(check)
            if check == "inventory_contains":
                item = preconditions[check]
                if not game.is_in_inventory(item):
                    all_conditions_met = False
                    if print_failure_reasons:
                        Game.print_slow("You don't have the %s" % item.name)
            if check == "in_location":
                location = preconditions[check]
                if not game.curr_location == location:
                    all_conditions_met = False
                    if print_failure_reasons:
                        Game.print_slow("You aren't in the correct location")
            if check == "location_has_item":
                item = preconditions[check]
                if not item.name in game.curr_location.items:
                    all_conditions_met = False
                    if print_failure_reasons:
                        Game.print_slow("The %s isn't in this location" % item.name)
            if check == "block_gone":
                item = preconditions[check]
                if item.name in game.curr_location.items:
                    all_conditions_met = False
                    if print_failure_reasons:
                        Game.print_slow("The %s is still blocking the way" % item.name)
        # todo - add other types of preconditions
        return all_conditions_met