import json

import time
import ast


from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
ps = PorterStemmer()

def intersect_postings(p1, p2):
    answer = list()

    while len(p1) != 0 and len(p2) != 0:
        if p1[0][0] == p2[0][0]: # comparing docIDs
            answer.append(p1[0])
            p1 = p1[1:]
            p2 = p2[1:]
        else:
            if p1[0][0] < p2[0][0]:
                p1 = p1[1:]
            else:
                p2 = p2[1:]
  
    return answer

if __name__ == '__main__':
    # assume query in merged_index
    # currently returning  postings containing query
        
    with open('term_position.json', 'r') as f1, \
        open('merged_index.txt', 'r') as merged_index, \
        open('docID_position.json', 'r') as f2, \
        open('docID.txt', 'r') as urls:
       
        term_position = json.load(f1)
        docID_position = json.load(f2)
        
        while True:
            query = input("Query: ")

            # for AND query
            stemmed_query_list = [ps.stem(token) for token in word_tokenize(query) if token.isalnum()]
           
            start_time =  time.time_ns()
            
            possible_postings = list()

            for term in stemmed_query_list:
                merged_index_position = term_position[term]
                merged_index.seek(merged_index_position)

                line = merged_index.readline()
                line_list = line.rstrip().split(', ', 1)
                postings = ast.literal_eval('[' + line_list[1][1:-1] + ']')
                
                possible_postings.append(postings)

            # sort because want to process in order of increasing frequency
            possible_postings.sort(key=lambda postings : len(postings))

            result_postings = possible_postings[0]
            for p in possible_postings[1:]:
                result_postings = intersect_postings(result_postings, p)

            # print("docID_freq:", docID_freq)
            counter = 0
            for doc in sorted(result_postings, key=lambda x: -x[1]): # doc is tuple(docID, freq)
                docID = doc[0]
                position = docID_position[str(docID)]
                urls.seek(position)
                url = urls.readline()
                print(url, end='')
                counter += 1
                if counter == 5:
                    break
            
            # result = None

            end_time =  time.time_ns()
            print("Time:", (end_time - start_time) // 1_000_000, "ms")

 
    # query = input("Query: ")
    # stemmed_tokens = [ps.stem(token) for token in word_tokenize(query) if token.isalnum()]
    # print(stemmed_tokens)