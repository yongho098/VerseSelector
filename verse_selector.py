import json

import requests

history_list = []
bible_list = []
url_start = "http://getbible.net/json?passage="
url_end = "&raw=true&version=kjv"

class passage_order_error(Exception):
    pass

class passage:
    def __init__(self, book, chapter, verse):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.output = ""
        
    
    def input_sanitize(self):
        if self.chapter.isnumeric():
            pass
        else:
            raise passage_order_error   
    
    def printout(self):
        print(self.output)
        
class passage_multiple_verse(passage):
    def __init__(self, book, chapter, verse):
        super().__init__(book, chapter, verse)
        # sanitize input
        
    
    def input_sanitize(self):
        self.verse_strip = self.verse.split("-")
        for item in range(len(self.verse_strip)):
            self.verse_strip[item] = self.verse_strip[item].strip()
        #error checks
        if len(self.verse_strip) != 2:
            # checks if extra passages inputted
            raise passage_order_error
        elif self.verse_strip[0].isnumeric() and self.verse_strip[-1].isnumeric():
            if int(self.verse_strip[0]) >= int(self.verse_strip[-1]):
                # checks if verses are numbers and ascending
                raise passage_order_error
        else:
            raise passage_order_error
        self.verse_start = self.verse_strip[0]
        self.verse_end = self.verse_strip[-1]
        
class passage_single_verse(passage):
    def __init__(self, book, chapter, verse):
        super().__init__(book, chapter, verse)
        
    def input_sanitize(self):
        if self.chapter.isnumeric() and self.verse.isnumeric():
            pass
        else:
            raise passage_order_error   
        

def main_funct():
    """Takes an input and prints out the verse""" 
    while True:
        # Get verse requested or exit, can use multiple inputs
        book = input("What book are you looking for? Type E to exit. Type H for history.\n")
        if book.lower() == "e":
            exit()
        elif book.lower() == "h":
            history_check()
            continue
        
        chapter = input("What chapter are you looking for?\n")        
        verse = input("What verses are you looking for?\n")
        
        # create passage using inputs
        current = create_passage(book, chapter, verse)
        if current == None:
            # passage input error on passage
            continue
        if current.output != "":
            # duplicate
            current.printout()
            continue
        
        url = create_url(current)
        try:
            # Use API 
            response = requests.get(url).json()
        except:
            # Input has a mistake
            history_list.pop()
            print("Invalid input")
            continue
        # parse and save output
        passage_parse(current, response)
        current.printout()
        
def passage_parse(passage_input: passage, request: json):
    # parse the request and assign to output
    if isinstance(passage_input, passage_multiple_verse):
        # multiple verse, assumes verses given are correct during init
        verse_upper = request["book"][0]["chapter"]
        current_verse = int(passage_input.verse_start)
        for verse in range(len(verse_upper)):
            # add each verse individually
            verse_lower = verse_upper[str(current_verse)]["verse"]
            passage_input.output += f"{current_verse}: {verse_lower}"
            current_verse += 1

    elif isinstance(passage_input, passage_single_verse):
        #single verse
        verse_upper = request["book"][0]["chapter"]
        verse_lower = verse_upper[passage_input.verse]["verse"]
        passage_input.output += f"{passage_input.verse}: {verse_lower}"
        
    elif isinstance(passage_input, passage):
        #whole chapter-parent class
        verse_upper = request["chapter"]
        current_verse = 1
        for verse in range(len(verse_upper)):
            # add each verse individually
            verse_lower = verse_upper[str(current_verse)]["verse"]
            passage_input.output += f"{current_verse}: {verse_lower}"
            current_verse += 1
            
def history_check():
    for previous_passage in history_list:
        if  isinstance(previous_passage, passage_single_verse):
            # verses
            print(f'{previous_passage.book} {previous_passage.chapter}: {previous_passage.verse} - {previous_passage.output}')
        elif isinstance(previous_passage, passage_multiple_verse):
            print(f'{previous_passage.book} {previous_passage.chapter}: {previous_passage.verse}')
        else:
            # whole chapter
            print(f'{previous_passage.book} {previous_passage.chapter}')

def duplicate_check(history_list: list, book: str, chapter: str, verse: str):
    # goes through history_list to see if given input is a duplicate
    for output_index in range(len(history_list)):
        if history_list[output_index].book == book and history_list[output_index].chapter == chapter and history_list[output_index].verse == verse:
            return output_index
    return -1

def create_passage(book: str, chapter: str, verse: str):
    # creates a passage using given inputs
    results = duplicate_check(history_list, book, chapter, verse)
    if results < 0:
        # unique verse
        if(verse == ""):
            # whole chapter
            try:
                history_list.append(passage(book, chapter, verse))
                history_list[-1].input_sanitize()
            except passage_order_error:
                history_list.pop()
                print("Passage Input Error")
                return None
            return history_list[-1]
        else:
            # check if verse or passage 
            if "-" in verse:
                try:
                    history_list.append(passage_multiple_verse(book, chapter, verse))
                    history_list[-1].input_sanitize()
                except passage_order_error:
                    history_list.pop()
                    print("Passage Input error")
                    return None
            else:
                # single verse
                try:
                    history_list.append(passage_single_verse(book, chapter, verse))
                    history_list[-1].input_sanitize()
                except passage_order_error:
                    history_list.pop()
                    print("Passage Input Error")
                    return None
            return history_list[-1]
    else:
        # duplicate verse
        # only add to list if not at the end
        if history_list[-1] == history_list[results]:
            pass
        else:
            history_list.append(history_list[results])
            history_list.pop(results)
        return history_list[-1]

def create_url(passage_in):
    # creates url based on if looking for whole chapter or verse
    if isinstance(passage_in, passage_multiple_verse) or isinstance(passage_in, passage_single_verse):
        # verse/passage
        return f"{url_start}{passage_in.book} {passage_in.chapter}: {passage_in.verse}{url_end}"
    else:
        # whole chapter
        return f"{url_start}{passage_in.book} {passage_in.chapter}{url_end}"

main_funct()