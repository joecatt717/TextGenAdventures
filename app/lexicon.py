# make a list of possible directions, verbs, stops, nouns, and errors
directions = ["north", "south", "east", "west", "up", "down", "left", "right"]
verbs = ["go", "kill", "eat", "stop"]
stops = ["the", "in", "of", "from", "at", "it", "to"]
nouns = ["bear", "princess", "castle"]
# numbers must == any string of 0 through 9 characters

def scan(sentence):

    words = sentence.split()
    print(words)
    x = []

    for i in range(len(words)):
        if words[i] in directions:
            x.append(('direction', words[i]))
        elif words[i] in verbs:
            x.append(('verb', words[i]))
        elif words[i] in stops:
            x.append(('stop', words[i]))
        elif words[i] in nouns:
            x.append(('noun', words[i]))
        else:
            x.append(('error', words[i]))
    return x


def main():
    for i in range(10):
        sentence = input("> ")
        scan(sentence)
        print(scan(sentence))

if __name__ == "__main__":
    main()