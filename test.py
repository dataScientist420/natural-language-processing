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
from nltk import tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from random import randrange
from nltk.corpus import wordnet 


"""****************************** CONSTANTS *********************************"""
MIN_LENGTH = (3, None)
THRESHOLD = (0.7, None)
SEN_FILE = ("sentences.txt", None)
USER_FORM = ("babysitter", "pool", "car", "driveway")


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
def word_to_num(w):
    if type(w) == str:
        if   w == "one":    return 1
        elif w == "two":    return 2
        elif w == "three":  return 3
        elif w == "four":   return 4
        elif w == "five":   return 5
        elif w == "six":    return 6
        elif w == "seven":  return 7
        elif w == "eight":  return 8
        elif w == "nine":   return 9
        elif w == "ten":    return 10
        elif w == "eleven": return 11
        elif w == "twelve": return 12


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
        try:
            syn1 = wordnet.synset(w1+".n.01")
            syn2 = wordnet.synset(w2+".n.01")
            return syn1.wup_similarity(syn2) >= THRESHOLD[0]
        except: return False
    return False


"""********************** Validate the sentence format **********************"""
def format_is_valid(sen):
    valid = False; length = len(sen)
    if type(sen) == str and length > MIN_LENGTH[0]:
        end_symbols = 0; valid = True
        for i in range(length):         
            if sen[i] == "." or sen[i] == "!" or sen[i] == "?":
                end_symbols += 1
                if end_symbols == 1 and i+1 < length:
                    valid = sen[i+1] == "\n" 
                elif end_symbols > 1: break
    return valid


"""*********************** Get digits from the tags list ********************"""
def get_digits(tags):
    digits = []
    if type(tags) == list:
        for i in range(len(tags)):
            if tags[i][1] == "NUM":
                if tags[i][0].isdigit():
                    digits.append(int(tags[i][0]))
                else: digits.append(word_to_num(tags[i][0].lower()))
    digits.sort()
    return digits


"""************************** Recognition process ***************************"""
def recognition_process(tags, syn):
    if type(tags) == type(syn) == list:
        for i in range(len(tags)):
            if tags[i][1] == "NOUN" or tags[i][1] == "ADJ":
                for j in range(len(syn)):
                    for k in range(len(syn[j])):
                        if threshold_is_valid(tags[i][0], syn[j][k]):
                            return USER_FORM[j]


"""******************************* ENTRY POINT ******************************"""
if __name__ == "__main__":
    while True: 
        # CLEARING THE SCREEN
        print("\n" * 100)
        
        # READ THE SENCENCES FROM FILE
        l_sent = read_sen_file()

        # SELECT RANDOM SENTENCE
        sentence = l_sent[randrange(0, len(l_sent))]

        # VALIDATE THE FORMAT
        format_flag = format_is_valid(sentence)

        # TOKENISATION
        words = tokenize.word_tokenize(sentence)

        # FILTERING TOKENS 
        stop_words = set(stopwords.words("english")) 
        filtered_words = [w for w in words if w not in stop_words]
    
        # SPEECH TAGGING 
        tags = pos_tag(filtered_words, tagset="universal")

        # GENERATE SYNONYMS LIST
        synonym = []
        for w in range(len(USER_FORM)):
            synonym.append(get_synonyms(USER_FORM[w]))

        # RELATION RECOGNITION
        user_form = recognition_process(tags, synonym)

        # UPDATE THE FORMAT FLAG IF NECESSARY
        if format_flag and user_form is None:
            format_flag = False
    
        print("\nSENTENCE\n", sentence)
        print("TOKENS\n", words)
        print("\nFILTERED TOKENS\n", filtered_words)
        print("\nTAGGING\n", tags)
        print("\nVALID FORMAT:", format_flag)
        print("\nDIGITS", get_digits(tags))
        print("\nUSERFORM:", user_form)

        # ENDING THE PROGRAM OR NOT ?
        if sys.stdin.read(1).lower() == "q":
            break
        
