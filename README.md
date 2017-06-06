# wikientity_parser
This is a git repo for parsing first paragraph of wiki entity. Its goal is to construct training data for concept pair explanation.

It constructs a dictionary where key is the wiki entity title, value is a triple of (first paragraph of wikipedia page of the given entity, a list of paired entities).It saves the parsing results to a local file. You can specify which file it saves into and how many wiki entities you want to parse by specifying the command line arguments. It saves the parsing results to a local file.
# Requirements
- Python 2.7 in Linux
- nltk (http://www.nltk.org/)
- wikipedia (https://pypi.python.org/pypi/wikipedia/)
- mwparserfromhell (https://github.com/earwig/mwparserfromhell)
- psycopg2 (http://initd.org/psycopg/) (if you are using different db, then use the corresponding python db interface)
# How to Start Parsing
0. Make sure you are on Linux with correct permission to the db and have all the dependencies installed.
1. Make sure your db stores the wikitext downloaded from wikipedia
2. Use the following command to see more info about passing command line arguments.
```
python parse_first_paragraph.py -h
```
3. Use pickle to unwrap the saved parsed result file into dictionary if you want to use the parse results later in your code
