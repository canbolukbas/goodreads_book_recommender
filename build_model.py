'''
To-Do's:
- Currently, I'm just applying tf-idf. I didn't select informative words.
'''
from helper import *
import json
import math
import os

def create_parsed_book_informations_json():

    # extract the contents of the given urls
    filepath = "./books.txt"
    file_book_urls = open(filepath, 'r')
    book_urls = []
    for line in file_book_urls:
        book_urls.append(line.split('\n')[0])
    file_book_urls.close()

    docs = {"books": []}
    for book_url in book_urls:
        try:
            title, author, description, urls_of_recommended_books, genres = helper.parse(book_url)
        except:
            docs['books'].append({'title': "", 'author': [], 'description': "", 'urls_of_recommended_books': [], 'genres': []})
        else:
            docs['books'].append({'title': title, 'author': author, 'description': description, 'urls_of_recommended_books': urls_of_recommended_books, 'genres': genres})

    # Save the contents in JSON format.
    json_saver("parsed_book_informations.json", docs)

def get_tf_df_tables():
    term_frequency_table = dict()
    document_frequency_table = dict()
    for book_id, book_info in enumerate(parsed_book_informations['books']):
        doc = book_info['description']
        tokens = normalize(doc)

        # Construct document freq.(df) table.
        # df represents the number of documents a term appears on.
        for token in set(tokens):
            if token in document_frequency_table:
                document_frequency_table[token] += 1
            else:
                document_frequency_table[token] = 1
                
        # Construct term freq.(tf) table.
        # tf represents number of times a term appears on each document.
        for token in tokens:

            if token in term_frequency_table:
                if book_id in term_frequency_table[token]:
                    term_frequency_table[token][book_id] += 1
                else:
                    term_frequency_table[token][book_id] = 1
            else:
                term_frequency_table[token] = {book_id: 1}
    
    return term_frequency_table, document_frequency_table

def get_tf_idf_table():
    # w(t, d) =(1+log10tf(t,d))×log10(N/df(t))
    # tf_idf table will be in size of len(total_tokens) x len(total_documents)
    tf_idf_table = [[0 for j in range(len(parsed_book_informations['books']))] for i in range(len(term_frequency_table))] 
    for i,term in enumerate(term_frequency_table):
        for j, book_id in enumerate(term_frequency_table[term]):
            # since tf_table is dictionary, no entry is zero. therefore make log calculations without checking if zero.
            # also document frequency table entries are all non-zero.
            idf = math.log10(len(parsed_book_informations['books']) / document_frequency_table[term])
            tf_idf_table[i][book_id] = (1 + math.log10(term_frequency_table[term][book_id])) * idf
    return tf_idf_table



# MAIN

# If "parsed_book_informations.json" is not in the current directory, it'll be created.
# This will take about 1.5-2 hours.
path = os.getcwd() + "/parsed_book_informations.json"
if os.path.exists(path):
    print("Parsed Book Informations found in the current directory.")
else:
    print("Parsed book informations couldn't be found under the current directory. Creating this file will take about 1.5-2 hours.")
    create_parsed_book_informations_json()

# read parsed book informations by JSON module
parsed_book_informations = json_reader("parsed_book_informations.json")

# Identify term and inverse document frequencies.
term_frequency_table, document_frequency_table = get_tf_df_tables()

# Save tf in JSON format.
json_saver("tf.json", term_frequency_table)

# Save df in JSON format.
json_saver("df.json", document_frequency_table)

# Creating tf-idf table.
tf_idf_table = get_tf_idf_table()
    
# Save tf_idf in JSON format.
json_saver("tf_idf.json", tf_idf_table)

# Select informative words by setting min/max thresholds on freq and number of terms(or sth else)
# Encode each book's description by using the occurences and scores of these informative words

# build and save the model with "selected" informative terms