from operator import index
import os
from bs4 import BeautifulSoup
import re
import json


inverted_index = {}


def tokenize(text):
    tokens = []
    lines = text.split('\n')
    for line in lines:
        for word in re.split(r'\W+', line):
            if word.isalnum() and word.isascii() and word != '':
                # Stemming here
                tokens.append(word.lower())
    return tokens


def indexer():
    for folder in os.listdir('DEV'):
        for file in os.listdir(os.path.join('DEV', folder)):
            with open(os.path.join('DEV', folder, file), 'r') as f:
                data = json.load(f)
                #soup = BeautifulSoup(data['content'], 'lxml')
                tokens = tokenize(data['content'])
                tokensFrequency = dict()
                for token in tokens:
                    if token not in tokensFrequency:
                        tokensFrequency[token] = 0
                    tokensFrequency[token] += 1
                for token, frequency in tokensFrequency.items():
                    if token not in inverted_index:
                        inverted_index[token] = set()
                    inverted_index[token].add((data['url'], frequency))

    for key, value in inverted_index.items():
        print(f'{key}: {value}')



if __name__ == '__main__':
    indexer()
