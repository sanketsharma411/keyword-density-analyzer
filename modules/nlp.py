"""
Natural Language proecssing module for Word density analyzer

Based off of NLTK, Stanford NER Tagger
"""

import nltk

def word_tokenize(text):
    """ Splits text into words
    
    Input : String
    Output: Iterable of words in the string
    
    Method : Splits at white spaces
    
    TODO : use better/other NLTK modules to for the task
    """
    return nltk.word_tokenize(text)

def sent_tokenize(text):
    """ Splits text into sentences 
    
    Input : String
    Output: Iterable of string sentences
    
    Method : Split at full-stops
    
    TODO : use better/other NLTK modules for the task
    """
    return nltk.sent_tokenize(text)



import os
java_path = "C:/Program Files/Java/jdk1.7.0_71/bin/java.exe"
os.environ['JAVAHOME'] = java_path


## Downloaded the following modules from 
# Download Stanford Named Entity Recognizer version 3.4 : http://nlp.stanford.edu/software/stanford-ner-2014-06-16.zip

ner_tagger_jar = '../modules/stanford-ner-2014-06-16/stanford-ner.jar'
tagger_path = '../modules/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz'

from  nltk.tag import StanfordNERTagger
st = StanfordNERTagger(tagger_path,ner_tagger_jar)

def NERTagger(text):
    if type(text) is not list:
        text = word_tokenize(text)
    return st.tag(text)





def sent_chunker(text):
    """ Convert text into POS tagged sentences
    
    Input : String of the text
    Output: List of sentence NLTK.trees
    
    
    Credits for this function : https://gist.github.com/onyxfish/322906
    """
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = list(nltk.ne_chunk_sents(tagged_sentences, binary=True))
                             
    return chunked_sentences
    
    
def extract_entity_names(tree):
    """ Extract named entities from NLTK.Trees
    
    
    Input : A single tree obtained from sent_chunker
    Output: A list of named entities from each tree
    
    Credits for this function : https://gist.github.com/onyxfish/322906
    """
    entity_names = []

    if hasattr(tree, 'label') and tree.label:
        if tree.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                entity_names.extend(extract_entity_names(child))

    return entity_names

    
    
def pos_tag(text):
    """ Generate POS tags for the entered text
    
    Input : tokens or string
    Output: List of tuples with first element the token and second one the POS tag
    """
    if type(text) is str:
        text = word_tokenize(text)
    return nltk.pos_tag(text)    