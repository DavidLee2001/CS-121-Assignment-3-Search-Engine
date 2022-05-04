import os
from bs4 import BeautifulSoup
import re
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


ps = PorterStemmer()

inverted_index = {}


# Not needed as the word_tokenize (and PortreStemmer) is used; keeping it for reference
'''
def tokenize(text):
    tokens = []
    lines = text.split('\n')
    for line in lines:
        for word in re.split(r'\W+', line):
            if word.isalnum() and word.isascii() and word != '':
                # Stemming here
                tokens.append(word.lower())
    return tokens
'''


def indexer():    
    for folder in os.listdir('DEV'):
        if folder == '.DS_Store': continue      # .DS_Store gets created automatically; no need to delete it all the time
        for file in os.listdir(os.path.join('DEV', folder)):
            if file == '.DS_Store': continue    # .DS_Store gets created automatically; no need to delete it all the time
            with open(os.path.join('DEV', folder, file), 'r') as f:
                data = json.load(f)
                content = data['content']

                # Need this block of code to use BeautifulSoup without warnings (still need to add more)
                # May not be able to use BeautifulSoup as not all JSON files are well-formatted
                '''
                # Index 20 was chosen to check the document type; doesn't necessarily have to be 20
                if '!DOCTYPE HTML' in content[:20] or '!DOCTYPE html' in content[:20]:      # Use 'lxml' parser
                    soup = BeautifulSoup(content, 'lxml')
                elif content[1:5] == '?xml':                                                # Use 'xml' parser
                    soup = BeautifulSoup(content, 'xml')
                else:                                                                       # Manual string processing
                    #soup = BeautifulSoup(content, 'lxml')
                    #print(soup.title, soup.text[:10])
                    return
                '''

                # Need to pass in the actual content to the 'word_tokenize' function instead of the entire HTML (need to use BeautifulSoup)
                stemmed_tokens = [ps.stem(token) for token in word_tokenize(content)]
                # May need to modify PorterStemmer to take word importance into account

                tokensFrequency = dict()
                for token in stemmed_tokens:
                    if token not in tokensFrequency:
                        tokensFrequency[token] = 0
                    tokensFrequency[token] += 1
                for token, frequency in tokensFrequency.items():
                    if token not in inverted_index:
                        inverted_index[token] = set()
                    # The url is the ID
                    inverted_index[token].add((data['url'], frequency))

    for key, value in inverted_index.items():
        print(f'{key}: {value}')




if __name__ == '__main__':
    indexer()
