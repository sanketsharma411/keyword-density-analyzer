
## Folder Structure:
```
/modules
/docs
/scripts
/flask-app
```


## Testing Websites
1. http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster <br>
Should return <br>
 2-Slice Toaster, Cuisinart CPT-122, Compact toaster

2. http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/
3. http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/



## Questions
1. Upper bound/limit on memory or page size ?
    We may fall into trouble with 3-gram models  

2. Confidence: With every rank also include a general confidence score of how confident you are about the topics. So for a small text with around 10 words you may not be very confident about the results.

3. Question of sensitivity vs specificity
    - Do we rank everything and return the entire ranking
    - Return top k ranks ?

## Analyzing the Content

Content Analysis in Python:
  http://conjugateprior.org/software/ca-in-python/
  
When we google this project we get figure out that it is an important SEO tool  
  Google : analyze web page for keywords
  
#### NewsPaper
Also there is a list of common news websites there

  We can pick them but would need to be smart with disclosing their source
  
He does a bunch of NLP here

  https://github.com/codelucas/newspaper/blob/master/newspaper/nlp.py
https://pypi.python.org/pypi/newspaper
http://newspaper.readthedocs.org/en/latest/


#### Python-coreference resoultion
https://groups.google.com/forum/#!topic/nltk-users/g1MsgI2PxXU


#### Python-goose

Extract article and title separately
https://github.com/grangier/python-goose
https://code.google.com/p/nltk-drt/
https://pypi.python.org/pypi/goose-extractor/

#### diff-bot
SEO Tool which does a better extraction similar to goose but it is a web-based product

#### Libextract
"Statistics-enabled" data extraction library working with HTML

