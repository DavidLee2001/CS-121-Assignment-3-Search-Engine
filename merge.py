import os
import json
import ast

term_counter = 0
term_position = dict() # position in merged_index

def merge():
    with open('merged_index.txt', 'w') as merged_index:
        # dict: {open(file_name, 'r'): file position}
        index_position = dict()
        
        indexes = list()
         
        # open all partial index files
        for file in os.listdir('indexes'):
            index = open(os.path.join('indexes', file), 'r')
            index_position[index]  = index.tell()
            indexes.append(index)

        # iterate through all files to get next term to put in merged_index, repeat:
            # get all possible next term from all files (readline)
            # pick the lowest term alphabetically
            # update position of the index(ess) of that term only
            # remove the index of any term that has line == ""
            # if there are duplicates for that lowest term, merge postings 

        while len(indexes) != 0:
            possible_terms = list()
            possible_postings = list()
            count  = 0
            for index in indexes: # index = open(file_name, 'r')
                count += 1
                print(count)
                position = index_position[index] # position = index.tell()
                index.seek(position)

                line = index.readline()

                # index_position[index] = index.tell() # Update file position

                if line != "":
                    line_list = line.rstrip().split(', ', 1)
                    current_term = line_list[0]
                    current_postings = ast.literal_eval('[' + line_list[1][1:-1] + ']')

                    possible_terms.append(current_term)
                    possible_postings.append(current_postings)

                    
                else:
                    possible_terms.append(line)
                    possible_postings.append(line)


            term = min(possible_terms)
            print(term)
            postings = None
            # index_position[index] = index.tell() # Update file position


            for i, t in enumerate(possible_terms):
                if t == term:
                    if postings == None:
                        postings = possible_postings[i]
                    else:
                        postings = union_postings(postings, possible_postings[i])
                    
                    index_position[indexes[i]] = indexes[i].tell()

            for i, t in enumerate(possible_terms):
                if t == "":
                    index_position[indexes[i]] = indexes[i].tell()
                    del indexes[i]


            if term != None and postings != None: 
                global term_position
                term_position[term] = merged_index.tell()

                merged_index.write(term + ", " + str(postings) + "\n")
                global term_counter
                term_counter += 1

            

        # close all partial index files
        for index in index_position:
            index.close()

    with open('term_position.json', 'w') as file:
        json.dump(term_position, file)


def union_postings(p1, p2):
    answer = list()
    # print(p1, p2)
    while len(p1) != 0 and len(p2) != 0:
        if p1[0][0] == p2[0][0]:
            answer.append(p1[0])
            p1 = p1[1:]
            p2 = p2[1:]
        else:

            if p1[0][0] < p2[0][0]:
                answer.append(p1[0])
                p1 = p1[1:]
            else:
                answer.append(p2[0])
                p2 = p2[1:]

    if len(p1) != 0:
        for p in p1:
            answer.append(p)
    if len(p2) != 0:
        for p in p2:
            answer.append(p)

    return answer



if __name__ == '__main__':
    merge()

    print(f'Number of terms: {term_counter}\n\n')


