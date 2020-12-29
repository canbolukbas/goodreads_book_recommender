'''
To-Do's:
- cosine similarity'de book genres da eklenecek
- I've assumed given URL already exists in given builded tf-idf model Ama bu yanlış gibi ya.
'''

import helper
import math
import json


# extract the content of the book whose url is given
# title, author, description, urls of recommended books and genres
book_url = "https://www.goodreads.com/book/show/18050143-zero-to-one"
title, authors, description, urls_of_recommended_books = helper.parse(book_url)

# output the content into terminal (I guess)
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
#print(myfile)

# Encode the content of the book.(vectorise I guess)
terms = helper.normalize(description)


# Recommend 18 books for this book with the model based on cosine similarity.
# set alpha "reasonable"
# formula on pdf
# currently only description based calculation will be performed.

# first lets read the tf_idf and tf models by JSON.
f = open("tf.json", "r")
term_frequency_table = json.load(f)
f.close()

f = open("tf_idf.json", "r")
tf_idf_table = json.load(f)
f.close()

# check the current url's id 
f = open("parsed_book_informations.json", "r")
parsed_book_informations = json.load(f)
f.close()

current_book_id = -1
for i, key in enumerate(parsed_book_informations['books']):
    # assuming there exists no books with the same title, maybe we can add another mechanism to ensure .
    if key['title'] == title:
        current_book_id = i
        break

doc_vectors = [[] for _ in range(len(parsed_book_informations['books']))]
for column in range(len(parsed_book_informations['books'])):
    for row in range(len(tf_idf_table)):
        doc_vectors[column].append(tf_idf_table[row][column])

lengths = []
for doc_vector in doc_vectors:
    acc = 0
    for val in doc_vector:
        acc += val*val
    length = math.sqrt(acc)
    lengths.append(length)

scores = []
for i in range(len(parsed_book_informations['books'])):
    curr = doc_vectors[i]
    score = 0
    for j in range(len(curr)):
        score += curr[j] * doc_vectors[current_book_id][j]
    scores.append(score)

scores_normalized = []
for i in range(len(scores)):
    scores_normalized.append(scores[i]/(lengths[i]*lengths[current_book_id]))
#print(scores_normalized)

top18books = []
temp = sorted(scores_normalized, key= float, reverse= True)
for i, item in enumerate(temp):
    if i > 17:
        break
    top18books.append(scores_normalized.index(item))
#print(top18books)

# Evaluate the recommendations
# Consider Goodreads recommendations as ground truth

# To evaluate, I need their urls.
filepath = "/Users/cakmadam98/Desktop/4.1/CmpE493/goodreads_book_recommender/books_50.txt"
file_book_urls = open(filepath, 'r')
book_urls = []
for line in file_book_urls:
    book_urls.append(line.split('\n')[0])
file_book_urls.close()

top18books_urls = []
for book_id in top18books:
    top18books_urls.append(book_urls[book_id].replace("\'", ""))
print(top18books_urls)
print()
print(urls_of_recommended_books)
print()
temp = set(top18books_urls).intersection(set(urls_of_recommended_books))
print(temp)


# Output precision and average precision scores.