## methodology

So the task involves two primary steps
1. Extract Text Data from the website (by scraping HTML)
2. Complete Linguistic Analysis on this text data



### Step I : Scraping

So the first step was to select correct scraping libraries, I spent some time looking around python libraries and found 
python-goose to work best for me( the tests conducted with the libraries are present in labs/1_...ipynb)

Then I had to figure out how to use the python-goose library So played around with it in labs/2_looking_around_goose.ipynb
Now for a couple of times, Goose did not work as expected, so to extract data for such websites where goose fails, I added
a backup of html2text and beautifulsoup

Now a webpage waas central to our task, so I defined the Webpage class which would allow me to easily extract and access web data
(labs/3_Webpage Class.ipynb). I added this class to the modules and this completed the first of the two primary steps


### Step II : Analysis

Now in order to extract information from the text we had to apply certain analysis on it. 

So there are a couple of nlp libraries available, first step was to select the right one (labs/4_selecting_nlp_libs.ipynb')

The most basic analysis would be an n-gram count of all the ngrams present in the text, So I used the nltk library for extracting ngrams from text and 
initialized the nlp module (modules/nlp.py which would hold all nlp computations) with a ngram parser (labs/5_ngrams.ipynb)

Then I felt that the entities involved in a webpage are more important than just the words so I added NER functionality to the nlp module (labs/6_ner.ipynb)

All this while I did not look at metadata i.e. the title, keywords, tags. So I added a POS tagger and selected all Proper Nouns from the title as they are crucial
to what is in the page (labs/7_pos.ipynb)

Then put it all together in (labs/8_analyze.ipyb)