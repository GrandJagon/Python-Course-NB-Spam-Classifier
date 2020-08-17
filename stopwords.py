#Module exporting the stopwords from a json file
import json as js


with open('stopwords.json', 'r') as read:
    content = js.load(read)

stopwords = content['words']






