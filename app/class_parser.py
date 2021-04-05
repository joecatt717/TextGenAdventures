'''
here is my own attempt to create a parser
'''

class Parser(object):
    '''
    create a parser object using the player's input (command)
    the parser will dice this up into subject, verb, direct_obj, indirect_obj
    '''

    verbs = {
        "go" : ["go", "move", "walk", "run", "stumble", "flee"],
        "eat" : ["eat", "consume", "ingest", "devour"],
        "get" : ["get", "aquire", "grab", "pick", "take", "snatch"],
    }

    items = {
        "tiger" : ["tiger", "cat", "leapard", "lion", "beast"],
        "potion" : ["potion", "concoction", "brew", "elixer"]
    }


    def __init__(self, command):
        self.no_punctuation = self.remove_punctuation(command)
        self.tokens = self.no_punctuation.split()
        self.verb = self.get_verb(self.tokens)
        self.direct_obj = self.get_direct_obj(self.tokens)
        self.indirect_obj = self.get_indirect_obj(self.no_punctuation)

    def remove_punctuation(self, sentence):
        punc = ('''"!()-[]{};:'"\,<>./?@#$%^&*_~''')
        for ele in sentence: 
            if ele in punc: 
                sentence = sentence.replace(ele, "")
        return sentence

    def get_verb(self, tokens):
        verb_list = []
        for word in tokens:
            for i in Parser.verbs:
                if word in Parser.verbs[i]:
                    verb_list.append(i)
        return verb_list

    def get_direct_obj(self, tokens):
        direct_obj_list = []
        for word in tokens:
            for i in Parser.items:
                if word in Parser.items[i]:
                    direct_obj_list.append(i)
        return direct_obj_list

    def get_indirect_obj(self, no_punctuation):
        return no_punctuation.split("with")





def main():
    while True:

        command = Parser(input("> "))

        print(command.tokens)
        print("verb: ", command.verb)
        print("direct object: ", command.direct_obj)
        print("preposition: ", command.indirect_obj)

if __name__ == "__main__":
    main()