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
from random import randrange

l_sent = ["I would like a babysitter this friday night!",
          "Clear my pool now",
          "babysitter 6 to 8",
          "wash my car",
          "shovel my driveway"]

if __name__ == "__main__":
    # RANDOM SENTENCE
    sentence = l_sent[randrange(0, len(l_sent))]

    # TOKENISATION
    words = tokenize.word_tokenize(sentence)

    # FILTERING TOKENS 
    stop_words = set(stopwords.words("english")) 
    filtered_words = [w for w in words if w not in stop_words]

    # SPEECH TAGGING 
    tags = pos_tag(filtered_words)

    # CHUNKING
    regex = RegexpParser("Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}")
    chunk = regex.parse(tags)
    chunk.draw()

    # ENTITY RECOGNITION
    entity = ne_chunk(tags)
    entity.draw()
    
    print "\nSENTENCE\n", sentence
    print "\nTOKENS\n", words
    print "\nFILTERED nTOKENS\n", filtered_words  
    print "\nTAGGING\n", tags
