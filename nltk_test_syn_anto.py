from nltk.corpus import wordnet

w0 = "ship"
w1 = "boat"


if __name__ == "__main__":
    synonyms = []
    antonyms = []
    syns = wordnet.synsets(w0)

    # rempit les listes des synonymes/antonymes pour w0
    for s in syns:
        for l in s.lemmas():
            synonyms.append(l.name())
            if (l.antonyms()):
                antonyms.append(l.antonyms()[0].name())

    syns0 = wordnet.synset(w0+".n.01")
    syns1 = wordnet.synset(w1+".n.01")

    print "synonyms (", w0, ") :\n", synonyms
    print "antonyms (", w0, ") :\n", antonyms
    
    print w0, "and", w1, "are", syns0.wup_similarity(syns1), "similar"
