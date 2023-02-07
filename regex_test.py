import re
import scriptures

print(scriptures.extract('This is a test Rom 3:23-5000 and psalm 17-18:2'))


# txt = "1 john 3:16-90"
# x = re.search("\b[a-zA-Z]+(?:\s+\d+)?(?::\d+(?:–\d+)?(?:,\s*\d+(?:–\d+)?)*)?", txt)
# y = re.search("john", txt)
# print(x)