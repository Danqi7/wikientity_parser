import psycopg2
import wikiparagraph_parser
import pickle
import time
import argparse

'''
    parse_first_paragraph.py parses the first paragraph of wikitext given a wiki entity.
    It constructs a dictionary where key is the wiki entity title, value is a triple of
    (first paragraph of wikipedia page of the given entity, a list of paired entities);

    parse result example:
    'Plumper Islands':
    ('The Plumper Islands, also referred to as the Plumper Group, are a small group of island located between
    Hanson Island and the Pearse Islands in the Queen Charlotte Strait region of the Central Coast of British Columbia.
    The island are named for the HMS Plumper, which surveyed the Coast of British Columbia in 1858-1861.',
    ['Pearse Islands', 'Queen Charlotte Strait', 'Central Coast of British Columbia', 'Hanson Island'])

    It saves the parsing results to a local file. You can specify which file it saves into
    and how many wiki entities you want to parse by specifying the command line arguments.
    Type "parse_first_paragraph.py -h" to see more info about passing command line arguments.

    Use pickle to load results file into dictionary if you want to use the saved results later.
'''




''' input: the number of wiki entities to get from db, in format of sequence
    simply get wikitext from db
    output: a list of triple (title, body)
'''
def get_pages(count):
    pages = []
    conn = psycopg2.connect(database="wikibrain_atlasify", user="pgadmin", password="websail_stark_pg", host="stark.cs.northwestern.edu")
    cur = conn.cursor()
    cur.execute("SELECT title, body from public.raw_page WHERE is_redirect = FALSE AND is_disambig = FALSE LIMIT (%s)", count) # count is required to be in format of sequence
    rows = cur.fetchall()
    return rows


''' input: (title, body) triple for one wiki page/entity
    get the wiki explanation and its paired entities
    output: dict{title, (explanation, list of paired entities)}
'''
def parse_pages(pages):
    summaries = {}
    for page in pages:
        summary = wikiparagraph_parser.get_expl_and_entities(page)
        if summary == None:
            continue

        summaries[page[0]] = summary
    return summaries

if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser()
    timestamp = str(time.time())
    parser.add_argument("--file_name", dest="file_name", default="parse_wikitext_"+timestamp,
                        help="The file you want to save your parse results into.")
    parser.add_argument("--count", dest="count", type=int, default=30,
                        help="The number of wiki entities you want to parse")
    ARGS = parser.parse_args()
    count = []
    count.append(ARGS.count)

    # parse
    pages = get_pages(count)
    summaries = parse_pages(pages)
    print summaries

    # save results to file
    with open(ARGS.file_name, 'w') as f:
        pickle.dump(summaries, f)
