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
THRESHOLD = (0.7,)
FILE_NAME = ("sentences.txt", "userforms.txt")


"""****************************** GLOBAL VAR *********************************"""
NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
          "six": 6, "seven": 7, "eight": 8, "nine": 9,"ten": 10,
          "eleven": 11, "twelve": 12, "midnight": 0, "noon": 12}


"""**************************** Read text file ******************************"""
def read_file(name, mode=None):
    if type(name) == str:
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
            return userform
        else: return []


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
                    digits.append(NUMBER[t[0]])
        digits.sort()
    return digits

    
"""************************** Recognition process ***************************"""
def recognition_process(tags, userforms):
    if type(tags) == type(userforms) == list and type(tags[0]) == tuple:
        threshold_max = tmp = 0; userform_name = None
    
        # merge extra words and synonyms in one list for every userform
        for form in userforms:
            form.append(get_synonyms(form.__getitem__(0)))

        # strategy: try to find the best match between each token and the userforms    
        for tag in tags:
            if tag[1] == "NOUN" or tag[1] == "ADJ" or tag[1] == "VERB":
                for form in userforms:
                    for word in form:
                        tmp = get_threshold(tag[0], word)
                        if tmp >= THRESHOLD[0] and threshold_max < tmp:
                            threshold_max = tmp
                            userform_name = form.__getitem__(0)
                            if threshold_max == 1:
                                break
        return userform_name
        
                        
"""******************************* Entry Point ******************************"""
if __name__ == "__main__":
    # read the userforms from file
    form_list = read_file(FILE_NAME[1], mode="form"); index=0
    while True: 
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
            break

