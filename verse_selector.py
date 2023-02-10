import json
import scriptures
from bible_class import Display, version_creator, version_validator, passage_order_error, Parent_bible, webapi_bible      
    
def main():
    
    """Takes an input and prints out the verse""" 
    while True:
        # Get verse requested or exit, can use multiple inputs
        # fix continous passages
        passage = input("What passage are you looking for? Type E to exit.\n")
        if passage.lower() == "e":
            exit()
            
        parsed_passage = scriptures.extract(passage)
        if len(parsed_passage) == 0:
            print("Invalid passage")
            continue
        if len(parsed_passage) != 1:
            print("Too many passages")
            continue
                
        try: 
            bible = version_creator(parsed_passage)
        except passage_order_error:
            continue
        validator = version_validator(bible.bible_output)
        try:
            validator.passage_prepare()
        except passage_order_error:
            continue
        validator.passage_parse()
        output = Display(bible.bible_output)
        output.printout()

main()