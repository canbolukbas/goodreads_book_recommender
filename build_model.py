'''
To-Do's:
- Decide how to include book genres. Genres is not considered right now.
- Parse the other html informations and store them(?)
- Use actual dataset, not the smaller one.
- Currently, I'm just applying tf-idf. I didn't select informative words.
'''
import helper
import json
import math

'''
# extract the contents of the given urls
filepath = "/Users/cakmadam98/Desktop/4.1/CmpE493/goodreads_book_recommender/books.txt"
file_book_urls = open(filepath, 'r')
book_urls = []
for line in file_book_urls:
    book_urls.append(line.split('\n')[0])
file_book_urls.close()

docs = {"books": []}
for book_url in book_urls:
    try:
        title, author, description, urls_of_recommended_books = helper.parse(book_url)
    except:
        docs['books'].append({'title': "", 'author': [], 'description': "", 'urls_of_recommended_books': []})
    docs['books'].append({'title': title, 'author': author, 'description': description, 'urls_of_recommended_books': urls_of_recommended_books})

# Save the contents in JSON format.
f = open("parsed_book_informations.json", "w")
json.dump(docs, f, indent=2)
f.close()
'''
# read parsed book informations by JSON module
f = open("parsed_book_informations.json", "r")
parsed_book_informations = json.load(f)
f.close()

# identify terms and calculate weights
# tf-idf weighting is a must.
# process descriptions.
# identify vocabulary.
# Identify term and inverse document frequencies.
term_frequency_table = dict()
document_frequency_table = dict()
for book_id, book_info in enumerate(parsed_book_informations['books']):
    doc = book_info['description']
    tokens = helper.normalize(doc)

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

    
# Save tf in JSON format.
f = open("tf.json", "w")
json.dump(term_frequency_table, f, indent=2)
f.close()

# Save df in JSON format.
f = open("df.json", "w")
json.dump(document_frequency_table, f, indent=2)
f.close()

# Creating tf-idf table and saving it also.
# w(t, d) =(1+log10tf(t,d))×log10(N/df(t))
# tf_idf table will be in size of len(total_tokens) x len(total_documents)
tf_idf_table = [[0 for j in range(len(parsed_book_informations['books']))] for i in range(len(term_frequency_table))] 
for i,term in enumerate(term_frequency_table):
    for j, book_id in enumerate(term_frequency_table[term]):
        # since tf_table is dictionary, no entry is zero. therefore make log calculations without checking if zero.
        # also document frequency table entries are all non-zero.
        idf = math.log10(len(parsed_book_informations['books']) / document_frequency_table[term])
        tf_idf_table[i][book_id] = (1 + math.log10(term_frequency_table[term][book_id])) * idf
    
# Save tf_idf in JSON format.
f = open("tf_idf.json", "w")
json.dump(tf_idf_table, f, indent=2)
f.close()


# Select informative words by setting min/max thresholds on freq and number of terms(or sth else)
# Encode each book's description by using the occurences and scores of these informative words

# build and save the model with "selected" informative terms