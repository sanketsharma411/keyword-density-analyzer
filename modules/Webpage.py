class Webpage:
    """ The core Webpage Class 
    
    Every page which we analyze would be an instance of this class.
    It is suppossed to serve as a collection of webpage attributes
    
    Attributes:
        url   : the url for this webpage
        text  : The cleaned text of the main article of the webpage
        title : 
        tags  : 
        meta_description:
        meta_keywords   :
        html : Complete HTML of the webpage
        __goose_article__: The inherent goose article which was used to populate these fields
    
    
    Methods:
        load(): Will load the url, and parse it to populate the data members of the object
        
        
    Not a lot of time has been spent in designing this class, so there are a couple of additions left
    
    TODO_1: NYTimes - None of the two methods seem to work for NYTimes, so design another parser using beautiful-soup
        which would be able to parse these sites well.
    TODO_2: Add other fields of data obtained from goose like author, movies, tweets etc..
    TODO_3: Incorporate other sources of data: 
        The only data related to the webpage is obtained from goose. You can also look at other sources of data like wikipedia, or 
        some place where we can get info about a site given its url.
    
    """
    
    def __init__(self,url = ''):
        self.url = url
        self.text= ''
        self.title = ''
        self.tags = []
        self.meta_description = ''
        self.meta_keywords = []
        self.html = ''
        self.__goose_article__ = None
        
    def set_url(self,url):
        """ Function to set the url for this webpage"""
        # if needed check to make sure you are not over writing og url 
        self.url = url
        
    def load(self):
        """ Load, parse the URL and store its results into instance variables
        
        If goose is unable to extract the article correctly, we switch to html2text to do the same
        """
        g = Goose()
        if not self.url:
            raise ValueError('URL not set please use webpage.set_url(url) to set it')
        self.__goose_article__ = g.extract(url = self.url)
        
        self.html = self.__goose_article__.raw_html
        self.title= self.__goose_article__.title
        self.tags = self.__goose_article__.tags
        self.meta_description = self.__goose_article__.meta_description
        self.meta_keywords = self.__goose_article__.meta_keywords
        
        # Now check if goose was able to extract the main content from the url correctly or not
        if not self._valid_text_():
            # if it is not valid, we fall back to html2txt for extracting the main text
            h = html2text.HTML2Text()
            h.ignore_links = True
            self.text = h.handle(self.html.decode('utf8'))
        else:
            self.text = self.__goose_article__.cleaned_text
            
        # If you do not have anything into text now, we raise an error because we are not very sure about
        # the accuracy/performance of the parsing, so we raise a valueerror
        
        # Now this error is raised after all the required parameters in the instance are populated,
        # so even if the user chooses to do nothing with the error, it would work
        if len(self.text.strip()) == 0:
            #    raise ValueError('Unable to correctly parse given URL:%s' %self.url)

            # I guess just warning the user is enough, then it is his call to proceed with this or not
            # if we raise an error we are telling,no, yelling at him to stop
            warn('Unable to correctly parse given URL:%s' %self.url)
        
    

    
    def _valid_text_(self):
        """ Check if the text extracted by goose is valid or not base on some heuristic 
        
        Here we can have multiple definitions checking if goose works or not
        The most trivial (and quick to compute) one would be if length of the extracted text is less than 100 letters
        
        Input : 
            - webpage object
        Return : 
            - boolean
        """
        if not self.__goose_article__:
            raise ValueError("goose article not initialized, use webpage.load() to initialize it")
        
        return len(self.__goose_article__.cleaned_text) > 100