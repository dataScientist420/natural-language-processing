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
from nltk.stem import PorterStemmer
from nltk.corpus import state_union
from nltk import pos_tag
from nltk import RegexpParser
from nltk import ne_chunk

sentence = "It is very important to be pythonly while you are pythoning with python!"

if __name__ == "__main__":
    # TOKENISATION
    words = tokenize.word_tokenize(sentence)

    # STOPPING UNUSELESS WORDS
    stop_words = set(stopwords.words("english")) 
    filtered_words = [w for w in words if w not in stop_words]

    # STEMMING
    porter_stem = PorterStemmer()
    new_sentence = ""
    for w in sentence: new_sentence += porter_stem.stem(w)

    # SPEECH TAGGING 
    postag = pos_tag(words)

    # CHUNKING
    regex = RegexpParser("Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}")
    chunk = regex.parse(postag)
    chunk.draw()

    # ENTITY RECOGNITION
    entity = ne_chunk(postag)
    entity.draw()
    
    print "\nSENTENCE\n", sentence
    print "\nTOKENS\n", words
    print "\nFILTERED WORDS\n", filtered_words  
    print "\nSTEMMING\n", new_sentence
    print "\nTAGGING\n", postag
