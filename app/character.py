'''
create dictionary values to hold data for character equipment
'''





class Player():

    def __init__(self, name, style, race):
        # Must give a character a name at start up
        self.name = name
        # Equipment is given by a list value in a dictionary with keys equal to each "style" or player-class
        self.equipment = equipment(style)
        # Inventory is given by a list value in a dictionary with keys equal to each "style" or player-class
        self.inventory = startingpack(style)
        # Race will modify a few parameters for the character
        self.race = race
        # Race and Style will contribute to a characters skills, which will be used to calculate success chances for various tasks in game
        self.skills = skills(style) + skills(race)