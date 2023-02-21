import pytest
import bible_class

test_passage = [('John', 3, 16, 3, 16)]

def test_create_webapi():
       # Test bibles created properly
       api_test = bible_class.version_creator(test_passage)
       assert isinstance(api_test.bible_output, bible_class.webapi_bible) == True
       
def test_url():
       # Test url is parsed correctly
       api_test = bible_class.version_creator(test_passage)
       api_test.bible_output.prepare()
       assert api_test.bible_output.data != None

def test_read():
       # Test output works correctly
       api_test = bible_class.version_creator(test_passage)
       api_validator = bible_class.version_validator(api_test.bible_output)
       api_validator.passage_prepare()
       api_validator.passage_parse()
       assert '16: For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.' in api_validator.bible.output
