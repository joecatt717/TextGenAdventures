#!sudo pip3 install nltk 
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

commands = [
    'wear crown',
    'smell rose',
    'eat fish',
    'light lamp',
    'give fish to troll',
    'propose to the princess',
    'go north',
]

def get_senses(word):
    ''' Returns a list of word senses (WordNet synsets) for a word'''
    word_senses = wn.synsets(word)
    return word_senses

def get_definition(word_sense):
    return word_sense.definition()

def get_synonyms(word_sense):
    synonyms = []
    for lemma in word_sense.lemmas():
        synonym = lemma.name().replace('_', ' ')
        synonyms.append(synonym)
    return synonyms

#Hypernyms / Hyponyms
#each word is nested into classes as hypernyms or hyponyms
# i.e. red is-a hyponym (hypo == subset) of color, and color is-a hypernym of red (hyper == above)
hyper = lambda s: s.hypernyms()
hypo = lambda s: s.hyponyms()

def get_hypernyms(word_sense, depth = 5):
    return list(word_sense.closure(hyper, depth = depth))

def get_hyponyms(word_sense, depth = 5):
    return list(word_sense.closure(hypo, depth = depth))
'''
def annotate_synsets(sentences):
    This function queries WordNet for each word in a list of sentences,
    and asks the user to input a number corresponding to the synset.

    word_senses = {}
    # Cached slections maps from word string to the previous
    # selection for this word (an integer)
    cached_selections = {}

    for i, sent in enumerate(sentences):
        words = word_tokenize(sent)

        for word in words:
            sysnsets = wn.synsets(word)
            if len(sysnsets) != 0:
                selection = select_synset(sent, word, sysnets, cached_selections)
                if selection != None:
                    cached_selections[word] = selection
                    if selection < len(sysnsets):
                        s = sysnsets[selection]
                        word_senses[word] = s.name()
        return word_senses
'''







def main():

    
    for i in range(10):
        word = input("> ").strip()
        word_senses = (get_senses(word))
        for j in range(len(word_senses)):
            
            definitions = get_definition(word_senses[j])
            print(definitions)
            synonyms = get_synonyms(word_senses[j])
            print(synonyms)
            '''
            hypernyms = get_hypernyms(word_senses[j])
            print(hypernyms)
            
            hyponyms = get_hyponyms(word_senses[j])
            print(hyponyms)
            
            x = annotate_synsets(word_senses)
            print(x)
            '''

if __name__ == "__main__":
    main()