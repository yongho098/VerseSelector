import json

import requests
from abc import ABC, abstractmethod

url_start = "http://getbible.net/json?passage="
url_end = "&raw=true&version=kjv"

class passage_order_error(Exception):
    pass

class Parent_bible(ABC):

    def __init__(self, book, chapter, verse, bible_type) -> None:
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.data = ""
        self.output = ""
        self.bible_type = bible_type
        self.validate = version_validator(self.bible_type)
        self.passage_type = ""
        self.verse_start = 0
      
    def save(self):
        pass
        
    def prepare(self):
        # prepares data for read()
        pass
     
    def read(self):
        # parses data from prepare()
        pass
    
    def passage_version(self):
        if(self.verse == ""):
            # whole chapter
            self.passage_type = "chapter"
        else:
            # check if verse or passage 
            if "-" in self.verse:
                self.passage_type = "passage"
            else:
                # single verse
                self.passage_type = "verse"

class webapi_bible(Parent_bible):
    def __init__(self, Parent_bible) -> None:
        super().__init__(Parent_bible.book, Parent_bible.chapter, Parent_bible.verse, Parent_bible.bible_type)
        
        self.url_start = "http://getbible.net/json?passage="
        self.url_end = "&raw=true&version=kjv"
    
    def prepare(self):
        # get raw data
        if self.passage_type == "passage" or self.passage_type == "verse":
            # verse/passage
            url = f"{url_start}{self.book} {self.chapter}: {self.verse}{url_end}"
        else:
            # whole chapter
            url = f"{url_start}{self.book} {self.chapter}{url_end}"
        try:
            # Use API 
            self.data = requests.get(url).json()
        except:
            # Input has a mistake
            print("Invalid input")
            
    def read(self):
        if self.passage_type == "passage":
            # multiple verse, assumes verses given are correct during init
            verse_upper = self.data["book"][0]["chapter"]
            current_verse = int(self.verse_start)
            for verse in range(len(verse_upper)):
                # add each verse individually
                verse_lower = verse_upper[str(current_verse)]["verse"]
                self.output += f"{current_verse}: {verse_lower}"
                current_verse += 1
        elif self.passage_type == 'verse':
            #single verse
            verse_upper = self.data["book"][0]["chapter"]
            verse_lower = verse_upper[self.verse]["verse"]
            self.output += f"{self.verse}: {verse_lower}"
            
        elif self.passage_type == 'chapter':
            #whole chapter-parent class
            verse_upper = self.data["chapter"]
            current_verse = 1
            for verse in range(len(verse_upper)):
                # add each verse individually
                verse_lower = verse_upper[str(current_verse)]["verse"]
                self.output += f"{current_verse}: {verse_lower}"
                current_verse += 1        

class version_validator:
    # passage parse, verse parse
    def __init__(self, bible) -> None:
        self.bible = bible

    def passage_prepare(self):
        self.bible.prepare()
        
    def passage_parse(self):
        self.bible.read()

class version_creator:
    # create bible type?, return bible
    def __init__(self, book, chapter, verse, bible_type):
        try:
            if bible_type.lower() == 'webapi':
                self.bible_output =  webapi_bible(Parent_bible(book, chapter, verse, bible_type))
            # future planned types: db_bible, text_bible, xml_bible, json_bible    
            else:
                raise passage_order_error
        except passage_order_error:
            print("error")
            exit()
        self.passage_type()
    
    def passage_type(self) -> None:
        # set passage type and error check input
        if(self.bible_output.verse == ""):
            # whole chapter
            if self.bible_output.chapter.isnumeric():
                pass
            else:
                raise passage_order_error   
            self.bible_output.passage_type = "chapter"
        elif "-" in self.bible_output.verse:
            # passage
            verse_strip = self.bible_output.verse.split("-")
            for item in range(len(verse_strip)):
                verse_strip[item] = verse_strip[item].strip()
            #error checks
            if len(verse_strip) != 2:
                # checks if extra passages inputted
                raise passage_order_error
            elif verse_strip[0].isnumeric() and verse_strip[-1].isnumeric():
                if int(verse_strip[0]) >= int(verse_strip[-1]):
                    # checks if verses are numbers and ascending
                    raise passage_order_error
            else:
                raise passage_order_error
            self.bible_output.verse_start = verse_strip[0]
            self.bible_output.passage_type = "passage"
        else:
            # single verse
            if self.bible_output.chapter.isnumeric() and self.bible_output.verse.isnumeric():
                pass
            else:
                raise passage_order_error
            self.bible_output.passage_type = "verse"      
    
class Display():
    
    def __init__(self, bible):
        self.bible = bible
    
    def printout(self):
        print(self.bible.output)
    
def main():
    
    """Takes an input and prints out the verse""" 
    while True:
        # Get verse requested or exit, can use multiple inputs
        book = input("What book are you looking for? Type E to exit.\n")
        if book.lower() == "e":
            exit()
        
        chapter = input("What chapter are you looking for?\n")        
        verse = input("What verses are you looking for?\n")
        bible_type = input("Where do you want the source from? (Currently only webapi)\n")
        
        bible = version_creator(book, chapter, verse, bible_type)
        validator = version_validator(bible.bible_output)
        validator.passage_prepare()
        validator.passage_parse()
        output = Display(bible.bible_output)
        output.printout()

main()