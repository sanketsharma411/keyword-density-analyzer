import sys
sys.path.append('modules/')
from webpage import *
import nlp



def get_meta_info(w):
    """ Extract relevant information from the website metadata"""
    
    # List of proper nouns from the title
    title_nouns = [tag for tag,token in nlp.reduced_pos_tag(w.title) if token == 'NNP']
    
    # List of processed meta_keywords
    keywords = nlp.pre_process(w.meta_keywords)
    
    # List of procesed tags
    tags = nlp.pre_process(' '.join(w.tags))
    
    return title_nouns,keywords,tags


def get_entities(text):
    """ Return the top 25% entities sorted by frequency """
    tagged_entity_count = nlp.entity_count(text) 
    entity_count = {entity:tagged_entity_count[tag][entity]
                    for tag in tagged_entity_count
                        for entity in tagged_entity_count[tag] }
    return [entity 
                for entity,count in sorted(entity_count.items(),key = lambda x:x[1], reverse = True)[:int(len(entity_count)/4)]
            if count > 2 ]


def get_ngrams(text,k1=10,k2=5,k3=2):
    """ Obtain relevant ngrams for the entered text """
    unigrams,bigrams,trigrams = nlp.ngram(text)

    
    relevant_unigrams = [unigram[0] for unigram,count in sorted(unigrams.items(), key = lambda x:x[1], reverse = True) 
                                 ][:len(unigrams)/k1]
    relevant_bigrams = [' '.join(bigram) for bigram,count in sorted(bigrams.items(), key = lambda x:x[1], reverse = True) 
                                 ][:len(bigrams)/k2]
    relevant_trigrams = [' '.join(trigram) for trigram,count in sorted(trigrams.items(), key = lambda x:x[1], reverse = True) 
                                 ][:len(trigrams)/k3]
    
    relevant_trigrams.extend(relevant_bigrams)
    relevant_trigrams.extend(relevant_unigrams)
    
    return relevant_trigrams


def validate(url):
    """ Check if it is a valid url or not"""
    pass


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def word_density_analyze(url):
    """ List of topics that describe the page """
    
    
    validate(url)
    w = Webpage(url)
    print "Loading the WebPage"
    w.load()
    print "Loading the WebPage !! COMPLETED !!"
    
    
    # First the meta    
    print "Extracting Meta Data"
    title_nouns,keywords,tags = get_meta_info(w)
    print "Extracting Meta Data !! COMPLETED !!"
    
    # Then the ner tags
    print "Extracting Entities (this may take a while)"
    entities = get_entities(w.text)
    print "Extracting Entities (this may take a while) !! COMPLETED !!"
    
    # Then the ngram counts
    print "Extracting ngram counts (this should be faster than Entities)"
    relevant_ngrams = get_ngrams(w.text)
    print "Extracting ngram counts (this should be faster than Entities) !! COMPLETED !!"
    
    
    print 'Generating Result'
    result = []
    keywords_used = False
    tags_used = False
    ngrams_used = False
    result.extend(title_nouns)
    
    result.append('\n')
    
    if len(keywords) <= 2:
        result.extend(keywords)
        keywords_used = True
        
    if len(tags) <= 2:
        result.extend(tags)
        tags_used = True
        
    result.extend(entities)    
    
    result.append('\n')
    
    if len(keywords) > 5 or len(tags) > 3:
        result.extend(relevant_ngrams)
    
    if not keywords_used:
        result.extend(keywords)
    
    if not tags_used:
        result.extend(tags)
    
    result.append('\n')
    
    if not ngrams_used:
        result.extend(relevant_ngrams)
    
    
    return remove_duplicates(result)


if __name__ == '__main__':
    

    print '==='.join('='*20)
    print 'Processing the webpage '
    print '==='.join('='*20)

    
    results = word_density_analyze('https://en.wikipedia.org/wiki/Georgia_Institute_of_Technology_College_of_Computing')
    #results = word_density_analyze("http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/")
    
    print '==='.join('='*20)
    print 'The Results '
    print '==='.join('='*20)
    
    print '\n'.join(results)
