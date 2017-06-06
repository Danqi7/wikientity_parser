import wikipedia
import nltk
import mwparserfromhell

''' input: wikitext of wiki entity
    extracts the entity links in first section of wikitext
    output: list of entity links
'''
def get_links(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    section = wikicode.get_sections()[0]
    
    # get links for first section
    links = section.filter_wikilinks()
    entities = []
    
    # we want 'private university' instead of just 'private'
    for link in links:
        if link.text != None:
            text = link.text
        else:
            text = link.title
        text = text.encode('utf-8').strip()
        entities.append(text)
     
    return set(entities) 

''' input: wiki entity title
    Get the summary of this wikipedia entity,
    simply calling wikipedia API
    output: first paragraph of input wiki entity
'''
def get_summary(title):
    try:
        page = wikipedia.summary(title)
    except Exception as e:
        return None
    
    page = page.encode('utf-8').strip()
    return page


''' input: (title, body), both are in form of wikitexti
    wikitext is used to get all entity links
    title is used to get the first paragraph of this entity
    output: 1) None if can't get summary of this title or no entity links pair
            2) (explanation, entities paired) 
'''
def get_expl_and_entities(title_and_body):
    wikitext = title_and_body[1]
    title = title_and_body[0]
    links = get_links(wikitext)
    
    explanation = get_summary(title)
    if explanation == None:
        return None

    entities = []
    
    for link in links:
        if link in explanation:
            entities.append(link)

    if not entities:
        return None

    return explanation, entities

if __name__ == "__main__":
    with open('sample1.txt', 'r') as f:
        wikitext = f.read()
