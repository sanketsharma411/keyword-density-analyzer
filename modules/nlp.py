"""
Natural Language proecssing module for Word density analyzer

Based off of NLTK, Stanford NER Tagger

Importing this module may take some time because it loads the NER Tagger
from disk 
"""

import nltk

def word_tokenize(text):
    """ Splits text into words
    
    Input : String
    Output: Iterable of words in the string
    
    Method : NLTK basic word_tokenize

    The idea here is to have a single tokenizer function in our nlp module
    and inside this function you can select/implement any tokenization scheme

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

def ner_tag(text):
    """ Return the tokens and associated NER Tags
    
    input : tokens (strings are fine as well)
    output: list of 2-tuples with first element being the token
            and the second on the tag
            
    Note : This is quite slow a procedure yet quite accurate
    """
    if type(text) is str:
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

def pre_process(text,word_length = 3):
    """ Clean and tokenize the text 
    
    input : String
        optional : word_length : Lower threshold on size of what is considered a valid word
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

# Complete ngram pipeline
def ngram(text,lower_count_threshold = 1):
    """ Computes ngram counts upto n = 3
    
    Input : string text
    output: Tuple  of unigrams,bigrams,trigrams 
            where each element is a dictionary  as follows:
                keys = n of n-gram
                vals = list of 2-tuples
                            first element = token n-gram
                            second element= count
    Rare n-grams which appear <= lower_count_threshold (= 1) times are disregarded 

    """
    tokens = pre_process(text)
    unigrams = {unigram:count for unigram,count in ngram_count(tokens).items() if count > lower_count_threshold}
    bigrams  = {bigram:count for bigram,count in ngram_count(tokens,2).items() if count > lower_count_threshold}
    trigrams = {trigram:count for trigram,count in ngram_count(tokens,3).items() if count > lower_count_threshold}

    return unigrams,bigrams,trigrams

################################################################################
### NER
################################################################################

def merge_same_ner_tags(temp_array):
    """ Merge tokens from the temp array into one token_tag tuple """
    
    merged_token = ' '.join(token_tag[0] for token_tag in temp_array)
    merged_tag = tuple({token_tag[1] for token_tag in temp_array})
    if len(merged_tag) != 1:
        raise ValueError('Trying to merge tokens with different NER tags %s ' %str(temp_array))
    return merged_token,merged_tag[0]

def merge_ner_tags(text_ner_tags):
    """ Combine adjacent tokens with same NER tag into one token"""
    
    merged_ner_tags = []
    temp_array = []
    prev_tag = 'O'
    
    for token_tag in text_ner_tags:
        tag = token_tag[1]
        
        if tag == 'O':
            # There can not be an continuity so empty the array and append the results to merged
            if len(temp_array) != 0:
                # Merge the contents
                m_token,m_tag = merge_same_ner_tags(temp_array)
                merged_ner_tags.append((m_token,m_tag))
                #print temp_array,'!!!'
                temp_array = []
                
            merged_ner_tags.append(token_tag)
            prev_tag = tag
            
        elif prev_tag != 'O' and tag == prev_tag:
            # continue the chain
            temp_array.append(token_tag)
            prev_tag = tag
            
            
        else:
            # current tag != 0 and prev_tag == 0 or tag != prev_tag
            # Start of something new
            if len(temp_array) != 0:
                # Merge the contents
                m_token,m_tag = merge_same_ner_tags(temp_array)
                merged_ner_tags.append((m_token,m_tag))
                #print temp_array,'!!!'
                temp_array = []
            
            temp_array.append(token_tag)
            prev_tag = tag
            
            
    if len(temp_array) != 0:
        merged_token = ' '.join(token_tag[0] for token_tag in temp_array)
        merged_tag = tuple({token_tag[1] for token_tag in temp_array})[0]
        merged_token_tag = (merged_token,merged_tag)
        merged_ner_tags.append(merged_token_tag)
    
    return merged_ner_tags


def reduce_tokens(tokens):
    """ Look at the tokens with the same NER tag and merge them if they are 'similar'
    
    Current definitions of similarity
        Compare the tag with every other tag and if the first tag is a part of a bigger tag
        Then they are probably referring to the same thing, so replace the smaller one by the bigger one
        
    input : list of tokens which have the same NER tag
    Output: list of reduced tokens
    
    TODO : | DONE | Add Abbreviation to similarity thing 
    """
    new_tokens = []
    for token in tokens:
        flag = 0 
        for other_token in sorted(tokens,key = lambda x:len(x), reverse = True):
            if compare_tokens(token,other_token):
                new_tokens.append(other_token)
                flag = 1
                break
        if flag != 1:
            new_tokens.append(token)

    return new_tokens

def compare_tokens(token,other_token):
    """ Compare two tokens to see if they are similar or not
    
    TODO : Extend this function ton include external sources of data like common abbreviaton databases
        maybe look at https://en.wikipedia.org/wiki/Lists_of_abbreviations
    """
    return ((token in other_token
                    and len(other_token) > len(token)
                    and "'s" not in other_token
                    and "of" not in other_token)
                or ("The" in other_token 
                    and token in other_token.replace("The",' ')
                   )
                or (token in get_abbr(other_token))
           )

def get_abbr(st):
    """ Generate an abbreviation of the passed string by some rule and return it 
    
    
    input : string 
    output: set of possible abbreviations
    
    Current method of abbr:
        Pick up first leter of every word
        Capitalize it
            1. One abbr would have it as U.S.
            2. Another abbr would be as US
    
    Thus you cannot abbreviate single word strings
    
    TODO : Use some library/regex thingy to obtain abbreviations faster
    """
    words = st.replace('The','').replace('of','').replace('&','').split()
    if len(words) < 2:
        return {}
    
    first_letters = [word[0].capitalize() for word in words]
    
    abbr_1 = '.'.join(first_letters)+'.'
    abbr_2 = ''.join(first_letters)
    
    return {abbr_1,abbr_2}




def entity_count(text):
    """ Identify and count the number of times an entity appears in some text 
    
    Given a piece of text, return a dictionary with keys as the entity_type 
    (ORGANIZATION,LOCATION,PERSON) and values as a dictionary with keys as entity tokens and values as their counts
    
    input : string text
    output: dictionary

    """
    text_ner_tags = ner_tag(text)
    tagged_entities = [tag for tag in merge_ner_tags(text_ner_tags) if tag[1] != 'O']
    tag_dict = {tag:[x[0] for x in tagged_entities if x[1] == tag] for tag in {x[1] for x in tagged_entities}}
    tag_dict = {tag:reduce_tokens(tag_dict[tag]) for tag in tag_dict}
    tag_entity_count_dict = {tag:{token[0]:count for token,count in ngram_count(tag_dict[tag]).items()} for tag in tag_dict}
    
    return tag_entity_count_dict