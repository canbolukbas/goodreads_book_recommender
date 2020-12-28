'''
To-Do's:
- Decide how to include book genres
- Parse the other html informations and store them(?)
- Use actual dataset, not the smaller one.
'''
import helper
# extract the contents of the given urls

filepath = "/Users/cakmadam98/Desktop/4.1/CmpE493/goodreads_book_recommender/books_small.txt"
file_book_urls = open(filepath, 'r')
book_urls = []
for line in file_book_urls:
    book_urls.append(line.split('\n')[0])
file_book_urls.close()

docs = {"books": []}
for book_url in book_urls:
    title, author, description, urls_of_recommended_books, genres = helper.parse(book_url)
    docs['books'].append({'title': title, 'author': author, 'description': description, 'urls_of_recommended_books': urls_of_recommended_books, 'genres': genres})
    break


# save the contents in a file

# identify terms and calculate weights
# tf-idf weighting is a must.
# process descriptions.
# identify vocabulary.
# Identify term and inverse document frequencies.
# Select informative words by setting min/max thresholds on freq and number of terms(or sth else)
# Encode each book's description by using the occurences and scores of these informative words

# build and save the model with "selected" informative terms