# Author: Omar Osman
# Email: oosman@umass.edu
# Spire ID: 33851978

import urllib.request
import search
import string
import sys
import re
def read_article_file(url):
    req = urllib.request.urlopen(url)
    text = req.read()
    text = text.decode('UTF-8')
    return text

def text_to_article_list(text):
    lis = re.split('<NEW ARTICLE>', text, flags = re.IGNORECASE)
    for obj in lis:
        if obj == "":
            lis.remove(obj)
    return lis
def split_words(text):
    total = []
    lines = text.splitlines()
    for line in lines:
        words = line.split()
        for word in words:
            total.append(word)
    return total
    
def scrub_word(text):
    new_text = text.strip(string.punctuation)
    return new_text

def scrub_words(words):
    new_list = []
    for word in words:
        lower_word = word.lower()
        new_word = lower_word.strip(string.punctuation)
        new_word = new_word.strip()
        if new_word == "":
            continue
        else:
            new_list.append(new_word)
    return new_list

def build_article_index(article_list):
    article_index = {}
    for index, article in enumerate(article_list):
        words = split_words(article)
        scrubbed_words = scrub_words(words)
        for word in scrubbed_words:
            if word not in article_index:
                article_index[word] = set()
            article_index[word].add(index)     
    return article_index

def find_words(keywords, index):
    intersect_docs = set()
    for keyword in keywords:   
        if keyword not in index:
            return intersect_docs
        if len(intersect_docs) == 0:
            intersect_docs = index[keyword]
        else:
            intersect_docs = intersect_docs.intersection(index[keyword])
    return intersect_docs  

if __name__ == "__main__":
    #print(search.read_article_file('https://bityl.co/Flzb'))
    #text_test = search.read_article_file('https://bityl.co/Flzb')
    #text_test = search.read_article_file('https://bityl.co/Fm50')
    #print(search.text_to_article_list(text_test))
    #print(split_words("dog cat \n1978\n 21 bear \nmouse\n"))
    #print(scrub_word("!@%&&@$text chatter here testing!!@#@!#@!"))
    #test_words = search.split_words('dog, ,cat! !@#$yikes$#@!       ')
    #print(search.scrub_words(test_words))
    #print(build_article_index(search.text_to_article_list(text_test)))
    document = sys.argv[1]
    command = sys.argv[2]
    keyword_or_index = sys.argv[3]
    #command = "find"
    #document = "https://bityl.co/Fm7v"
    #keyword_or_index = "life moon"

    if command == "print":
        lis = text_to_article_list(read_article_file(document))
        print(lis[int(keyword_or_index)])
    elif command == "find":
        keywords = split_words(keyword_or_index)
        sett = find_words(keywords, build_article_index(text_to_article_list(read_article_file(document))))
        for number in sett:
            print(str(number), end = " ")