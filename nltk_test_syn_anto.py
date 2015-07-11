#!/usr/bin/env python

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

File: nltk_test_syn_anto.py
Description: this file is used for testing the nltk module
Author: Victor Neville
Date: 11-07-2015
*****************************************************************************"""

from nltk.corpus import wordnet

if __name__ == "__main__":
    w0 = "ship"
    w1 = "boat"
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
