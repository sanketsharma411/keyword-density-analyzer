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



##################################################################################
###  from ngrams.ipynb
##################################################################################
import re, string

from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

'''
Pre-processing
For certain nlp tasks like keyword count, detection, ngram count we may need to pre-process the data i.e. filter out stop words
But stuff like ner_tagger,pos_tagger and others may not enjoy working with the processed text
So the pre-processing we hence define would only be specific to use with ngrams
'''

def pre_process(text):
    """ Clean and process the text 
    
    input : String
    output: Tokenized and processed text
    
    Applies certain generic pre-processing steps to make the result more conducive for ngram analysis
    Note: This is done specifically for ngram analysis and some other pre-processing steps might be used 
    based on the downstream nlp-task
    
    Credits for part of the pre-processing to this tutorial 
        http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    """

    #Convert to lower case
    text = text.lower()
    # apostrophe
    text = text.replace("'",'') 
    
    # punctuation
    text = re.sub('['+string.punctuation+']',' ',text)
    
    # keep word if it has an alphabet in it => Remove all numbers and punctuations
    text = re.sub("^[a-z]+$",' ',text)


    #Remove additional white spaces
    text = re.sub('[\s]+', ' ', text)
    
    #trim
    text = text.strip('\'"')
    
    # Now everything occurs at the token level
    
    # Tokenize
    text = word_tokenize(text)
    
    # Stopwords
    text = [wnl.lemmatize(word) for word in text if (word not in stopwords)
                                             and len(word) > 3]
                   
    
    return text

from nltk.util import ngrams

def ngram_count(tokens,n = 1):
    """ Count occurrences of ngrams in passed tokens
    
    
    Input : list/iterable of string tokens
    Output: Dictionary with keys as token and values as their count
    
    Does not apply any pre-processing steps
    """
    
    tokens_ngrams = list(ngrams(tokens,n))
    
    tokens_ngrams_count = {x:tokens_ngrams.count(x) for x in set(tokens_ngrams)}
    
    return tokens_ngrams_count
    

def sorted_ngram_count(tokens,n=1):
    """ Returns the count sorted ngram list of the passed tokens 
    
    Input : list/iterable of string tokens
    Output: List of 2-tuples with first element as token and second as their count
    """
    return sorted(ngram_count(tokens,n).items(),key=lambda x:x[1], reverse = True)