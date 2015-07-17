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

import sys
from nltk import tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk import RegexpParser
from nltk import ne_chunk
from random import randrange
from nltk.corpus import wordnet 


MIN_LENGTH = (3, None)
THRESHOLD = (0.7, None)
USER_FORM = (0, 1, 2, 3)
keyword = ["babysitter", "pool", "car", "driveway"]


"""**************** Create a list of synonyms for the word arg **************"""
def get_synonyms(word):
    synonyms = []
    if type(word) == str:
        for s in wordnet.synsets(word):
            for l in s.lemmas():
                synonyms.append(l.name())
    return synonyms


"""****************** Validate the threshold between 2 words ****************"""
def threshold_is_valid(w1, w2):
    if type(w1) == type(w2) == str:
        syn1 = wordnet.synset(w1+".n.01")
        syn2 = wordnet.synset(w2+".n.01")
        return syn1.wup_similarity(syn2) >= THRESHOLD[0]
    return False


"""********************** Validate the sentence format **********************"""
def input_format_is_ok(sen):
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


"""*********************** Get digits from the tags list ********************"""
def get_digits(tags):
    digits = []
    if type(tags) == list:
        for i in range(len(tags)):
            if tags[i][1] == "CD" and tags[i][0].isdigit():
                digits.append(int(tags[i][0]))
    digits.sort()
    return digits


"""******************* Recognition process (NOT FINISHED) *******************"""
def recognition_process(tags, syn):
    user_form = None
    if type(tags) == type(syn) == list:
        for i in range(len(tags)):
            if tags[i][1] == "NN":
                for j in range(len(syn)):
                    for k in range(len(syn[j])):
                        if threshold_is_valid(tags[i][0], syn[j][k]):
                            if   j == USER_FORM[0]: user_form = keyword[0]
                            elif j == USER_FORM[1]: user_form = keyword[1]
                            elif j == USER_FORM[2]: user_form = keyword[2]
                            elif j == USER_FORM[3]: user_form = keyword[3]
                            digits = get_digits(tags)
                            if len(digits) > 0:
                                pass #TODO    
    return user_form


"""******************************* ENTRY POINT ******************************"""
if __name__ == "__main__":
    l_sent = [
              "I would like a babysitter this friday night!",
              "Clear my pool now",
              "sitter 6 to 7",
              "wash my car",
              "shovel my driveway"]
    
    # GENERATE THE SYNONYMS LIST
    synonym = []
    for w in range(len(keyword)):
        synonym.append(get_synonyms(keyword[w]))

    # RANDOM SENTENCE
    sentence = l_sent[randrange(0, len(l_sent))]

    # VALIDATE THE FORMAT
    if not input_format_is_ok(sentence): sys.exit(1)

    # TOKENISATION
    words = tokenize.word_tokenize(sentence)

    # FILTERING TOKENS 
    stop_words = set(stopwords.words("english")) 
    filtered_words = [w for w in words if w not in stop_words]
    
    # SPEECH TAGGING 
    tags = pos_tag(filtered_words)

    # RELATION RECOGNITION
    user_form = recognition_process(tags, synonym)
    
    print("\nSENTENCE\n", sentence)
    print("\nTOKENS\n", words)
    print("\nFILTERED TOKENS\n", filtered_words)
    print("\nTAGGING\n", tags)
    print("\nDIGITS", get_digits(tags))
    print("\nUSERFORM:\n", user_form)
    
    """
    # ENTITY RECOGNITION
    entity = ne_chunk(tags)
    
    #CHUNKING
    regex = RegexpParser("Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}")
    chunk = regex.parse(tags)
    chunk.draw()
    entity.draw()
    """
