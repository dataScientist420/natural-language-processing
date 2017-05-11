#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Description: This code returns a userform name after analysing data 
#			   from text file. The algorithms strategies use natural 
#			   language processing techniques.

# @file: demo.py
# @author: Victor Neville
# @python version: 3.4.0
# @date: 07-06-2015

import sys
import enchant
from nltk import pos_tag
from nltk import tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords as stop
from nltk.metrics import edit_distance as dist

################################# GLOBALS #####################################
MAX_DIST = (2,)
MIN_LENGTH = (3,)
THRESHOLD = (0.9,)
FILE_NAME = ("sentences.txt", "userforms.txt")
NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
          "six": 6, "seven": 7, "eight": 8, "nine": 9,"ten": 10,
          "eleven": 11, "twelve": 12, "midnight": 0, "noon": 12}

###############################################################################
    # @name: read_file
    # @description: Allows the user to read a text file.
    # @inputs:
    # - name: the file name
    # - mode: the reading mode (sentences of form)
    # @returns: a list containing the text tokens
def read_file(name, mode=None):
    if isinstance(name, str):
        try:
            with open(name) as file:
                l_sent = file.readlines()
        except IOError as err:
            print("I/O Error %s" %(err))
            sys.exit()
        else:
            file.close()
        if mode == "sen":
            return l_sent
        elif mode == "form":
            userform = tokens = []
            for s in l_sent:
                tokens = tokenize.word_tokenize(s)
                userform.append([w for w in tokens if w.isalnum()])          
                userform.append(get_synonyms(userform.__getitem__(0)))
            return userform
    return []

###############################################################################
    # @name: get_synonyms
    # @description: Creates a list of synonyms for the token argument.
    # @inputs:
    # - token: a word
    # @returns: a list containing the token synonyms
def get_synonyms(token):
    synonyms = []
    if isinstance(token, str):
        for s in wordnet.synsets(token):
            for w in s.lemmas():
                try: synonyms.append(w.name())
                except: continue
    return synonyms

###############################################################################
    # @name: spell_check
    # @description: Creates a list with corrected spelling errors.
    # @inputs:
    # - tokens: a list of words
    # @returns: a list with corrected spelling errors
def spell_check(tokens):
    if isinstance(tokens, list):
        sd = enchant.Dict("en_US")
        
        # add extra word to the dictionnary
        if not sd.is_added("$"):  
            sd.add_to_session("$")
            
        new_tokens = list()
        for word in tokens:
            if sd.check(word):
               new_tokens.append(word)
            else:
                suggestions = sd.suggest(word)
                for sug in suggestions:
                    distance = dist(word, sug)
                    if distance <= MAX_DIST[0]:
                        new_tokens.append(sug)
                        break
        return new_tokens
    return []

###############################################################################
    # @name: get_threshold
    # @description: Gets the threshold value of 2 words.
    # @inputs:
    # - w1: the first word
    # - w2: the second word
    # @returns: a threshold value [0.0, 1.0]
def get_threshold(w1, w2):
    if isinstance(w1, str) and isinstance(w2, str):
        if w1 == w2 or w1 == w2 + "s" or w1 == w2 + "es":
            return 1.0
        else:
            try:
                syn1 = wordnet.synset(w1+".n.01")
                syn2 = wordnet.synset(w2+".n.01")
                return syn1.wup_similarity(syn2)
            except: 
            	return 0.0
    return 0.0

###############################################################################
    # @name: validate_format
    # @description: It validates the sentence format.
    # @inputs:
    # - sen: a string containing a sentence
    # @returns: True if sentence is valid, else False
def validate_format(sen):
    if isinstance(sen, str):
        length = len(sen) 
         
        if length > MIN_LENGTH[0]:
            flag = False
            for i in range(length):         
                if sen[i] in ("." , "!", "?") and not flag:
                    flag = True
                elif flag and sen[i].isalnum():
                    return False
            return True
    return False

###############################################################################
    # @name: get_digits
    # @description: Returns a list with digits related to the tags argument.
    # @inputs:
    # - tags: a list containing the tags
    # @returns: a list containing digits
def get_digits(tags):
    digits = []
    
    if isinstance(tags, list):
        for t in tags:
            if t[1] == "NUM":
                if t[0].isdigit():
                    digits.append(int(t[0]))
                else:
                    try: 
                    	digits.append(NUMBER[t[0]])
                    except: continue
        digits.sort()
        
    return digits

###############################################################################
    # @name: recognition_process
    # @description: It associates text with a form.
    # @inputs:
    # - tags: a list containing the tags
    # - userforms: a list containing the userforms names
    # @returns: a user form name
def recognition_process(tags, userforms):
    if isinstance(tags, list) and isinstance(userforms, list):
        threshold_max = 0.0
        userform_name = None

        # try to find the best match between each token and forms    
        for tag in tags:
            if tag[1] in ("NOUN", "ADJ", "VERB"):
                for form in userforms:
                    for word in form:
                        tmp = get_threshold(tag[0], word)
                        if tmp >= THRESHOLD[0] and threshold_max < tmp:
                            threshold_max = tmp
                            userform_name = form.__getitem__(0)
                            if threshold_max == 1:
                                break
        return userform_name
        
                  
# Entry Point 
if __name__ == "__main__":
    # read the userforms from file
    form_list = read_file(FILE_NAME[1], mode="form")
    index = 0
    done = False
    
    while not done: 
        # clearing the screen
        print("\n" * 100)
        
        # read the sentences from file
        sen_list = read_file(FILE_NAME[0], mode="sen")

        # select a sentence
        index %= len(sen_list)
        sentence = sen_list[index]
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
            user_form = recognition_process(tags, form_list)
    
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
            done = True
