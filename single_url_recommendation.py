'''
To-Do's:
- not sure about get_18books-urls
'''

from helper import *
import math
import json
import sys

def get_top18books_urls(parsed_book_informations, top18books):
    top18books_urls = []
    for book_id in top18books:
        top18books_urls.append(parsed_book_informations['books'][book_id]['url'])
    return top18books_urls

def evaluate(parsed_book_informations, top18books, urls_of_recommended_books):
    # To evaluate, I need their urls.
    top18books_urls = get_top18books_urls(parsed_book_informations, top18books)

    precision_acc = 0
    counter = 0
    for i, url in enumerate(top18books_urls):
        if url in set(urls_of_recommended_books):
            counter += 1
            precision_acc += (counter / (i+1))

    final_precision = len(set(top18books_urls).intersection(set(urls_of_recommended_books))) / len(top18books_urls)
    if counter != 0:
        average_precision = precision_acc / len(set(top18books_urls).intersection(set(urls_of_recommended_books)))
    else:
        average_precision = 0

    return average_precision, final_precision

def get_recommendations(combined_scores):
    top18books = []
    temp = sorted(combined_scores, key= float, reverse= True)
    for i, item in enumerate(temp):
        if i > 17:
            break
        top18books.append(combined_scores.index(item))
        # assert scores_normalized[scores_normalized.index(item)] == item
    #print(top18books)
    return top18books

def print_book_content(title, authors, description, urls_of_recommended_books, genres):

    print("title:")
    print(title)
    print()
    print("authors:")
    print(", ".join(authors))
    print()
    print("Description")
    print(description)
    print()
    print("urls of recommended books:")
    for url in urls_of_recommended_books:
        print(url)
    print()
    print("Genres: ")
    print(", ".join(genres))
    print()

def get_book_similarity(scores_normalized, scores_normalized_genres):
    alpha = 0.5
    
    combined_scores = []
    assert len(scores_normalized) == len(scores_normalized_genres)
    for i in range(len(scores_normalized)):
        combined_scores.append(alpha*scores_normalized[i] + (1-alpha)*scores_normalized_genres[i])
    return combined_scores

def calculate_query_term_weight(term, query, df, parsed_book_informations):
    counter = 0
    # Doing this for every term is very inefficient.
    for qt in query:
        if qt == term:
            counter += 1
    
    if term not in df:
        return (1 + math.log10(counter))* math.log10(len(parsed_book_informations['books']))
    else:
        return (1 + math.log10(counter))* (math.log10(len(parsed_book_informations['books']) / (1 + df[term])))
    
def calc_lengths(arrs):
    lengths = []
    for arr in arrs:
        acc = 0
        for i in arr:
            acc += i*i
        lengths.append(math.sqrt(acc))
    return lengths

def get_term_index_from_df(term, df):
    terms = list(df.keys())
    return terms.index(term)

def calculate_document_vectors(query, tfidf, df, parsed_book_informations):
    document_vectors = [[] for i in range(len(parsed_book_informations['books']))]
    for i, term in enumerate(query):
        # if term does not exist in the corpus, ignore. Move to another term.
        if term not in list(df.keys()):
            continue
        for book_id, tfidf_value in enumerate(tfidf[get_term_index_from_df(term, df)]):
            document_vectors[book_id].append(tfidf_value)
    return document_vectors
        
def get_normalized_scores_new(scores, vector_lengths, query_length):
    assert len(scores) == len(vector_lengths)
    normalized_scores = []
    for i in range(len(scores)):
        # Try/Except usage is not a solid solution. Can be improved.
        try:
            normalized_scores.append(scores[i]/(vector_lengths[i]* query_length))
        except:
            normalized_scores.append(0)
    return normalized_scores

def get_cosine_similarity_scores_new(tfidf, df, query, parsed_book_informations):
    scores = [0 for i in range(len(parsed_book_informations['books']))]
    query_term_weight_list = []
    for term in query:
        query_term_weight = calculate_query_term_weight(term, query, df, parsed_book_informations)
        query_term_weight_list.append(query_term_weight)
        # This is due to usage of 2D array for tf-idf instead of a dict.
        # Check if the term exists in the Corpus, if doesn't exists continue
        if term not in list(df.keys()):
            # print(term)
            continue
        term_index = get_term_index_from_df(term, df)
        for i, weight in enumerate(tfidf[term_index]):
            scores[i]+=(weight * query_term_weight)
    
    query_length = calc_lengths([query_term_weight_list])[0]
    document_vectors = calculate_document_vectors(query, tfidf, df, parsed_book_informations)
    document_vector_lengths = calc_lengths(document_vectors)
    return get_normalized_scores_new(scores, document_vector_lengths, query_length)

def get_book_information(book_id, parsed_book_informations):
    book_json = parsed_book_informations['books'][book_id]
    return book_json['title'], book_json['author']

def print_books(book_id_arr, parsed_book_informations):
    # Construct the information list.
    book_informations = []
    for book_id in book_id_arr:
        title, author = get_book_information(book_id, parsed_book_informations)
        book_informations.append([title, author])
    
    # Print the list.
    print("My 18 recommendations:")
    for book_info in book_informations:
        print("Title : {}".format(book_info[0]))
        print("Author : {}".format(", ".join(book_info[1])))
        print()
    print()

# MAIN
def main(book_url):
    # Extract the content of the book whose url is given
    title, authors, description, urls_of_recommended_books, genres = parse(book_url)

    # Print the book content 
    print_book_content(title, authors, description, urls_of_recommended_books, genres)

    # Perform tokenization and normalization for description.
    terms = normalize(description)

    # Read JSON files.
    tf_idf_table = json_reader("tf_idf_description.json")
    df_description = json_reader("df_description.json")
    tf_idf_table_genres = json_reader("tf_idf_genres.json")
    df_genres = json_reader("df_genres.json")
    parsed_book_informations = json_reader("parsed_book_informations.json")

    # Get Cosine Similarity scores of books based on "Description"
    scores_normalized_description_new = get_cosine_similarity_scores_new(tf_idf_table, df_description, terms, parsed_book_informations)

    # Get Cosine Similarity scores of books based on "Genres"
    scores_normalized_genres_new = get_cosine_similarity_scores_new(tf_idf_table_genres, df_genres, genres, parsed_book_informations)

    # combine genre based and description based similarities
    combined_scores = get_book_similarity(scores_normalized_description_new, scores_normalized_genres_new)

    # Recommend 18 books based on combined_scores.
    top18books = get_recommendations(combined_scores)

    # Print informations of top 18 books.
    print_books(top18books, parsed_book_informations)

    # Evaluate the recommendations
    # Consider Goodreads recommendations as ground truth
    # top18books contains our system's recommendations
    average_precision, final_precision = evaluate(parsed_book_informations, top18books, urls_of_recommended_books)

    # Output precision and average precision scores.
    print("final_precision: " + str(final_precision))
    print("average_precision: " + str(average_precision))