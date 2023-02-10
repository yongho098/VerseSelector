import requests
from abc import ABC, abstractmethod

class passage_order_error(Exception):
    pass

class Parent_bible(ABC):
    
    def __init__(self, book, start_chapter, start_verse, end_chapter, end_verse):
        self.book = book
        self.start_chapter = start_chapter
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.end_chapter = end_chapter
        self.data = ""
        self.output = ""
        self.validate = version_validator(self)
      
    def save(self):
        pass
        
    def prepare(self):
        # prepares data for read()
        pass
     
    def read(self):
        # parses data from prepare()
        pass

class webapi_bible(Parent_bible):
    def __init__(self, Parent_bible):
        super().__init__(Parent_bible.book, Parent_bible.start_chapter, Parent_bible.start_verse, Parent_bible.end_chapter, Parent_bible.end_verse)
        
        self.url_start = "http://getbible.net/json?passage="
        self.url_end = "&raw=true&version=kjv"
    
    def prepare(self):
        # get raw data
        url = f"{self.url_start}{self.book} {self.start_chapter}: {self.start_verse}-{self.end_verse}{self.url_end}"
                
        try:
            # Use API 
            self.data = requests.get(url).json()
        except:
            # Input has a mistake
            print("Invalid input")
            self.data = None
            raise passage_order_error
            
    def read(self):
        # multiple verse, assumes verses given are correct during init
        verse_upper = self.data["book"][0]["chapter"]
        current_verse = int(self.start_verse)
        for verse in range(len(verse_upper)):
            verse_lower = verse_upper[str(current_verse)]["verse"]
            self.output += f"{current_verse}: {verse_lower}"
            current_verse += 1 

class version_validator:
    # passage parse, verse parse
    def __init__(self, bible):
        self.bible = bible

    def passage_prepare(self):
        self.bible.prepare()
        
    def passage_parse(self):
        self.bible.read()

class version_creator:
    # create bible type?, return bible
    def __init__(self, parsed_passage):
        #condition to check which bible version is
        # test connection to api
        self.bible_output =  webapi_bible(Parent_bible(parsed_passage[0][0], parsed_passage[0][1], parsed_passage[0][2], parsed_passage[0][3], parsed_passage[0][4]))
        
class Display():
    
    def __init__(self, bible):
        self.bible = bible
    
    def printout(self):
        print(self.bible.output)