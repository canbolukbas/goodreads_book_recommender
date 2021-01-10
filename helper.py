'''
To-Do's:
- \\xe2\\x80\\x99 problem is solved. But other may emerge.
- Informer kitabından span 1 olduğu için patlıyor.
'''

import urllib.request
import re
import string
import json

def json_reader(path: str):
    f = open(path, "r")
    text = json.load(f)
    f.close()
    return text

def json_saver(path: str, file: str):
    # Save df in JSON format.
    f = open(path, "w")
    json.dump(file, f, indent=2)
    f.close()

def authors_parser(myfile):
    try:
        # AUTHOR = <a class="authorName" itemprop="url" href=.*><span itemprop="name">.*</span></a>
        authors = re.findall('<a class="authorName" itemprop="url" href=.*?><span itemprop="name">.*?</span></a>', myfile)
        for i in range(len(authors)):
            author = authors[i]
            author = re.split('<a class="authorName" itemprop="url" href=.*?><span itemprop="name">', author)[-1]
            authors[i] = re.split('</span></a>', author)[0]
    except:
        authors = []
    #print("authors : " + ", ".join(authors))
    #print()
    return authors

def genre_parser(text):
    try:
        lines = re.findall('<a class="actionLinkLite bookPageGenreLink" href=".*?">.*?</a>', text)
        result = []
        for line in lines:
            result.append(re.split('<a class="actionLinkLite bookPageGenreLink" href=".*?">', line)[-1].split("</a>")[0])
    except:
        return []
    else:
        # print(result)
        return result

def title_parser(myfile):
    # calculations on myfile
    # TITLE = <h1 id="bookTitle" class="gr-h1 gr-h1--serif" itemprop="name">\n ....... \n</h1>
    try:
        title = re.search("<h1.*</h1>", myfile).group().split("\\n")[1].lstrip().rstrip()
    except:
        title = ""
    
    #print("title: " + title)
    #print()
    return title

def description_parser(myfile):
    try:
        # DESCRIPTION = <div id="description" class="readable stacked" style="right:0"> </div> arasında. fakat ilk span değil, ikinci span. ikinci spande <div> ile </div> arasında. </p><p>'leri filan ignore et.
        description_readable_stacked = re.findall('<div id="description" class="readable stacked" style="right:0">.*?<a data-text-id=".*?" href="#" onclick', myfile)[0]
        #print(description_readable_stacked)
        #print()
        span = re.findall('<span id=".*?".*?</span>' , description_readable_stacked)[1] # first one is the short one
        #print(span)
        #print()
        # cleaning description from tags
        description = " ".join(re.split('<br ?/>',re.split('</span>', re.split('<span id=".*?".*?>',span)[-1])[0]))
        # replace \xe2\x80\x99 with '
        description = description.replace('\\xe2\\x80\\x99', '\'')
    except:
        description = ""
    #print("Description:")
    #print(description)
    #print()
    return description

def recommendations_parser(myfile):
    try:
        temp = re.findall('li class=.*?cover.*?id=.*?bookCover_.*?.*?>.*?n<a href=".*?"><img alt="', myfile)
        urls_of_recommended_books = []
        for tempp in temp:
            urls_of_recommended_books.append(re.split('"><img alt="',re.split('li class=.*?cover.*?id=.*?bookCover_.*?.*?>.*?n<a href="', tempp)[-1])[0])
    except:
        urls_of_recommended_books = []
    
    return urls_of_recommended_books

def parse(url: str):

    # Get url content and store it as a string.
    f = urllib.request.urlopen(url)
    myfile = str(f.read())
    f.close()

    # Parse book contents
    title = title_parser(myfile)
    authors = authors_parser(myfile)
    description = description_parser(myfile)
    urls_of_recommended_books = recommendations_parser(myfile)
    genres = genre_parser(myfile)

    return title, authors, description, urls_of_recommended_books, genres

def normalize(text):

    # case-folding
    text = text.lower()

    # convert punctuations into whitespace, instead of deleting them
    # e.g. in "string1/string2" case, it is better to convert it into whitespace
    text_with_no_punc = ""
    punc_set = set(string.punctuation)
    for ch in text:
        if ch not in punc_set:
            text_with_no_punc += ch
        else:
            text_with_no_punc += " "

    
    # white space removal
    tokens = text_with_no_punc.split()

    # removing tokens with 0 length (idk how it's possible)
    temp = []
    for token in tokens:
        if len(token) == 0:
            continue

        temp.append(token)

    return temp