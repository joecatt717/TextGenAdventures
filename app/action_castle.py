from locations import Location
from items import Item
from game import Game
from class_parser import Parser
#from game import add_item_to_inventory
#from game import describe_something
#from game import destroy_item
#from game import end_game


def build_game():
    # Locations
    cottage = Location("Cottage", "You are standing in a small cottage.")
    garden_path = Location("Garden Path", "You are standing on a lush garden path. There is a cottage here.")
    cliff = Location("Cliff", "There is a steep cliff here. You fall off the cliff and lose the game. THE END.", end_game=True)
    fishing_pond = Location("Fishing Pond", "You are at the edge of a small fishing pond.")
    winding_path = Location("Winding Path", "You are walking along a winding path that leads south and east. There is a tall tree here.")
    tree = Location("A Tall Tree", "You are at the top of a tall tree. From your perch you can see the tower of Action Castle.")
    drawbridge = Location("Drawbridge", "You come to the drawbridge of Action Castle.")
    courtyard = Location("Courtyard", "You are in the courtyard of Action Castle. A castle guard stands watch to the east. Stairs lead up into the tower and down into darkness.")
    great_feasting_hall = Location("Gread Feasting Hall", "You stand inside the great feasting hall.")
    tower_stairs = Location("Tower Stairs", "You climb the tower stairs until you come to a door.")
    dungeon_stairs = Location("Dungeon Stairs", "You are on the dungeon stairs. It's very dark here.")
    tower = Location("Tower", "You are in the tower.")
    dungeon = Location("Dungeon", "You are in the dungeon.")

    # Connections
    cottage.add_connection("out", garden_path)
    garden_path.add_connection("west", cliff)
    garden_path.add_connection("south", fishing_pond)
    garden_path.add_connection("north", winding_path)
    winding_path.add_connection("up", tree)
    winding_path.add_connection("east", drawbridge)
    drawbridge.add_connection("east", courtyard)
    courtyard.add_connection("up", tower_stairs)
    courtyard.add_connection("down", dungeon_stairs)
    courtyard.add_connection("east", great_feasting_hall)
    tower_stairs.add_connection("in", tower)
    dungeon_stairs.add_connection("down", dungeon)

    # Items that you can pick up
    lantern = Item("lantern", "an oil lantern", "IT PROVIDES ADEQUATE LIGHT WHEN NEEDED. MADE IN CHINA.", start_at=cottage)
    fishing_pole = Item("pole", "a fishing pole", "A SIMPLE FISHING POLE.", start_at=cottage)
    potion = Item("potion", "a poisonous potion", "IT'S BRIGHT GREEN AND STEAMING.", start_at=cottage, take_text='As you near the potion, the fumes cause you to faint and lose the game. THE END.', end_game=True)
    rosebush = Item("rosebush", "a rosebush", "THE ROSEBUSH CONTAINS A SINGLE RED ROSE.  IT IS BEAUTIFUL.", start_at=garden_path)
    rose = Item("rose", "a red rose", "IT SMELLS GOOD.",  start_at=None)
    fish = Item("fish", "a dead fish", "IT SMELLS TERRIBLE.", start_at=None)
    branch = Item("branch", "a dead branch", "IT COULD MAKE A GOOD CLUB.", start_at=tree)
    key = Item("key", "a shining key", "YOUR NOT SURE WHERE IT LEADS TO.", start_at=None)
    crown = Item("crown", "a gold crown", "YOU SEE THE GOLD CROWN THAT ONCE BELONGED TO THE KING OF ACTION CASTLE.", start_at=None)
    candle = Item("candle", "a strange candle", "YOU SEE THAT THE STRANGE CANDLE IS COVERED IN MYSTERIOUS RUNES.", start_at=great_feasting_hall)

    # Scenery (not things that you can pick up)
    pond = Item("pond", "a small fishing pond", "THERE ARE FISH IN THE POND.", start_at=fishing_pond, gettable=False)
    troll = Item("troll", "a mean troll", "HE LOOKS ANGRY!", start_at=drawbridge, gettable=False)
    guard = Item("guard", "one of the king's guard", "THE GUARD WEARS CHAINMAIL ARMOR BUT NO HELMET. A KEY HANGS FROM HIS BELT.", start_at=courtyard, gettable=False)
    unconscious_guard = Item("unconcious guard", "an unconscious guard", "THE GUARD LIES MOTIONLESS ON THE GROUND. HIS KEY DANGLES LOOSELY FROM HIS BELT.", start_at=None, gettable=False)
    locked_tower_door = Item("door", "a door", "THE DOOR LOOKS LIKE IT NEEDS A KEY.", start_at=tower_stairs, gettable=False)
    darkness = Item("nothing, IT'S PITCH BLACK DOWN HERE!", "", "", start_at=dungeon_stairs, gettable=False)
    ghost = Item("ghost", "a spooky ghost", "THE GHOST HAS BONY, CLAW-LIKE FINGERS AND WEARS A GOLD CROWN.", start_at=dungeon, gettable=False)

    # Add special functions to your items
    rosebush.add_action("pick rose",  Game.add_item_to_inventory, (rose, "You pick the lone rose from the rosebush.", "You already picked the rose."))
    rose.add_action("smell rose",  Game.describe_something, ("It smells sweet."))
    pond.add_action("catch fish",  Game.describe_something, ("You reach into the pond and try to catch a fish with your hands, but they are too fast."))
    pond.add_action("catch fish with pole",  Game.add_item_to_inventory, (fish, "You dip your hook into the pond and catch a fish.","You weren't able to catch another fish."), preconditions={"inventory_contains":fishing_pole})
    fish.add_action("eat fish",  Game.end_game, ("That's disgusting! It's raw! And definitely not sashimi-grade! But you've won this version of the game. THE END."))
    troll.add_action("give troll a fish", Game.perform_multiple_actions,
        ([(Game.destroy_item, (fish, "You give the troll a tasty fish.", "")),
        (Game.destroy_item, (troll, "The troll runs off to eat his prize.", "")),]), preconditions={"inventory_contains":fish, "location_has_item":troll})
    troll.add_action("hit troll with branch", Game.end_game, ("Not a good idea! The troll rips you limb from limb! THE END."))
    guard.add_action("steal key from guard", Game.end_game, ("That was unwise... The guard locks you in the dungeon and you starve to death! THE END."))
    guard.add_action("hit guard with branch", Game.perform_multiple_actions,
        ([(Game.destroy_item, (branch, "You hit the guard with the branch, and the branch shatters into tiny pieces.", "")),
        (Game.destroy_item, (guard, "The guard slumps to the ground, unconscious.", "")),
        (Game.create_item, (unconscious_guard, "", "")),
        (Game.create_item, (key, "The guard's key falls to the ground", "")),]), preconditions={"inventory_contains":branch, "location_has_item":guard})
    locked_tower_door.add_action("unlock door", Game.destroy_item, (locked_tower_door, "You use the key to unlock the door.", ""),preconditions={"inventory_contains":key})
    lantern.add_action("light lantern", Game.destroy_item, (darkness, "You can now see well enough to continue down the stairs.", ""), preconditions={"inventory_contains":lantern, "in_location":dungeon_stairs})
    ghost.add_action("take crown", Game.end_game, ("The ghost reaches out a skeletal hand and drains your life force. THE END."))
    darkness.add_action("light candle", Game.describe_something, ("The candle's flickering flame is blown out by a draft."), preconditions={"inventory_contains":candle})
    ghost.add_action("light candle", Game.perform_multiple_actions,
        ([(Game.describe_something, ("The candle casts a flickering flame and emits acrid smoke.")),
        (Game.destroy_item, (ghost, "The ghost flees the dungeon, and leaves behind a gold crown.", "")),
        (Game.create_item, (crown, "", "")),]), preconditions={"inventory_contains":candle})
    candle.add_action("light candle", Game.describe_something, ("The candle casts a flickering flame and emits acrid smoke."), preconditions={"inventory_contains":candle})
    '''
    candle.add_action("light candle", Game.perform_multiple_actions,
        ([(Game.describe_something, ("The candle casts a flickering flame and emits acrid smoke.")),
        if Game.current_location == dungeon:
            (Game.destroy_item, (ghost, "The ghost flees the dungeon, and leaves behind a gold crown.", "")),
            (Game.create_item, (crown, "", "")),]), preconditions={"inventory_contains":candle})
        else:
            (Game.describe_something, ("A draft blows the candle out...")),]), preconditions={"inventory_contains":candle}
    '''
    # Blocks
    drawbridge.add_block("east", "There is a troll blocking the bridge. The troll has a warty green hide and looks hungry.", preconditions= {"block_gone":troll})
    tower_stairs.add_block("in", "The door is locked. Maybe it needs a key.", preconditions= {"block_gone":locked_tower_door})
    dungeon_stairs.add_block("down", "It's too dark to see!", preconditions = {"block_gone":darkness})

    return Game(cottage)


def game_loop():
    game = build_game()
    parser = Parser(game)
    game.describe()

    command = ""
    while not (command.lower() == "exit" or command.lower == "q"):
        command = input(">")
        end_game = parser.parse_command(command)
        if end_game:
            return

game_loop()
print('THE GAME HAS ENDED.')