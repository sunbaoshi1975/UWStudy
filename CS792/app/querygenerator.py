__author__ = 'sunboss'

if __name__ == '__main__':
    QG_MAX_KEYWORDS=10
    #from terminology.snomed import snomed
    from terminology.mesh import mesh
    #from terminology.icd10_diseases_and_injuries import icd10_diseases
    from terminology.nlm import nlm
else:
    from config import QG_MAX_KEYWORDS
    #from app.terminology.snomed import snomed
    from app.terminology.mesh import mesh
    #from app.terminology.icd10_diseases_and_injuries import icd10_diseases
    from app.terminology.nlm import nlm

term_snomed = []
term_mesh = []
term_icd10_diseases = []
term_nlm = []

'''
Query Generator
Input: query - original key words string, e.g. 'gall stone'
Output: refined key words string, e.g. ''
Process:
    Terminology translation, which can be done in several ways, e.g.
    1. Looking up local dictionary (manually input and/or digested from Matching MeSH/ICD)
    2. Calling SNOMED API
    3. Applying some Semantic NW technology
    4. The most relevant keyword should be put at the head of the list,
       and the list should have length limitation, e.g. <= 10 words
'''
def query(query):
    assert isinstance(query, str)

    # ToDo: Implement query translation
    #newquery = query
    kw_list =  query.split(' ')
    newkw_list = []
    for word in kw_list:
        term_translate(word, kw_list, newkw_list)

    # Assemble keyword list
    newquery = ''
    nLen = 0
    for word in newkw_list:
        if nLen > 0:
            newquery += ' '
        newquery += word
        nLen += 1
        if nLen >= QG_MAX_KEYWORDS:
            break

    print('query translated from [' + query + '] to [' + newquery + ']')
    return newquery

def append_keyword(word, nlist):
    if (not word in nlist) or (word == 'OR'):
        nlist += [word]
    return

def term_translate(word, wlist, nlist):
    new_word = word.lower()

    # Gallstone special process
    if new_word in ['stone', 'stones']:
        if 'gallstone' in nlist:
            new_word = ''
            return

    if new_word in ['gal', 'galll']:
        new_word = 'gall'
        if 'gallstone' in nlist:
            new_word = ''
            return

    if new_word in ['galstone', 'golstone', 'gollstone']:
        new_word = 'gallstone'

    if new_word.lower() == 'gall':
        if 'stone' in wlist or 'stones' in wlist:
            new_word = 'gallstone'

    # Append basic keyword
    if not new_word in nlist:
        nlist += [new_word]

    # Extend keywords
    # Looking up local dictionary (manually input and/or digested from Matching MeSH/ICD)
    if 'gallstone' in nlist:
        append_keyword('OR', nlist)
        append_keyword('biliary calculi', nlist)
        append_keyword('OR', nlist)
        append_keyword('bile duct', nlist)
    if 'hiv' in nlist:
        append_keyword('OR', nlist)
        append_keyword('AIDS', nlist)

    return

# load medical terminology
def init():
    #term_snomed = snomed.split('@')
    term_mesh = mesh.split('@')
    term_nlm = nlm.split('@')
    # ToDo: convert to JSON format

    return

# Simple test code
if __name__ == '__main__':
    init()
    query('gal gall galll')     # gall
    query('gal stone')          # gallstone
    query('gall stone stones')  # gallstone
    query('gall stone gal')     # gallstone
    query('galstone')           # gallstone
    query('golstone')           # gallstone
    query('gollstone')          # gallstone
