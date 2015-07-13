#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""***************************************************************************** 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

File: test_nltk.py
Description: this file is used for testing the nltk module
Author: Victor Neville
Date: 07-06-2015
*****************************************************************************"""

from nltk import tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk import RegexpParser
from nltk import ne_chunk
from nltk import WordNetLemmatizer
from random import randrange
from nltk.corpus import wordnet
import sys

MIN_LENGTH = (3, None)

"""***** Fonction qui retourne une liste de synonymes pour le mot recu ******"""
def get_synonyms(word):
    synonyms = []
    if type(word) == str:
        synsets = wordnet.synsets(word)
        for s in synsets:
            for l in s.lemmas():
                synonyms.append(l.name().encode("ascii"))
    return synonyms

"""********* Fonction qui s'assure que la phrase recue est valide ***********"""
def input_is_valid(sen):
    valid = False
    length = len(sen)
    if type(sen) == str and length >= MIN_LENGTH[0]:
        end_symbols = 0
        valid = True
        for i in range(length):         
            #si phrase détectée, on s'assure qu'il n'y en a qu'une seule
            if sen[i] == "." or sen[i] == "!" or sen[i] == "?":
                end_symbols += 1
                if end_symbols == 1 and i+1 < length:
                    valid = sen[i+1] is None
                elif end_symbols > 1: break
    return valid

l_sent = ["I would like a babysitter this friday night!",
          "Clear my pool now",
          "babysitter six to seven",
          "wash my car",
          "shovel my driveway"]

# Cette liste contient un mot clé correspondant a chaque type 
types = ["babysitter", "pool", "car", "driveway"]


"""******************************* ENTRY POINT ******************************"""
if __name__ == "__main__":
    # Creation d'une liste avec les synonymes de chaque type
    synonyms = []
    for w in range(len(types)):
        synonyms.append(get_synonyms(types[w]))

    
    # RANDOM SENTENCE
    sentence = l_sent[randrange(0, len(l_sent))]

    if not input_is_valid(sentence): sys.exit(1)

    # TOKENISATION
    words = tokenize.word_tokenize(sentence)

    # FILTERING TOKENS 
    stop_words = set(stopwords.words("english")) 
    filtered_words = [w for w in words if w not in stop_words]

    # LEMATIZING
    lem = WordNetLemmatizer()
    size = len(filtered_words)
    lem_words = [None] * size
    for w in range(size):
        lem_words[w] = lem.lemmatize(filtered_words[w])
    
    # SPEECH TAGGING 
    tags = pos_tag(filtered_words)

    # CHUNKING
    regex = RegexpParser("Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}")
    chunk = regex.parse(tags)

    # ENTITY RECOGNITION
    entity = ne_chunk(tags, binary=True)
    
    print "\nSENTENCE\n", sentence
    print "\nTOKENS\n", words
    print "\nFILTERED nTOKENS\n", filtered_words
    print "\nLEMMATIZE nTOKENS\n", lem_words
    print "\nTAGGING\n", tags
    print "\nSYNONYMS OF %s:\n" %("BABYSITTER"), get_synonyms("babysitter")

    #chunk.draw()
    #entity.draw()
