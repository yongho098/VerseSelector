import json

import requests

# previous verses looked up
history = {}
history_list = []
url_start = "http://getbible.net/json?passage="
url_end = "&raw=true&version=kjv"

class passage_order_error(Exception):
    pass

class passage:
    # parent class-whole chapter
    def __init__(self, book, chapter, verse):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.output = ""
        
    def printout(self):
        print(self.output)
        
class passage_multiple_verse(passage):
    def __init__(self, book, chapter, verse):
        super().__init__(book, chapter, verse)
        # sanitize input
        self.verse_strip = self.verse.split("-")
        for item in range(len(self.verse_strip)):
            self.verse_strip[item] = self.verse_strip[item].strip()
        #error checks
        if len(self.verse_strip) != 2:
            # checks if extra passages inputted
            print("len")
            raise passage_order_error
        elif self.verse_strip[0].isnumeric() and self.verse_strip[-1].isnumeric():
            if int(self.verse_strip[0]) >= int(self.verse_strip[-1]):
                # checks if verses are ascending
                raise passage_order_error
        else:
            print("else")
            raise passage_order_error
        self.verse_start = self.verse_strip[0]
        self.verse_end = self.verse_strip[-1]
        
class passage_single_verse(passage):
    def __init__(self, book, chapter, verse):
        super().__init__(book, chapter, verse)
        

def main_funct():
    """Takes an input and prints out the verse""" 
    while True:
        # Get verse requested or exit, can use multiple inputs
        book = input("What book are you looking for? Type E to exit.\n")
        if book.lower() == "e":
            exit()
        elif book.lower() == "h":
            pass
        chapter = input("What chapter are you looking for?\n")
        verse = input("What verses are you looking for?\n")
        
        # split and strip to sanitize
        verse_components = verse.strip()
        verse_components = verse_components.split("-")
        
        # Parse input, error check
        if(verse == ""):
            # whole chapter
            # check if already exists
            history[f"{book} {chapter} {verse}"] = passage(book, chapter, verse)
            history_list.append(history[f"{book} {chapter} {verse}"])
            current = history_list[-1]
            url = f"{url_start}{current.book} {current.chapter}{url_end}"
        else:
            # check if verse or passage 
            if "-" in verse:
                # passage
                try:
                    history[f"{book} {chapter} {verse}"] = passage_multiple_verse(book, chapter, verse)
                except passage_order_error:
                    print("Passage input error")
                    continue
            else:
                # single verse
                history[f"{book} {chapter} {verse}"] = passage_single_verse(book, chapter, verse)
            history_list.append(history[f"{book} {chapter} {verse}"])
            current = history_list[-1]
            url = f"{url_start}{current.book} {current.chapter}: {current.verse}{url_end}"
        try:
            # Use API 
            response = requests.get(url).json()
        except:
            # Input has a mistake
            print("Invalid input")
            continue
        # parse and save output
        passage_parse(current, response)
        current.printout()
        
def passage_parse(passage_input, request):
    # parse the request and assign to output
    if isinstance(passage_input, passage_multiple_verse):
        # multiple verse, assumes verses given are correct during init
        verse_upper = request["book"][0]["chapter"]
        current_verse = int(passage_input.verse_start)
        for verse in range(len(verse_upper)):
            #print each verse individually
            verse_lower = verse_upper[str(current_verse)]["verse"]
            passage_input.output += f"{current_verse}: {verse_lower}"
            current_verse += 1

    elif isinstance(passage_input, passage_single_verse):
        #single verse
        verse_upper = request["book"][0]["chapter"]
        verse_lower = verse_upper[passage_input.verse]["verse"]
        passage_input.output += f"{passage_input.verse}: {verse_lower}"
        
    elif isinstance(passage_input, passage):
        #whole chapter-parent
        verse_upper = request["chapter"]
        current_verse = 1
        for verse in range(len(verse_upper)):
            #print each verse individually
            verse_lower = verse_upper[str(current_verse)]["verse"]
            passage_input.output += f"{current_verse}: {verse_lower}"
            current_verse += 1

main_funct()