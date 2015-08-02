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
from nltk.tokenize import word_tokenize, regexp_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords as stop
from nltk.metrics import edit_distance as dist
from difflib import SequenceMatcher
from nltk.corpus.reader import WordNetError

# CONSTANTS
MAX_DISTANCE = 2
MIN_LENGTH = 3
THRESHOLD = 0.95
SENTENCES = "sentences.txt"  # will be user input soon
FORMS = "userforms.txt"
NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
           "ten": 10, "eleven": 11, "twelve": 12, "midnight": 0, "noon": 12}


class Sentence(object):

    def __init__(self, sentence):
        self.sentence = sentence

        self.forms = []
        for s in tuple(open(FORMS, "r")):  # read the user_forms from file
            self.forms.append([w for w in regexp_tokenize(s, "[-\w]+") if w.isalnum()])

        if self.is_valid():
            self.tokens = regexp_tokenize(self.sentence, "(\\$)|[-\w]+")  # tokenizing with regex
            self.stop_words = set(stop.words("english"))  # filtering tokens words to remove
            self.filtered = [w.lower() for w in self.tokens if w not in self.stop_words]  # remove stop words
            self.spell_checked = self.spell_check()
            self.tags = pos_tag(self.spell_checked, tagset="universal")  # speech tagging (identification)
            print(self.tags)
            self.digits = self.get_digits()
            self.user_form = self.get_user_form()

    # Get digits from the tags list
    def get_digits(self):
        digits = []
        short_list = [x for x in self.tags if "NUM" in x]
        for word, tag in short_list:
            if word.isdigit():
                digits.append(int(word))
            elif word in NUMBERS:
                digits.append(NUMBERS[word])
        return digits

    # Create a list of synonyms for the word arg
    @staticmethod
    def get_synonyms(tokens):
        synonyms = []
        for s in wordnet.synsets(tokens):
            for w in s.lemmas():
                synonyms.append(w.name())
        return synonyms

    # Recognition process
    def get_user_form(self):
        threshold_max = 0
        user_form = ""
        # strategy: try to find the best match between each token and the user_forms
        a = ("NOUN", "ADJ", "VERB")
        for tag in self.tags:
            if any(x in tag for x in a):
                for form in self.forms:
                    for word in form:
                        tmp = self.get_threshold(tag[0], word)
                        if tmp >= THRESHOLD and threshold_max < tmp:
                            threshold_max = tmp
                            user_form = form.__getitem__(0)
                            if threshold_max == 1:
                                break
        return user_form

    # Get the threshold value between 2 words
    @staticmethod
    def get_threshold(w1, w2):
        if w1 == w2 or w1 == w2 + "s" or w1 == w2 + "es":
            return 1
        else:
            try:
                syn1 = wordnet.synset(w1 + ".n.01")
                syn2 = wordnet.synset(w2 + ".n.01")
                return syn1.wup_similarity(syn2)
            except WordNetError:
                return 0

    def is_valid(self):
        if len(self.sentence) > MIN_LENGTH:
            flag = False
            a = (".", "!", "?")
            for s in self.sentence:
                if any(x in s for x in a):
                    flag = True
                if flag and s.isalnum():
                    return False
            return True
        else:
            return False

    def spell_check(self):
        dic = enchant.Dict("en_US")
        if not dic.is_added("$"):  # Create a list for spell check
            dic.add_to_session("$")  # still good to have (for payments)

        new_tokens = []
        for tok in self.filtered:
            if dic.check(tok):  # correctly spelled
                new_tokens.append(tok)
            else:  # improperly spelled: lets find the proper spelling
                suggestions = dic.suggest(tok)
                # possible_suggestions = {}
                # smallest = MAX_DISTANCE + 1
                # takes the first that "works" doesn't take into account frequency...
                for sug in suggestions:
                    distance = dist(tok, sug)
                    if distance <= MAX_DISTANCE:
                        new_tokens.append(sug)
                        break
                #         if distance <= smallest:
                #             smallest = distance
                #             possible_suggestions[distance] = sug
                #             print(possible_suggestions)
                # if smallest != MAX_DISTANCE + 1:
                #     new_tokens.append(possible_suggestions[smallest])
        return new_tokens

    def __str__(self):
        return str(self.sentence)


# main
if __name__ == "__main__":
    with open('output.txt', 'w') as f:
        singularize_plural_noun("patatoes")
        sentences = []
        lines = [line.rstrip() for line in open(SENTENCES, "r")]  # read the sentences from file
        for l in lines:
            sentences.append(Sentence(l))
            sen = sentences[-1]
            print("SENTENCE : " + str(sen))
            if sen.is_valid():
                print(sen.tokens)
                print(sen.tags)
                print(sen.user_form)

                f.write("SENTENCE : " + str(sen) + "\n")
                f.write("TOKENS \t\t\t\t\t: " + str(sen.tokens) + "\n")
                f.write("FILTERED TOKENS : " + str(sen.filtered) + "\n")
                f.write("SPELL CHECK \t\t: " + str(sen.spell_checked) + "\n")
                f.write("TAGGING : " + str(sen.tags) + "\n")
                f.write("DIGITS : " + str(sen.digits) + "\n")
                f.write("USER_FORM : " + str(sen.user_form) + "\n")
            else:
                f.write("INVALID FORMAT!" + "\n")
            f.write("\n\n")
        print("done")
