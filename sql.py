import sqlite3

# conn = sqlite3.connect('sqbible.db')
# print('opened database successfully')

# cursor = conn.execute("SELECT b, c, v, t from t_kjv where b = 2 and c = 2")

# for row in cursor:
#    print (f"book = {row[0]}")
#    print (f"chapter = {row[1]}")
#    print (f"verse = {row[2]}") 
#    print (f"text = {row[3]}\n")

# print(type(cursor))
# conn.close()

#dictionary of books and count
# 1-39, ot. 40-66 nt.
books = {'Genesis': 1,
         'Exodus': 2,
         'Leviticus': 3,
         'Numbers': 4,
         'Deuteronomy': 5,
         'Joshua': 6,
         'Judges': 7,
         'Ruth': 8,
         '1 Samuel': 9,
         '2 Samuel': 10,
         '1 Kings': 11,
         '2 Kings': 12,
         '1 Chronicles': 13,
         '2 Chronicles': 14,
         'Ezra': 15,
         'Nehemiah': 16,
         'Esther': 17,
         'Job': 18,
         'Psalms': 19,
         'Proverbs': 20,
         'Ecclesiastes': 21,
         'Song of Solomon': 22,
         'Isaiah': 23,
         'Jeremiah': 24,
         'Lamentations': 25,
         'Ezekiel': 26,
         'Daniel': 27,
         'Hosea': 28,
         'Joel': 29,
         'Amos': 30,
         'Obadiah': 31,
         'Jonah': 32,
         'Micah': 33,
         'Nahum': 34,
         'Habakkuk': 35,
         'Zephaniah': 36,
         'Haggai': 37,
         'Zechariah': 38,
         'Malachi': 39,
         'Matthew': 40,
         'Mark': 41,
         'Luke': 42,
         'John': 43,
         'Acts': 44,
         'Romans': 45,
         '1 Corinthians': 46,
         '2 Corinthians': 47,
         'Galatians': 48,
         'Ephesians': 49,
         'Philippians': 50,
         'Colossians': 51,
         '1 Thessalonians': 52,
         '2 Thessalonians': 53,
         '1 Timothy': 54,
         '2 Timothy': 55,
         'Titus': 56,
         'Philemon': 57,
         'Hebrews': 58,
         'James': 59,
         '1 Peter': 60,
         '2 Peter': 61,
         '1 John': 62,
         '2 John': 63,
         '3 John': 64,
         'Jude': 65,
         'Revelation of Jesus Christ': 66}

def preparer2(book, chapter):
    # grab entire chapter, sort it in class
    output = []
    conn = sqlite3.connect('sqbible.db')
    # print('opened database successfully')
    cursor = conn.execute(f"SELECT b, c, v, t from t_kjv where b = {books[book]} and c = {chapter}")
    
    for row in cursor:
        output.append(f'{row[3]}')
    conn.close()
    return output
