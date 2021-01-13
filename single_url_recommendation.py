'''
To-Do's:
- I've assumed given URL already exists in given builded tf-idf model Ama bu yanlış gibi ya.
'''

from helper import *
import math
import json

def evaluate():
    # To evaluate, I need their urls.
    filepath = "./books.txt"
    file_book_urls = open(filepath, 'r')
    book_urls = []
    for line in file_book_urls:
        book_urls.append(line.split('\n')[0])
    file_book_urls.close()

    # print(len(book_urls))
    # print(len(parsed_book_informations['books']))
    assert len(book_urls) == len(parsed_book_informations['books'])

    top18books_urls = []
    for book_id in top18books:
            top18books_urls.append(book_urls[book_id])

    #print(top18books_urls)
    #print()
    #print(urls_of_recommended_books)
    #print()
    precision_acc = 0
    counter = 0
    for i, url in enumerate(top18books_urls):
        if url in set(urls_of_recommended_books):
            counter += 1
            precision_acc += (counter / (i+1))

    print("Intersection: ")
    print(set(top18books_urls).intersection(set(urls_of_recommended_books)))
    print()
    final_precision = len(set(top18books_urls).intersection(set(urls_of_recommended_books))) / len(top18books_urls)
    if counter != 0:
        average_precision = precision_acc / len(set(top18books_urls).intersection(set(urls_of_recommended_books)))
    else:
        average_precision = 0

    return average_precision, final_precision

def get_recommendations():
    top18books = []
    temp = sorted(combined_scores, key= float, reverse= True)
    for i, item in enumerate(temp):
        if i > 17:
            break
        top18books.append(combined_scores.index(item))
        # assert scores_normalized[scores_normalized.index(item)] == item
    #print(top18books)
    return top18books

def get_cosine_similarity_scores(tf_idf_table, current_book_id, chosen_column_as_data):

    # Get Document Vectors from TF-IDF table.
    doc_vectors = [[] for _ in range(len(parsed_book_informations['books']))]
    for column in range(len(parsed_book_informations['books'])):
        for row in range(len(tf_idf_table)):
            assert len(tf_idf_table[row]) == len(parsed_book_informations['books'])
            doc_vectors[column].append(tf_idf_table[row][column])

    # Calculate length of vectors
    lengths = []
    for doc_vector in doc_vectors:
        acc = 0
        for val in doc_vector:
            acc += val*val
        length = math.sqrt(acc)
        lengths.append(length)

    # Calculate dot product of vector pairs.
    scores = []
    for i in range(len(parsed_book_informations['books'])):
        curr = doc_vectors[i]
        score = 0
        for j in range(len(curr)):
            # Assumption: queried book exists in the corpus
            score += curr[j] * doc_vectors[current_book_id][j]
        scores.append(score)

    # Normalize dot product values.
    scores_normalized = []
    for i in range(len(scores)):
        if lengths[i]==0 or lengths[current_book_id]==0:
            scores_normalized.append(0)
        else:
            scores_normalized.append(scores[i]/(lengths[i]*lengths[current_book_id]))
    #print(scores_normalized)
    assert len(scores_normalized) == len(parsed_book_informations['books'])

    return scores_normalized

def get_current_book_id():
    current_book_id = -1
    for i, key in enumerate(parsed_book_informations['books']):
        # assuming there exists no books with the same title, maybe we can add another mechanism to ensure .
        if key['title'] == title:
            current_book_id = i
            break
    
    return current_book_id

def print_book_content():

    print("title: " + title)
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
    # jaqqard_coefficients_of_books
    # scores_normalized

    alpha = 0.8
    
    combined_scores = []
    assert len(scores_normalized) == len(scores_normalized_genres)
    for i in range(len(scores_normalized)):
        combined_scores.append(alpha*scores_normalized[i] + (1-alpha)*scores_normalized_genres[i])
    return combined_scores

def calculate_query_term_weight(term, query, df):
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

def get_normalized_scores(vector):
    N = len(vector)
    length = calc_lengths(vector)
    normalized_vector = []
    assert len(length) == N
    for i in range(N):
        normalized_vector.append(vector[i]/length[i])
    return normalized_vector

def get_term_index_from_df(term, df):
    terms = list(df.keys())
    return terms.index(term)

def calculate_document_vectors(query, tfidf, df):
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

def get_cosine_similarity_scores_new(tfidf, df, query):
    scores = [0 for i in range(len(parsed_book_informations['books']))]
    query_term_weight_list = []
    for term in query:
        query_term_weight = calculate_query_term_weight(term, query, df)
        query_term_weight_list.append(query_term_weight)
        # This is due to usage of 2D array for tf-idf instead of a dict.
        # Check if the term exists in the Corpus, if doesn't exists continue
        if term not in list(df.keys()):
            continue
        term_index = get_term_index_from_df(term, df)
        for i, weight in enumerate(tfidf[term_index]):
            scores[i]+=(weight * query_term_weight)
    
    query_length = calc_lengths([query_term_weight_list])[0]
    document_vectors = calculate_document_vectors(query, tfidf, df)
    document_vector_lengths = calc_lengths(document_vectors)
    return get_normalized_scores_new(scores, document_vector_lengths, query_length)

# MAIN

# Extract the content of the book whose url is given
book_url = "https://www.goodreads.com/book/show/18288.Critique_of_Pure_Reason"
title, authors, description, urls_of_recommended_books, genres = parse(book_url)

# Print the book content 
print_book_content()

# Perform tokenization and normalization for description.
terms = normalize(description)

# Read JSON files.
tf_idf_table = json_reader("tf_idf_description.json")
df_description = json_reader("df_description.json")
tf_idf_table_genres = json_reader("tf_idf_genres.json")
df_genres = json_reader("df_genres.json")
parsed_book_informations = json_reader("parsed_book_informations.json")

# Get Current Book's ID
current_book_id = get_current_book_id()

# Get Cosine Similarity scores of books based on "Description"
scores_normalized_description_new = get_cosine_similarity_scores_new(tf_idf_table, df_description, terms)

# Get Cosine Similarity scores of books based on "Genres"
scores_normalized_genres_new = get_cosine_similarity_scores_new(tf_idf_table_genres, df_genres, genres)

# Get Cosine Similarity scores of each book based on "Description"
scores_normalized = get_cosine_similarity_scores(tf_idf_table, current_book_id, "description")

# Get Cosine Similarity scores of each book based on "Genres"
scores_normalized_genres = get_cosine_similarity_scores(tf_idf_table_genres, current_book_id, "genres")

# combine genre based and description based similarities
# combined_scores = get_book_similarity(scores_normalized, scores_normalized_genres)
combined_scores = get_book_similarity(scores_normalized_description_new, scores_normalized_genres_new)

# Recommend 18 books based on combined_scores.
top18books = get_recommendations()

# Evaluate the recommendations
# Consider Goodreads recommendations as ground truth
# top18books contains our system's recommendations
average_precision, final_precision = evaluate()

# Output precision and average precision scores.
print("final_precision: " + str(final_precision))
print("average_precision: " + str(average_precision))