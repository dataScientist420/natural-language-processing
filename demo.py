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

Description: This code generates user forms after receiving and analysing
             text data from file. The algorithms use natural language
             processing techniques.

File: demo.py
Author: Victor Neville
Python version: 3.4.0
Date: 07-06-2015
*****************************************************************************"""

import sys
import enchant
from nltk import pos_tag
from nltk import tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords as stop
from nltk.metrics import edit_distance as dist


"""****************************** CONSTANTS *********************************"""
SEN_FILE = ("input.txt", None)
THRESHOLD = (0.75, None)
MIN_LENGTH = (3, None)
MAX_DIST = (2, None)
USER_FORM = (#userform key   extra words
            ("car",          None),
            ("babysitter",   None),
            ("pool",         ("basin", None)),
            ("snow",         ("shovel", None)),
            ("house",        ("residence", None)),
            ("appointment",  ("schedule", "meeting"))
            )


"""**************************** Read text file ******************************"""
def read_sen_file():
    l_sent = []
    try:
        with open(SEN_FILE[0]) as file:
            l_sent = file.readlines()
    except IOError as err:
        print("I/O Error %s" %(err))
        sys.exit()
    else:
        file.close()
    return l_sent


"""**************** Convert word to num to represent hours  *****************"""
def word_to_num(token):
    if type(token) == str:
        if token == "one":    return 1
        if token == "two":    return 2
        if token == "three":  return 3
        if token == "four":   return 4
        if token == "five":   return 5
        if token == "six":    return 6
        if token == "seven":  return 7
        if token == "eight":  return 8
        if token == "nine":   return 9
        if token == "ten":    return 10
        if token == "eleven": return 11
        if token == "twelve": return 12


"""**************** Create a list of synonyms for the word arg **************"""
def get_synonyms(token):
    if type(token) == str:
        for s in wordnet.synsets(token):
            synonyms = [l.name() for l in s.lemmas()]
        return synonyms
    return []


"""*********** Verify if token equals to user form extra words  *************"""
def equal_to_extra_words(key, token):
    if type(token) == type(key) == str:
        for f in USER_FORM:
            if f[0] == key and type(f[1]) == tuple:
                for w in f[1]:
                    if token == w:
                        return True
    return False


"""********************* Create a list for spell check **********************"""
def spell_check(tokens):
    if type(tokens) == list:
        sd = enchant.Dict("en_US")
        length = len(tokens)
        new_tokens = [None]*length
        tokens_range = range(length)
        for i in tokens_range:
            suggestions = sd.suggest(tokens[i])
            if sd.check(tokens[i]):
                new_tokens[i] = tokens[i]
            elif suggestions and dist(tokens[i], suggestions[0]) <= MAX_DIST[0]:
                new_tokens[i] = suggestions[0]
            else: new_tokens[i] = tokens[i]
        return new_tokens
    return []


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
def validate_format(sen):
    if type(sen) == str:
        length = len(sen); sen_range = range(length) 
        if length > MIN_LENGTH[0]:
            end_symbols = 0; valid = True
            for i in sen_range:         
                if sen[i] == "." or sen[i] == "!" or sen[i] == "?":
                    end_symbols += 1
                    if end_symbols == 1:
                        if i+1 < length:
                            valid = sen[i+1] == "\n" or sen[i+1] == " "
                        if i+2 < length:
                            valid = sen[i+2] == "\n" or sen[i+2] == " " 
                    elif end_symbols > 1:
                        break
            return valid
    return False


"""*********************** Get digits from the tags list ********************"""
def get_digits(tags):
    digits = []
    if type(tags) == list and type(tags[0]) == tuple:
        for t in tags:
            if t[1] == "NUM":
                if t[0].isdigit():
                    digits.append(int(t[0]))
                else:
                    digits.append(word_to_num(t[0]))
        digits.sort()
    return digits
    

"""************************** Recognition process ***************************"""
def recognition_process(tags):
    if type(tags) == list and type(tags[0]) == tuple:
        syn = [get_synonyms(f[0]) for f in USER_FORM]
        syn_range = [range(len(l)) for l in syn]
        list_range = range(len(syn))
        for t in tags:
            if t[1] == "NOUN" or t[1] == "ADJ" or t[1] == "VERB":
                for i in list_range:
                    for j in syn_range[i]:
                        if (threshold_is_valid(t[0], syn[i][j])
                            or t[0] == syn[i][j] + "s"
                            or equal_to_extra_words(USER_FORM[i][0], t[0])):
                            return USER_FORM[i][0]


"""******************************* ENTRY POINT ******************************"""
if __name__ == "__main__":
    cnt = 0
    while True: 
        # CLEARING THE SCREEN
        print("\n" * 100)
        
        # READ THE SENCENCES FROM FILE
        l_sent = read_sen_file()

        # SELECT A SENTENCE
        sentence = l_sent[cnt % len(l_sent)]
        cnt += 1

        # VALIDATE THE FORMAT
        format_is_valid = validate_format(sentence)

        if format_is_valid:
            # TOKENISATION
            tokens = tokenize.word_tokenize(sentence)

            # SPELL CHECKING
            modif_tokens = spell_check(tokens)

            # FILTERING TOKENS 
            stop_words = set(stop.words("english")) 
            filt_tokens = [w.lower() for w in modif_tokens if w not in stop_words]
    
            # SPEECH TAGGING 
            tags = pos_tag(filt_tokens, tagset="universal")
        
            # RELATION RECOGNITION
            user_form = recognition_process(tags)
    
        print("\nSENTENCE\n", sentence)
        print("\nVALID FORMAT:", format_is_valid)
        
        if format_is_valid:
            print("\n\nTOKENS\n", tokens)
            print("\n\nSPELL CHECK\n", modif_tokens)
            print("\n\nFILTERED TOKENS\n", filt_tokens)
            print("\n\nTAGGING\n", tags)
            print("\n\nDIGITS:", get_digits(tags))
            print("\n\nUSERFORM:", user_form)

        # ENDING THE PROGRAM OR NOT ?
        if sys.stdin.read(1).lower() == "q":
            break

