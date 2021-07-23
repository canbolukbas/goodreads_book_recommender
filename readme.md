To-Do's:
- change readme into .md file
- implement an endpoint which takes the url as a parameter and returns the list of recommendations.
- deploy.
- dockerize.
- add CI & CD.
- use external API's to get other website recommendations.

To build model:
`python query.py [PATH_OF_THE_FILE]`
e.g. `python query.py books.txt`

To see recommmendations of a single book:
`python query.py [URL_OF_THE_BOOK]`
e.g. `python query.py https://www.goodreads.com/book/show/41721428-can-t-hurt-me`

Notes:
- My python version is 3.9.0
