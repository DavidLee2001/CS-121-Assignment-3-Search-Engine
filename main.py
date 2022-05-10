import os
from bs4 import BeautifulSoup
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



ps = PorterStemmer()

numDocuments = 0
inverted_index = dict()
url_index = dict()



def indexer():
    global numDocuments
    if not os.path.exists('Indexes'): os.mkdir('Indexes')
    docID = 0
    for folder in os.listdir('DEV'):
        indexes = dict()
        if folder == '.DS_Store': continue          # .DS_Store gets created automatically; no need to delete it all the time
        for file in os.listdir(os.path.join('DEV', folder)):
            if file == '.DS_Store': continue        # .DS_Store gets created automatically; no need to delete it all the time
            numDocuments += 1
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

                if data['url'] not in url_index:
                    docID += 1
                    url_index[data['url']] = docID

                # Need to pass in the actual content to the 'word_tokenize' function instead of the entire HTML (need to use BeautifulSoup)
                stemmed_tokens = [ps.stem(token) for token in word_tokenize(content) if token.isalnum()]
                # May need to modify PorterStemmer to take word importance into account

                tokensFrequency = dict()
                for token in stemmed_tokens:
                    if token not in tokensFrequency:
                        tokensFrequency[token] = 0
                    tokensFrequency[token] += 1
                for token, frequency in tokensFrequency.items():
                    if token not in indexes:
                        indexes[token] = set()
                    indexes[token].add((url_index[data['url']], frequency))
                    if token not in inverted_index:
                        inverted_index[token] = set()
                    inverted_index[token].add((url_index[data['url']], frequency))
        
        # Store the indexes to a file with the same name as the folder (one index file for each folder)
        with open(f'Indexes/{folder}.ser', 'w') as file:
            file.write(str(indexes))
        
    # Store URL/integer HashMap
    with open(f'docID.ser', 'w') as file:
        file.write(str(url_index))


if __name__ == '__main__':
    indexer()



    # Report - MS 1
    print(f'Number of Documents: {numDocuments}\n\n')

    print(f'Number of (Unique) Words: {len(inverted_index)}\n\n')

    print(f"Total Size of Index: {sum([os.path.getsize(os.path.join('Indexes', file)) for file in os.listdir(os.path.join(os.getcwd(), 'Indexes')) if file.endswith('.ser')] + [os.path.getsize('docID.ser')])} bytes")
