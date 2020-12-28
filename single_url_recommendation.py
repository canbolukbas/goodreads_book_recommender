import urllib.request


# extract the content of the book whose url is given
# title, author, description, urls of recommended books and genres
book_url = "https://www.goodreads.com/book/show/18050143-zero-to-one"
f = urllib.request.urlopen(book_url)
myfile = f.read()
print(myfile)

# output the content into terminal (I guess)

# Encode the content of the book.(vectorise I guess)

# Recommend 18 books for this book with the model based on cosine similarity.
# set alpha "reasonable"
# formula on pdf

# Evaluate the recommendations
# Consider Goodreads recommendations as ground truth

# Output precision and average precision scores.