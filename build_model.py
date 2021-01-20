from helper import *
import json
import math
import os
import sys

def create_parsed_book_informations_json(book_urls_file):

    # extract the contents of the given urls
    filepath = book_urls_file
    file_book_urls = open(filepath, 'r')
    book_urls = []
    for line in file_book_urls:
        book_urls.append(line.split('\n')[0])
    file_book_urls.close()

    docs = {"books": []}
    for book_url in book_urls:
        try:
            title, author, description, urls_of_recommended_books, genres = parse(book_url)
        except:
            docs['books'].append({'title': "", 'author': [], 'description': "", 'urls_of_recommended_books': [], 'genres': [], 'url': book_url})
        else:
            docs['books'].append({'title': title, 'author': author, 'description': description, 'urls_of_recommended_books': urls_of_recommended_books, 'genres': genres, 'url': book_url})

    # Save the contents in JSON format.
    json_saver("parsed_book_informations.json", docs)

def get_tf_df_tables(chosen_column_as_data, parsed_book_informations):
    term_frequency_table = dict()
    document_frequency_table = dict()
    for book_id, book_info in enumerate(parsed_book_informations['books']):
        doc = book_info[chosen_column_as_data]
        if chosen_column_as_data == "description":
            tokens = normalize(doc)
        else:
            # Adding normalization for genres ?
            tokens = doc

        # Construct document freq.(df) table.
        # df represents the number of documents a term appears on.
        ordered_tokens = sorted(tokens)
        set_of_tokens = set()
        for token in ordered_tokens:
            
            # If token is already in set of tokens, no need to use it for df.
            if token in set_of_tokens:
                continue
            else:
                set_of_tokens.add(token)
            
            if token in document_frequency_table:
                document_frequency_table[token] += 1
            else:
                document_frequency_table[token] = 1
                
        # Construct term freq.(tf) table.
        # tf represents number of times a term appears on each document.
        # Sorting is necessary for checking the index of a term in single_url_recommendation/get_term_index_from_tfidf()
        for token in ordered_tokens:

            if token in term_frequency_table:
                if book_id in term_frequency_table[token]:
                    term_frequency_table[token][book_id] += 1
                else:
                    term_frequency_table[token][book_id] = 1
            else:
                term_frequency_table[token] = {book_id: 1}
    
    return term_frequency_table, document_frequency_table

def get_tf_idf_table(term_frequency_table, document_frequency_table, parsed_book_informations):
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
def build_model_main(book_urls_file):
    # If "parsed_book_informations.json" is not in the current directory, it'll be created.
    # This will take about 1.5-2 hours.
    path = os.getcwd() + "/parsed_book_informations.json"
    if os.path.exists(path):
        print("Parsed Book Informations found in the current directory.")
    else:
        print("Parsed book informations couldn't be found under the current directory. Creating this file would take long.")
        create_parsed_book_informations_json(book_urls_file)

    # read parsed book informations by JSON module
    parsed_book_informations = json_reader("parsed_book_informations.json")

    # Identify term and inverse document frequencies for book descriptions.
    tf_description, df_description = get_tf_df_tables("description", parsed_book_informations)

    # Creating tf-idf table for book descriptions.
    tf_idf_table_for_description = get_tf_idf_table(tf_description, df_description, parsed_book_informations)
        
    # Save tf_idf in JSON format.
    json_saver("tf_idf_description.json", tf_idf_table_for_description)

    # Save df in in JSON format
    json_saver("df_description.json", df_description)

    # Identify term and inverse document frequecies for book genres.
    tf_genres, df_genres = get_tf_df_tables("genres", parsed_book_informations)

    # Creating tf-idf table for book descriptions.
    tf_idf_table_for_genres = get_tf_idf_table(tf_genres, df_genres, parsed_book_informations)
        
    # Save tf_idf in JSON format.
    json_saver("tf_idf_genres.json", tf_idf_table_for_genres)

    # Save df in in JSON format
    json_saver("df_genres.json", df_genres)