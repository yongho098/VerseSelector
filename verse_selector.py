import requests
import json

def main_funct():
    """Takes an input and prints out the verse""" 
    while True:
        # Get verse requested or exit, can use multiple inputs
        book = input("What book are you looking for?\n")
        if book.lower() == "e":
            exit()
        chapter = input("what chapter are you looking for?\n")
        verse = input("what verses are you looking for?\n")
        
        # split and strip to sanitize
        verse_components = verse.strip()
        verse_components = verse_components.split("-")
        
        # Parse input, error check
        if(verse == ""):
            url = f"http://getbible.net/json?passage={book} {chapter}&raw=true&version=kjv"
        else:
            url = f"http://getbible.net/json?passage={book} {chapter}: {verse}&raw=true&version=kjv"
        try:
            # Use API 
            response = requests.get(url).json()
        except:
            # Input has a mistake
            print("Invalid input")
            continue
        passage_print(verse_components, response)
        

def passage_print(verse, request):
    """Helper function to print out the given verses"""
    # Single verse
    if len(verse) == 1:
        if(verse[0] == ""):
            # Entire chapter
            verse_upper = request["chapter"]
            current_verse = 1
            for verse in range(len(verse_upper)):
                #print each verse individually
                verse_lower = verse_upper[str(current_verse)]["verse"]
                print(f"{current_verse}: {verse_lower}")
                current_verse += 1
        else:
            verse_upper = request["book"][0]["chapter"]
            verse_lower = verse_upper[verse[0]]["verse"]
            print(f"{verse[0]}: {verse_lower}")
    elif(len(verse) == 2):
        # Verse passage
        if(int(verse[0]) > int(verse[1])):
            # Check to make sure verses are ascending
            print("Invalid input")
            return
        verse_upper = request["book"][0]["chapter"]
        current_verse = int(verse[0])
        for verse in range(len(verse_upper)):
            #print each verse individually
            verse_lower = verse_upper[str(current_verse)]["verse"]
            print(f"{current_verse}: {verse_lower}")
            current_verse += 1
    else:
        # Multiple verses, not supported form
        print("Invalid input")
        return

main_funct()