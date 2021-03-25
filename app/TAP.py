# Author:       Adam Anderson
# Date:         Mar 15, 2016
# Module:       taps.py
# Python:       3.4.2

import string
from enum import Enum


# --- DATA OBJECTS
class WordType(Enum):
    """
    An enumeration of WordTypes from the Parts of Speech.
    """
    VERB = 0
    ADJECTIVE = 1
    NOUN = 2
    PREPOSITION = 3
    COMMAND = 5


class SentenceType(Enum):
    """
    An enumeration of sentence types.
    """
    COMMAND = 1
    VERB_NOUN = 2
    VERB_NOUN_PREP_NOUN = 3


class ParserContext(object):
    """
    A class representing any sort of state required for proper parser operation.  The desire is to keep the entire
    parser stateless with the exception of this class - and also to keep this class as simple as possible.
    The ParserContext is not planned to be persisted between application runs, however ,if this state proves to be
    valuable enough to keep between runs of the game, it could be persisted.
    """
    def __init__(self):
        self.last_noun = None


class GameDictionary(object):
    """
    An object that encapsulates the words known by the game.
    This class sort of duplicates functionality in the Parser Context - wondering if this replaces the dictionary
    functions of that class?
    """

    def __init__(self, adjectives=[], commands=[], nouns=[], prepositions=[], verbs=[]):
        """
        Initializes the game dictionary with the supplied Lists of words.
        :param verbs - the list of verbs (Strings) that the game knows.
        :param nouns - the list of nouns (Strings) that the game knows.
        :param adjectives - the list of adjectives (Strings) that the game knows.
        :param prepositions - the list of prepositions (Strings) that the game knows.
        :param commands - the list of commands (Strings) that the game knows.  Commands are special words that are
        detected by the parser because they are special single-word commands that tell the game processor to do
        something unreleated to advancing the story of the game.  For example:  'inventory' might display the player's
        inventory, or 'quit' might exit the game.  Neither of them have anything to do with the player character or what
        is going on in the story right now.
        """
        self.verbs = verbs
        self.nouns = nouns
        self.adjectives = adjectives
        self.prepositions = prepositions
        self.commands = commands


class StatementStructure(object):
    def __init__(self, structure, unrecognized_words=[]):
        """
        Creates a new instance of StatementStructure.
        :param structure - a List of 2-tuples constructed as follows:  WordType instance and a String
        representing the word.
        :param unrecognized_words a List of Strings that were the words in the input that were not
        recognized.
        """
        self.structure = structure

        # TODO this should probably be a tuple so that it is immutable.
        self.unrecognized_words = unrecognized_words

    def get_structure(self):
        """
        Returns a Tuple of the WordTypes that make up the statement structure.
        :return: a Tuple of instances of WordType which define this statement structure's statement's structure.
        """
        s = []
        for word in self.structure:
            s.append(word[0])
        return tuple(s)


class Result(object):
    """
    The object returned by the InputParser.  The game implementation uses this object to determine what happened
    as a result of the user's input.
    """

    def __init__(self, type, verb, direct_obj, preposition=None, indirect_obj=None):
        """ Initializes the Result.
            :param type - the sentence type.
            :param verb - the verb in the sentence.  A verb is required for all supported sentences.  As such, None
            is not valid.
            :param direct_obj - the direct object (the object the verb is modifying or acting upon).  A direct_object
            is present in all supported sentences, so None is not valid for this object.
            :param preposition - a preposition, if one is present.
            :param indirect_obj - a second noun in the sentence, a direct object or object of a preposition.
        """
        self.sentence_type = type
        self.verb = verb
        self.direct_obj = direct_obj
        self.preposition = preposition
        self.indirect_obj = indirect_obj


# --- PROCESSORS
class InputParser(object):
    """
    Class wrapping the function and state of the input parser.
    """

    def __init__(self, game_dict):
        # Store the game dictionary.
        self.game_dict = game_dict

        # Initialize Parser Context
        self.parser_context = ParserContext()

        # Basically only two structures are currently supported VERB NOUN and VERB NOUN PREPOSITION NOUN, but
        # each noun can optionally have an adjective.
        self.valid_structures = [(WordType.COMMAND,),
                                 (WordType.VERB, WordType.NOUN),
                                 (WordType.VERB, WordType.ADJECTIVE, WordType.NOUN),
                                 (WordType.VERB, WordType.NOUN, WordType.PREPOSITION, WordType.NOUN),
                                 (WordType.VERB, WordType.NOUN, WordType.PREPOSITION, WordType.ADJECTIVE, WordType.NOUN),
                                 (WordType.VERB, WordType.ADJECTIVE, WordType.NOUN, WordType.PREPOSITION, WordType.NOUN),
                                 (WordType.VERB, WordType.ADJECTIVE, WordType.NOUN, WordType.PREPOSITION, WordType.ADJECTIVE, WordType.NOUN)]

    def sanitize_input(self, input_string):
        """
        Remove all whitespace, punctuation and other non-essential characters and returns the input string as a list,
        split into words.
        :param input_string: the user's input string to be sanitized.
        :return: a list of clean words.  No punctuation, all lower case.
        """

        # Remove any punctuation characters from the input string.
        # probably shouldn't reconstruct this map every time we sanitize input, but for now, its cool.
        remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
        input_string = input_string.translate(remove_punct_map)

        # Force to lower case.
        input_string = input_string.lower()

        # Split the string into words.
        words = input_string.split(" ")

        return words

    def __determine_structure(self, input_string):
        """
        Determines the structure of an input string, and returns a StatementStructure object describing it.
        :param input_string: the ser input string to parse to generate the StatementStructure object.
        :return:
        """
        words = self.sanitize_input(input_string)
        structure = []
        unrecognized = []

        # If the wordlist is a command, it will be only one word long - this is the only valid one-word structure.
        # If its not a recognized command, return an Unrecognized Structure.
        if len(words) is 1:
            if words[0] in self.game_dict.commands:
                structure.append((WordType.COMMAND, words[0]))
            else:
                unrecognized.append(words[0])

            return StatementStructure(tuple(structure), unrecognized)


        # If the wordlist is a multi-word sentence, process it to the fullest extent.
        nouns_found = 0

        for word in words:
            word = word.lower()
            # VERB
            if word in self.game_dict.verbs:
                structure.append((WordType.VERB, word))

            # NOUN
            elif word in self.game_dict.nouns:
                structure.append((WordType.NOUN, word))

                # Update Parser context with most recently referenced noun.
                nouns_found += 1
                self.parser_context.last_noun = word

            # PREP
            elif word in self.game_dict.prepositions:
                structure.append((WordType.PREPOSITION, word))

            # ADJ
            elif word in self.game_dict.adjectives:
                structure.append((WordType.ADJECTIVE, word))

            # If we didnt recognize the word as a Verb, Noun or Preposition, add it to the unrecognized word list.
            else:
                if word not in unrecognized:
                    unrecognized.append(word)

        # if more than one noun was found in this sentence, follow-on sentences can't just
        # refer to a noun indirectly, so clear the referenced noun.
        if nouns_found > 1:
            self.parser_context.last_noun = None

        return StatementStructure(tuple(structure), unrecognized)

    def parse_input(self, input_string):
        """
        This method takes an input string, sanitizes it, performs checks to ensure it is valid, and generates a
        StatementStructure object.
        :param input_string: the string to parse.
        :return: None
        """

        # Generate Statement Structure
        statement = self.__determine_structure(input_string)

        """
        print("Unrecognized Words", statement.unrecognized_words)
        print("Structure", statement.structure)
        if statement.get_structure() in self.valid_structures:
            print("Structure supported:", statement.get_structure())
        else:
            print("Structure not supported:", statement.get_structure())
        """

        return statement