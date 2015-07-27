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

File: test.py
Description: this file is used for testing the nltk module
Author: Victor Neville
Python version: 3.4.0
Date: 07-06-2015
*****************************************************************************"""

import sys
import enchant
from nltk import pos_tag
from nltk import tokenize
from nltk.corpus import wordnet
from random import randrange as rand
from nltk.corpus import stopwords as stop
from nltk.metrics import edit_distance as dist


"""****************************** CONSTANTS *********************************"""
SEN_FILE = ("sentences.txt", None)
THRESHOLD = (0.75, None)
MIN_LENGTH = (3, None)
MAX_DIST = (2, None)
USER_FORM = ("car",
             "pool",
             "house", 
             "shovel",
             "babysitter",
             "appointment")


"""**************************** Read text file ******************************"""
def read_sen_file():
    l_sent = []
    try:
        with open(SEN_FILE[0]) as file:
            l_sent = file.readlines()
    except IOError as err:
        print("I/O Error %s" %(err))
        sys.exit()
    else: file.close()
    return l_sent


"""***** Verify than the 1st str arg is the plural of the 2nd str arg *******"""
def isplural(w1, w2):
    if type(w1) == type(w2) == str:
        return w1 == w2+"s"
    else: return False


"""**************** Convert word to num to represent hours  *****************"""
def word_to_num(w):
    if type(w) == str:
        if w == "one":    return 1
        if w == "two":    return 2
        if w == "three":  return 3
        if w == "four":   return 4
        if w == "five":   return 5
        if w == "six":    return 6
        if w == "seven":  return 7
        if w == "eight":  return 8
        if w == "nine":   return 9
        if w == "ten":    return 10
        if w == "eleven": return 11
        if w == "twelve": return 12


"""**************** Create a list of synonyms for the word arg **************"""
def get_synonyms(token):
    if type(token) == str:
        for s in wordnet.synsets(token):
            synonyms = [l.name() for l in s.lemmas()]
        return synonyms
    else: return []


"""********************* Create a list for spell check **********************"""
def spell_check(tokens):
    if type(tokens) == list:
        sd = enchant.Dict("en_US"); size = len(tokens); new_list = [None]*size
        for i in range(size):
            suggestions = sd.suggest(tokens[i])
            if sd.check(tokens[i]):
                new_list[i] = tokens[i]
            elif suggestions and dist(tokens[i], suggestions[0]) <= MAX_DIST[0]:
                new_list[i] = suggestions[0]
            else: new_list[i] = tokens[i]
        return new_list
    else: return []


"""****************** Validate the threshold between 2 words ****************"""
def threshold_is_valid(w1, w2):
    if type(w1) == type(w2) == str:
        try:
            syn1 = wordnet.synset(w1+".n.01")
            syn2 = wordnet.synset(w2+".n.01")
            return syn1.wup_similarity(syn2) >= THRESHOLD[0]
        except: return False
    return False


"""********************** Validate the sentence format **********************"""
def format_is_valid(sen):
    valid = False; size = len(sen)
    if type(sen) == str and size > MIN_LENGTH[0]:
        end_symbols = 0; valid = True
        for i in range(size):         
            if sen[i] == "." or sen[i] == "!" or sen[i] == "?":
                end_symbols += 1
                if end_symbols == 1 and i+1 < size:
                    valid = sen[i+1] == "\n" 
                elif end_symbols > 1: break
    return valid


"""*********************** Get digits from the tags list ********************"""
def get_digits(tags):
    digits = [] 
    if type(tags) == list and type(tags[0]) == tuple:
        size = len(tags)
        for i in range(size):
            if tags[i][1] == "NUM":
                if tags[i][0].isdigit():
                    digits.append(int(tags[i][0]))
                else:
                    digits.append(word_to_num(tags[i][0].lower()))
    digits.sort()
    return digits


"""************************** Recognition process ***************************"""
def recognition_process(tags):
    if type(tags) == list and type(tags[0]) == tuple:
        syn = [get_synonyms(w) for w in USER_FORM]; size = len(tags)
        for i in range(size):
            if tags[i][1] == "NOUN" or tags[i][1] == "ADJ" or tags[i][1] == "VERB":
                for j in range(len(syn)):
                    for k in range(len(syn[j])):
                        if threshold_is_valid(tags[i][0], syn[j][k]) or isplural(tags[i][0], syn[j][k]):
                            return USER_FORM[j]


"""******************************* ENTRY POINT ******************************"""
if __name__ == "__main__":
    while True: 
        # CLEARING THE SCREEN
        print("\n" * 100)
        
        # READ THE SENCENCES FROM FILE
        l_sent = read_sen_file()

        # SELECT RANDOM SENTENCE
        sentence = l_sent[rand(0, len(l_sent))]

        # VALIDATE THE FORMAT
        format_flag = format_is_valid(sentence)

        # TOKENISATION
        tokens = tokenize.word_tokenize(sentence)

        # SPELL CHECKING
        modified_tokens = spell_check(tokens)

        # FILTERING TOKENS 
        stop_words = set(stop.words("english")) 
        filtered_tokens = [w for w in modified_tokens if w not in stop_words]
    
        # SPEECH TAGGING 
        tags = pos_tag(filtered_tokens, tagset="universal")
        
        # RELATION RECOGNITION
        user_form = recognition_process(tags)

        # UPDATE THE FORMAT FLAG IF NECESSARY
        if format_flag and user_form is None:
            format_flag = False
    
        print("\nSENTENCE\n", sentence)
        print("TOKENS\n", tokens)
        print("\nSPELL CHECK\n", modified_tokens)
        print("\nFILTERED TOKENS\n", filtered_tokens)
        print("\nTAGGING\n", tags)
        print("\nVALID FORMAT:", format_flag)
        print("\nDIGITS:", get_digits(tags))
        print("\nUSERFORM:", user_form)

        # ENDING THE PROGRAM OR NOT ?
        if sys.stdin.read(1).lower() == "q":
            break
