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
Description: This code returns a userform name after analysing data from text file.
             The algorithms strategies use natural language processing techniques.
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
MAX_DIST = (2,)
MIN_LENGTH = (3,)
THRESHOLD = (0.875,)
SEN_FILE = ("sentences.txt",)
USER_FORM = (#userform name     extra words
            ("dentist",         None),
            ("bodyguard",       None),
            ("storage",         None),
            ("loan",            None),
            ("dustman",         ("trash", None)),
            ("snow",            ("shovel", None)),
            ("caterer",         ("catrer", None)),
            ("mover",           ("moving", None)),
            ("ticket",          ("hockey", None)),
            ("therapist",       ("massage", None)),
            ("tutor",           ("tutoring", None)),
            ("guide",           ("gide", "visit")),
            ("renting",         ("rent", "rant")),
            ("pool",            ("basin", "pol")),
            ("instructor",      ("teach", "learn")),
            ("trainer",         ("gym", "workout")),
            ("exterminator",    ("roach", "insect")),
            ("assembler",       ("set", "assemble")),
            ("tattooist",       ("tattoo", "piercer")),
            ("veterinary",      ("animal", "cat", "dog")),
            ("delivery",        ("bier", "beer", "pizza")),
            ("carpooling",      ("getting", "lift", "carpool")),
            ("plumber",         ("toilet", "conditioner", "swing")),
            ("babysitter",      ("kid", "children", "housekeeping")),
            ("taxi",            ("driver", "drive", "pick", "ride")),
            ("article",         ("shoe", "watch", "perfume", "dress")),
            ("photographer",    ("picture", "photo", "pic", "photograf")),
            ("programmer",      ("developer", "web", "computer", "network")),
            ("couturier",       ("shirt", "fashion", "tailor", "clothe",
                                 "t-shirt")),
            ("gardener",        ("lawn", "flower", "garden", "plant",
                                "gardn", "gardening", "mowed")),
            ("housemaid",       ("waitress", "lady", "dish", "laundry",
                                 "menage", "server")),
            ("car",             ("garage", "truk", "towing", "carburator", 
                                 "carburetor")),
            ("event",           ("musician", "bouncer", "security", "DJ",
                                 "sound", "mix", "song")),
            ("booking",         ("schedule", "meeting", "appointment",
                                 "book", "pm", "am")),
            ("house",           ("residence", "porch", "deck", "roof", "dec",
                                 "roof", "chimney", "ditch", "doghouse", "tree",
                                 "fence", "paint", "painter", "gutter", "apartment"
                                 "paving")))


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
    synonyms = []
    if type(token) == str:
        for s in wordnet.synsets(token):
            for w in s.lemmas():
                try: synonyms.append(w.name())
                except: continue
    return synonyms


"""********************* Create a list for spell check **********************"""
def spell_check(tokens):
    if type(tokens) == list:
        sd = enchant.Dict("en_US")
        sd.add("!")
        length = len(tokens)
        new_tokens = [None]*length
        tokens_range = range(length)
        for i in tokens_range:
            suggestions = sd.suggest(tokens[i])
            if sd.check(tokens[i]):
                new_tokens[i] = tokens[i]
            elif suggestions and dist(tokens[i], suggestions[0]) < MAX_DIST[0]:
                new_tokens[i] = suggestions[0]
            else: new_tokens[i] = tokens[i]
        return new_tokens
    return []


"""****************** Get the threshold value between 2 words ***************"""
def get_threshold(w1, w2):
    if type(w1) == type(w2) == str:
        if w1 == w2 or w1 == w2 + "s" or w1 == w2 + "es":
            return 1
        else:
            try:
                syn1 = wordnet.synset(w1+".n.01")
                syn2 = wordnet.synset(w2+".n.01")
                return syn1.wup_similarity(syn2)
            except: return 0
    return 0


"""********************** Validate the sentence format **********************"""
def validate_format(sen):
    if type(sen) == str:
        length = len(sen); sen_range = range(length) 
        if length > MIN_LENGTH[0]:
            flag = False
            for i in sen_range:         
                if sen[i] == "." or sen[i] == "!" or sen[i] == "?" and not flag:
                    flag = True
                elif flag and sen[i].isalnum():
                    return False
            return True
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
def recognition_process(args):
    if type(args) == list and type(args[0]) == tuple:
        threshold_max = index = int()

        # merge extra words and synonyms in one list, for every userform
        words_dict = [get_synonyms(f[0]) for f in USER_FORM]
        for i, form in enumerate(USER_FORM):
            if type(form[1]) == tuple:
                for extra_word in form[1]:
                    words_dict[i].append(extra_word)

        # calling range and len methods before the main loop (optimisation)         
        dict_range = [range(len(l)) for l in words_dict]
        form_range = range(len(USER_FORM))
        for tag in args:
            if tag[1] == "NOUN" or tag[1] == "ADJ" or tag[1] == "VERB":
                for i in form_range:
                    for j in dict_range[i]:
                        tmp = get_threshold(tag[0], words_dict[i][j])
                        if tmp >= THRESHOLD[0]:
                            threshold_max = tmp
                            index = i
                            if threshold_max == 1: break
        if threshold_max:
            return USER_FORM[index][0]
        
                        
"""******************************* Entry Point ******************************"""
if __name__ == "__main__":
    index = 0
    while True: 
        # clearing the screen
        print("\n" * 100)
        
        # read the sentences from file
        l_sent = read_sen_file()

        # select a sentence
        index %= len(l_sent)
        sentence = l_sent[index]
        index += 1

        # validate the format
        format_is_valid = validate_format(sentence)

        if format_is_valid:
            # tokenisation
            tokens = tokenize.word_tokenize(sentence)

            # spell checking
            modif_tokens = spell_check(tokens)

            # filtering tokens 
            stop_words = set(stop.words("english")) 
            filt_tokens = [w.lower() for w in modif_tokens if w not in stop_words]
    
            # speech tagging (identification) 
            tags = pos_tag(filt_tokens, tagset="universal")
        
            # relation recognition
            user_form = recognition_process(tags)
    
        print("\nSENTENCE #%d\n" %(index), sentence)
        print("\nVALID FORMAT:", format_is_valid)
        
        if format_is_valid:
            print("\n\nTOKENS\n", tokens)
            print("\n\nSPELL CHECK\n", modif_tokens)
            print("\n\nFILTERED TOKENS\n", filt_tokens)
            print("\n\nTAGGING\n", tags)
            print("\n\nDIGITS:", get_digits(tags))
            print("\n\nUSERFORM:", user_form)

        # ending the program or not ?
        if sys.stdin.read(1).lower() == "q":
            break

