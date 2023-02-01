import json

import requests

history_list = []
bible_list = []
url_start = "http://getbible.net/json?passage="
url_end = "&raw=true&version=kjv"

class Parent_bible:
    def __init__(self, book, chapter, verse) -> None:
        self.book = book
        self.chapter = chapter
        self.verse = verse
        
    def save(self):
        pass
    
    def read(self):
        pass

class webapi_bible(Parent_bible):
    def __init__(self, book, chapter, verse) -> None:
        super().__init__(book, chapter, verse)
    pass

    
class version_validator:
    # passage parse, verse parse
    pass

class version_creator:
    # create bible type?, return bible
    pass

class Display:
    def __init__(self) -> None:
        pass
    
def main():
    
    
    # create version creator, call read
    pass

main()