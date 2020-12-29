import helper


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


# Recommend 18 books for this book with the model based on cosine similarity.
# set alpha "reasonable"
# formula on pdf

# Evaluate the recommendations
# Consider Goodreads recommendations as ground truth

# Output precision and average precision scores.